
import streamlit as st
from game import EscapeRoomGame
from gemini_game_master import get_gemini_response

st.set_page_config(
    page_title="AI Escape Room",
    page_icon="🔐",
    layout="centered"
)

# Initialize game
if "game" not in st.session_state:
    st.session_state.game = EscapeRoomGame()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Welcome to the Mystery of the Locked Library! "
                "You wake up inside a mysterious room. "
                "The exit door is locked. Explore the room and find a way to escape!"
            )
        }
    ]

game = st.session_state.game

# Title
st.title("🔐 AI-Powered Escape Room")
st.caption("The Mystery of the Locked Library")
st.divider()

# Sidebar
with st.sidebar:
    st.header("🎒 Your Inventory")

    if game.inventory:
        for item in game.inventory:
            st.write(f"🔑 {item}")
    else:
        st.write("Your inventory is empty.")

    st.divider()
    st.header("📍 Game Progress")

    st.write("Drawer:", "🔓 Unlocked" if game.drawer_unlocked else "🔒 Locked")
    st.write("Exit:", "🔓 Unlocked" if game.door_unlocked else "🔒 Locked")
    st.write("Objects examined:", len(game.examined_objects), "/ 5")

    if st.button("🔄 Restart Game"):
        st.session_state.game = EscapeRoomGame()
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Welcome back! Your new escape-room adventure begins."
            }
        ]
        st.rerun()

# Room description
st.subheader("📚 Inside the Library")
st.write(
    "You see an old desk, a bookshelf, a painting, "
    "a locked drawer and a mysterious exit door."
)

# Display conversation
st.subheader("💬 Talk to the Game")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Player interaction
if prompt := st.chat_input("What would you like to do?"):

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.write(prompt)

    command = prompt.lower().strip()
    response = ""

    if game.escaped:
        response = "You have already escaped! Restart to play again."

    elif command.startswith("examine ") or command.startswith("inspect "):
        object_name = command.split(" ", 1)[1]
        response = game.examine_object(object_name)

    elif command.startswith("unlock drawer "):
        code = command.replace("unlock drawer ", "", 1).strip()
        response = game.unlock_drawer(code)

    elif command.startswith("unlock door "):
        code = command.replace("unlock door ", "", 1).strip()
        response = game.unlock_door(code)

    elif command in ["inventory", "show inventory"]:
        response = game.show_inventory()

    elif command in ["help", "commands"]:
        response = (
            "Try these commands:\n\n"
            "- examine bookshelf\n"
            "- examine desk\n"
            "- examine painting\n"
            "- examine drawer\n"
            "- examine door\n"
            "- unlock drawer 2584\n"
            "- unlock door 7391\n"
            "- inventory"
        )

    else:
        # Use Gemini for natural conversation
        with st.spinner("The Game Master is thinking..."):
            try:
                status = str(game.get_status())
                response = get_gemini_response(prompt, status)
            except Exception as error:
                response = (
                    "The Game Master is temporarily unavailable. "
                    "Please try a game command such as 'examine bookshelf'."
                )
                print("Gemini error:", error)

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )

    with st.chat_message("assistant"):
        st.write(response)

    if game.escaped:
        st.balloons()
        st.success("🎉 Congratulations! You escaped the library!")

    # Refresh sidebar to show updated game progress
    st.rerun()
