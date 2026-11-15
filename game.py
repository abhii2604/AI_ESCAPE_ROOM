
import json
from pathlib import Path


class EscapeRoomGame:

    def __init__(self):
        config_path = Path(__file__).parent / "game_config.json"

        with open(config_path, "r", encoding="utf-8") as file:
            self.config = json.load(file)

        self.inventory = []
        self.examined_objects = []
        self.drawer_unlocked = False
        self.door_unlocked = False
        self.escaped = False

    def examine_object(self, object_name):

        object_name = object_name.lower().strip()

        if object_name not in self.config["objects"]:
            return "That object does not exist in this room."

        if object_name in self.examined_objects:
            return f"You have already examined the {object_name}."

        self.examined_objects.append(object_name)

        if object_name == "desk":
            return (
                "You examine the old wooden desk. "
                "There are some papers and strange markings on it."
            )

        elif object_name == "bookshelf":
            return (
                "You notice four unusual books. "
                "Each book contains a handwritten number: "
                "2, 5, 8 and 4. "
                "Perhaps they form a code!"
            )

        elif object_name == "painting":
            return (
                "You inspect the painting carefully. "
                "Behind its frame, you discover a note: "
                "The final code is 7391."
            )

        elif object_name == "drawer":
            if self.drawer_unlocked:
                return "The drawer is already open."
            return "The drawer is locked. You need a four-digit code."

        elif object_name == "door":
            if self.escaped:
                return "You have already escaped!"
            return "The exit door is secured with a digital lock."

    def unlock_drawer(self, code):

        if self.drawer_unlocked:
            return "The drawer is already unlocked."

        if "bookshelf" not in self.examined_objects:
            return "Examine the bookshelf first to find the code."

        if code == self.config["puzzles"]["drawer_code"]:
            self.drawer_unlocked = True
            self.inventory.append("key")

            return (
                "Correct code! The drawer opens. "
                "You found a key and added it to your inventory."
            )

        return "Incorrect code. Try investigating the clues again."

    def unlock_door(self, code):

        if self.escaped:
            return "You have already escaped!"

        if not self.drawer_unlocked or "key" not in self.inventory:
            return "You need to unlock the drawer and collect the key first."

        if "painting" not in self.examined_objects:
            return "Examine the painting to discover the final clue."

        if code == self.config["puzzles"]["final_code"]:
            self.door_unlocked = True
            self.escaped = True

            return (
                "Congratulations! The door unlocks. "
                "You successfully escaped the library!"
            )

        return "Incorrect final code. Keep investigating!"

    def show_inventory(self):

        if not self.inventory:
            return "Your inventory is empty."

        return "Inventory: " + ", ".join(self.inventory)

    def get_status(self):

        return {
            "examined_objects": self.examined_objects,
            "inventory": self.inventory,
            "drawer_unlocked": self.drawer_unlocked,
            "door_unlocked": self.door_unlocked,
            "escaped": self.escaped
        }
