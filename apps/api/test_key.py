import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("GEMINI_API_KEY")
print(f"Testing key starting with: {key[:10]}... (length: {len(key)})")

client = genai.Client(api_key=key)
try:
    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents="Hello, are you there?"
    )
    print("Success!")
    print(response.text)
except Exception as e:
    print(f"Error: {e}")
