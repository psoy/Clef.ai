import chromadb
from chromadb.utils import embedding_functions
import uuid

# Initialize ChromaDB client
# Persistent client to save data to disk
client = chromadb.PersistentClient(path="data/chromadb")

# Use default embedding function (all-MiniLM-L6-v2)
# This downloads the model locally.
embedding_fn = embedding_functions.DefaultEmbeddingFunction()

# Create or get collection
collection = client.get_or_create_collection(
    name="sheet_music",
    embedding_function=embedding_fn
)

def add_to_vector_db(abc_content: str, metadata: dict):
    """
    Adds ABC notation content to the vector database.
    
    Args:
        abc_content (str): The ABC notation string.
        metadata (dict): Metadata about the piece (filename, title, etc.)
    """
    # Chunking strategy:
    # For music, we might want to chunk by measures or sections.
    # For simplicity, we'll just add the whole piece or large chunks for now.
    # In a real app, we'd parse the ABC and split by bars.
    
    # Simple chunking by lines for now to avoid token limits if the piece is huge
    # But ABC is compact, so maybe 10-20 lines per chunk?
    
    lines = abc_content.split('\n')
    chunk_size = 20
    chunks = []
    ids = []
    metadatas = []
    
    for i in range(0, len(lines), chunk_size):
        chunk = '\n'.join(lines[i:i+chunk_size])
        if not chunk.strip():
            continue
            
        chunks.append(chunk)
        ids.append(str(uuid.uuid4()))
        metadatas.append(metadata)
        
    if chunks:
        collection.add(
            documents=chunks,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Added {len(chunks)} chunks to Vector DB.")

def query_rag(query_text: str, n_results: int = 3):
    """
    Queries the vector database for relevant sheet music chunks.
    
    Args:
        query_text (str): The user's query.
        n_results (int): Number of results to return.
        
    Returns:
        dict: Query results.
    """
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    
    return results

if __name__ == "__main__":
    # Test RAG
    # add_to_vector_db("X:1\nT:Test\nK:C\nCDEF GABc|", {"title": "Test Scale"})
    # print(query_rag("scale"))
    pass
