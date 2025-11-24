from typing import Optional
import os
from rag_indexer import get_index

# Initialize LlamaIndex (Lazy load to avoid overhead on import if possible, but for now global)
_index = None

def get_rag_engine():
    global _index
    if _index is None:
        # Load from persistence
        _index = get_index(data_dir="../MusicXML_test", persist_dir="data/chromadb")
    return _index.as_query_engine() if _index else None

def music_retrieval(query: str, instrument: Optional[str] = None, measure_number: Optional[int] = None):
    """
    Retrieves musical information from the sheet music database.
    """
    engine = get_rag_engine()
    if not engine:
        return "RAG engine not initialized."
    
    refined_query = query
    if instrument:
        refined_query += f" (Instrument: {instrument})"
    if measure_number:
        refined_query += f" (Measure: {measure_number})"
        
    try:
        response = engine.query(refined_query)
        return str(response)
    except Exception as e:
        return f"Error querying RAG: {str(e)}"

class SimpleAgent:
    """Simple agent that wraps RAG queries without complex LangChain dependencies."""
    
    def invoke(self, inputs: dict):
        """Process user input and return response."""
        user_message = inputs.get("input", "")
        
        # Check if we have an API key for full LLM responses
        if not os.environ.get("OPENAI_API_KEY"):
            # Use RAG only mode
            try:
                rag_response = music_retrieval(user_message)
                return {
                    "output": f"[RAG Response - No LLM]\n\n{rag_response}\n\nNote: For better responses, please provide an OpenAI API key."
                }
            except Exception as e:
                return {
                    "output": f"I'm a mock agent. I need an OpenAI API key to provide full responses. Error: {str(e)}"
                }
        
        # If we have an API key, we could use full LangChain here
        # For now, still use RAG only
        try:
            rag_response = music_retrieval(user_message)
            return {"output": rag_response}
        except Exception as e:
            return {"output": f"Error: {str(e)}"}

def create_clef_agent():
    """Creates and returns a simple agent."""
    return SimpleAgent()
