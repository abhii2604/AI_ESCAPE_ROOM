
from pathlib import Path
import os
from dotenv import load_dotenv
from google import genai

load_dotenv(Path(__file__).with_name(".env"), override=True)

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options={"timeout": 180000}
)

print("Sending a simple Gemini request...")

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Reply with only: Hello!"
)

print("Gemini response:", response.text)
