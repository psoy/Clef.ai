import os
import sys

# Add backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.agent import create_clef_agent

def test_agent():
    print("Testing Clef Agent...")
    
    # Mock API key if not present to trigger mock agent
    if "OPENAI_API_KEY" not in os.environ:
        print("No API Key found, expecting Mock Agent.")
    else:
        print("API Key found, expecting Real Agent.")

    try:
        agent = create_clef_agent()
        query = "What is the key of measure 1 in simple.xml?"
        print(f"Invoking agent with query: {query}")
        
        response = agent.invoke({"input": query})
        print("Response received:")
        print(response["output"])
        
    except Exception as e:
        print(f"Agent failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_agent()
