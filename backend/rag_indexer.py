import os
from typing import List, Dict, Any
from pathlib import Path
import music21
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core.schema import Document
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb
from llama_index.core import Settings

# Don't configure at import time - do it lazily when needed
_settings_configured = False

def _configure_settings():
    """Configure embedding model and LLM based on API key availability."""
    global _settings_configured
    if _settings_configured:
        return
    
    if not os.environ.get("OPENAI_API_KEY"):
        print("OPENAI_API_KEY not found. Using local HuggingFace embeddings and mock LLM.")
        from llama_index.embeddings.huggingface import HuggingFaceEmbedding
        from llama_index.core.llms import MockLLM
        Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
        # Use MockLLM to avoid API calls during indexing
        Settings.llm = MockLLM()
    else:
        print(f"OPENAI_API_KEY found. Using OpenAI embeddings and LLM.")
        from llama_index.embeddings.openai import OpenAIEmbedding
        from llama_index.llms.openai import OpenAI
        Settings.embed_model = OpenAIEmbedding()
        Settings.llm = OpenAI(model="gpt-3.5-turbo")
    
    _settings_configured = True

# Ensure you have OPENAI_API_KEY set in your environment or .env file
# For this example, we'll assume it's available or use a placeholder if checking locally without keys.

class MusicXMLReader:
    """Custom reader for MusicXML files to extract musical data with rich metadata."""

    def load_data(self, file_path: Path) -> List[Document]:
        """Parse MusicXML and return a list of Documents (chunks)."""
        documents = []
        try:
            score = music21.converter.parse(str(file_path))
            
            # Extract Score Metadata
            title = score.metadata.title if score.metadata and score.metadata.title else file_path.stem
            composer = score.metadata.composer if score.metadata and score.metadata.composer else "Unknown"
            
            # Iterate through parts (Instruments)
            for part in score.parts:
                part_name = part.partName if part.partName else "Unknown Instrument"
                
                # Iterate through measures
                for measure in part.getElementsByClass('Measure'):
                    measure_number = measure.number
                    
                    # Extract content from measure
                    # We'll create a text representation of the measure's content
                    # e.g., "Notes: C4 quarter, D4 quarter. Dynamics: mf."
                    
                    elements_text = []
                    notes = []
                    dynamics = []
                    lyrics = []
                    
                    for element in measure.flatten():
                        if isinstance(element, music21.note.Note):
                            notes.append(f"{element.nameWithOctave} ({element.duration.type})")
                            if element.lyric:
                                lyrics.append(element.lyric)
                        elif isinstance(element, music21.chord.Chord):
                            chord_notes = "-".join([n.nameWithOctave for n in element.notes])
                            notes.append(f"Chord:{chord_notes} ({element.duration.type})")
                        elif isinstance(element, music21.dynamics.Dynamic):
                            dynamics.append(element.value)
                        elif isinstance(element, music21.expressions.TextExpression):
                            dynamics.append(element.content)
                            
                    content_str = f"Measure {measure_number} of {part_name}.\n"
                    if notes:
                        content_str += f"Notes: {', '.join(notes)}.\n"
                    if dynamics:
                        content_str += f"Dynamics/Expressions: {', '.join(dynamics)}.\n"
                    if lyrics:
                        content_str += f"Lyrics: {' '.join(lyrics)}.\n"
                        
                    # Create Document with Metadata
                    metadata = {
                        "file_name": file_path.name,
                        "title": title,
                        "composer": composer,
                        "instrument": part_name,
                        "measure_number": measure_number,
                        # Add range for easier filtering if needed later, though single measure is fine
                        "measure_start": measure_number,
                        "measure_end": measure_number
                    }
                    
                    doc = Document(text=content_str, metadata=metadata)
                    documents.append(doc)
                    
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            # Return an empty list or a document indicating error? 
            # For now, skip failed files but log it.
            pass
            
        return documents

def get_index(data_dir: str = "data/Catholic", persist_dir: str = "data/chromadb"):
    """Creates or loads the RAG index."""
    
    # Configure settings based on current environment
    _configure_settings()
    
    # Initialize ChromaDB
    db_path = os.path.join(os.path.dirname(__file__), persist_dir)
    chroma_client = chromadb.PersistentClient(path=db_path)
    chroma_collection = chroma_client.get_or_create_collection("catholic_hymns")
    
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
    # Check if we have documents to index
    # In a real app, we might check if the index is empty or check for new files.
    # For this demo, we'll just load everything if the collection is empty-ish or force reload.
    
    reader = MusicXMLReader()
    all_docs = []
    
    data_path = Path(os.path.join(os.path.dirname(__file__), data_dir))
    if not data_path.exists():
        print(f"Data directory {data_path} does not exist.")
        return None

    # Only load if we explicitly want to re-index or if it's empty. 
    # For now, let's just load a few files to test.
    
    files = list(data_path.glob("*.xml")) + list(data_path.glob("*.mxl"))
    print(f"Found {len(files)} files in {data_path}")
    
    for file_path in files:
        print(f"Processing {file_path.name}...")
        docs = reader.load_data(file_path)
        all_docs.extend(docs)
        
    if not all_docs:
        print("No documents extracted.")
        return None
        
    print(f"Indexing {len(all_docs)} chunks...")
    index = VectorStoreIndex.from_documents(
        all_docs, storage_context=storage_context
    )
    
    return index

def add_document_to_index(file_path: Path, index):
    """Adds a single file to the existing index."""
    reader = MusicXMLReader()
    docs = reader.load_data(file_path)
    if docs:
        for doc in docs:
            index.insert(doc)
        print(f"Added {len(docs)} chunks from {file_path.name}")
    else:
        print(f"No documents extracted from {file_path.name}")

if __name__ == "__main__":
    # Test run
    index = get_index(data_dir="../MusicXML_test") # Point to test dir for now
    if index:
        print("Index created successfully.")
        
        # Only test query if we have an API key (for LLM)
        if os.environ.get("OPENAI_API_KEY"):
            query_engine = index.as_query_engine()
            response = query_engine.query("What is the key or notes in measure 1?")
            print(f"Response: {response}")
        else:
            print("Skipping query test (no OPENAI_API_KEY). Index is ready for use with agent.")
