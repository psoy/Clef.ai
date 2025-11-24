import os
from dotenv import load_dotenv

# Load environment variables (override existing ones)
load_dotenv(override=True)

api_key = os.environ.get("OPENAI_API_KEY")

if api_key:
    print(f"API Key loaded: {api_key[:20]}...{api_key[-4:]}")
    print(f"Full length: {len(api_key)} characters")
    
    # Test OpenAI connection
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        # Simple test call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say hello"}],
            max_tokens=10
        )
        print("\n✅ OpenAI API connection successful!")
        print(f"Response: {response.choices[0].message.content}")
    except Exception as e:
        print(f"\n❌ OpenAI API connection failed: {e}")
else:
    print("❌ No API key found in environment")
