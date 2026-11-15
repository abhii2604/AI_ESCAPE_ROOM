import os
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).with_name(".env"))

api_key = os.getenv("GEMINI_API_KEY")

url = "https://generativelanguage.googleapis.com/v1beta/interactions"

headers = {
    "Content-Type": "application/json",
    "x-goog-api-key": api_key
}

payload = {
    "model": "gemini-3.8-flash",
    "input": "Reply only with Hello"
}

print("Testing Gemini 3.8 Interactions API...")

try:
    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=90
    )

    print("HTTP Status:", response.status_code)
    print("Response:", response.text[:2000])

except requests.exceptions.RequestException as error:
    print("Connection error:", repr(error))