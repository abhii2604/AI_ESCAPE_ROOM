
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load API key
load_dotenv(
    dotenv_path=Path(__file__).with_name(".env"),
    override=True
)

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("Gemini API key not found in .env")

MODEL_NAME = "gemini-3.5-flash"

SYSTEM_INSTRUCTION = """
You are the Game Master of an interactive escape room
called The Mystery of the Locked Library.

STORY:
The player wakes up inside a mysterious locked library.

The room contains:
1. An old wooden desk.
2. A bookshelf containing four unusual books.
3. A mysterious painting.
4. A locked drawer.
5. A locked exit door.

YOUR RESPONSIBILITIES:
- Act as an engaging Game Master.
- Describe the environment creatively.
- Respond naturally to player messages.
- Give hints when players ask for help.
- Make the experience mysterious and interesting.

IMPORTANT RULES:
- Do not invent new objects or items.
- Do not reveal secret codes before they are discovered.
- Never claim an action succeeded without Python confirmation.
- Never claim the player escaped without Python confirmation.
- Python controls all puzzle solutions and game progress.
- Keep responses clear and relatively short.
- Stay in character.
"""


def get_gemini_response(player_message, game_status=""):

    url = (
        "https://generativelanguage.googleapis.com/"
        f"v1beta/models/{MODEL_NAME}:generateContent"
    )

    prompt = f"""
CURRENT GAME STATUS:
{game_status}

PLAYER MESSAGE:
{player_message}

Respond as the Game Master.
Do not independently change the game state.
"""

    payload = {
        "systemInstruction": {
            "parts": [{"text": SYSTEM_INSTRUCTION}]
        },
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": API_KEY
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=60
        )

        response.raise_for_status()
        data = response.json()

        return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as error:
        print("Gemini API error:", error)
        return "The Game Master is temporarily unavailable. Please try again."
