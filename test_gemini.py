
from gemini_game_master import get_gemini_response

print("Testing Gemini AI Game Master...")

try:
    response = get_gemini_response(
        "I just woke up inside this library. Where am I?",
        "The player has just started. No objects examined."
    )

    print("\nGemini Game Master Response:")
    print(response)

    print("\nGEMINI API TEST SUCCESSFUL!")

except Exception as error:
    print("\nGEMINI API TEST FAILED:")
    print(repr(error))
