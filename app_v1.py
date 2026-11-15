
import os
import requests
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).with_name(".env"))

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-3.5-flash"

SYSTEM_PROMPT = """
You are the AI Game Master of The Mystery of the Locked Library.

STORY:
The player wakes up in a locked library.
There are five interactive objects:
1. An old wooden desk.
2. A bookshelf containing four unusual books.
3. A mysterious painting.
4. A locked drawer.
5. A locked exit door.

GAME RULES:
- Guide the player through the escape room.
- Respond naturally to player messages.
- Describe clues when the player examines objects.
- The bookshelf contains a clue leading to drawer code 2584.
- The painting contains a clue leading to final code 7391.
- The drawer contains a key.
- The player needs the key and final code to escape.
- Remember the player's actions from the conversation.
- Do not invent extra objects.
- Do not reveal all solutions immediately.
- Give hints when requested.
- Keep responses engaging and relatively short.
- You are responsible for managing the story and game progress
  in this Version 1 prototype.
"""

st.set_page_config(page_title="AI Escape Room - Version 1", page_icon="🔐")

st.title("🔐 AI Escape Room — Version 1")
st.caption("Interactive AI Game Master | The Mystery of the Locked Library")

if "history" not in st.session_state:
    st.session_state.history = [
        {
            "role": "assistant",
            "content": (
                "Welcome to the Locked Library! You wake up in a "
                "mysterious room. The exit is locked. What would "
                "you like to investigate first?"
            )
        }
    ]

if not API_KEY:
    st.error("Gemini API key not found. Check your .env file.")
    st.stop()

with st.sidebar:
    st.header("Game Information")
    st.write("Version 1: AI-managed game")
    st.write("Game Master: Gemini")
    st.write("Objects: Desk, Bookshelf, Painting, Drawer, Door")

    if st.button("Restart Game"):
        st.session_state.history = [
            {
                "role": "assistant",
                "content": "Welcome back! Your escape-room adventure begins again."
            }
        ]
        st.rerun()

st.subheader("💬 Talk to the AI Game Master")

for message in st.session_state.history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("What would you like to do?"):

    st.session_state.history.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.write(prompt)

    conversation = "\n".join(
        f"{m['role'].upper()}: {m['content']}"
        for m in st.session_state.history[-12:]
    )

    payload = {
        "systemInstruction": {
            "parts": [{"text": SYSTEM_PROMPT}]
        },
        "contents": [
            {
                "parts": [
                    {
                        "text": "Continue this game conversation:\n" + conversation
                    }
                ]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": API_KEY
    }

    with st.chat_message("assistant"):
        with st.spinner("Game Master is thinking..."):
            try:
                response = requests.post(
                    f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",
                    headers=headers,
                    json=payload,
                    timeout=60
                )
                response.raise_for_status()

                answer = response.json()["candidates"][0]["content"]["parts"][0]["text"]

            except Exception as error:
                answer = "The Game Master is temporarily unavailable. Please try again."
                print("Gemini error:", error)

        st.write(answer)

    st.session_state.history.append(
        {"role": "assistant", "content": answer}
    )
