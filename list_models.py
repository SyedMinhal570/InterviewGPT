import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()  # .env file se key load karega
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("Available models that support generateContent:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"  - {m.name}")