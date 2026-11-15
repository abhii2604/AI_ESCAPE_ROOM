
import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

load_dotenv(Path(__file__).with_name(".env"), override=True)

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

print("Checking available Gemini models...\n")

try:
    for model in client.models.list():
        if "generateContent" in (model.supported_actions or []):
            print(model.name)

except Exception as error:
    print("MODEL CHECK FAILED:")
    print(repr(error))
