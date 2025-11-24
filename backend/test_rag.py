import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__)))

from rag import add_to_vector_db, query_rag

def test_rag():
    print("Testing RAG System...")
    
    # Sample ABC content
    abc_content = """X:1
T:Test Scale
M:4/4
L:1/4
K:C
CDEF GABc|
"""
    
    # Add to DB
    print("Adding to DB...")
    add_to_vector_db(abc_content, {"title": "Test Scale", "filename": "test.abc"})
    
    # Query
    print("Querying 'scale'...")
    results = query_rag("scale")
    
    if results and results['documents']:
        print("Query successful!")
        print(f"Found {len(results['documents'][0])} documents.")
        print("First document:", results['documents'][0][0])
    else:
        print("Query returned no results.")

if __name__ == "__main__":
    test_rag()
