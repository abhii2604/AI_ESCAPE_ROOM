
from game import EscapeRoomGame


game = EscapeRoomGame()

print("\n===== AI ESCAPE ROOM TESTING =====")

# Test 1: Examine bookshelf
result = game.examine_object("bookshelf")
print("\nTest 1 - Bookshelf:")
print(result)
assert "2, 5, 8 and 4" in result

# Test 2: Try incorrect drawer code
result = game.unlock_drawer("1234")
print("\nTest 2 - Incorrect drawer code:")
print(result)
assert game.drawer_unlocked is False

# Test 3: Unlock drawer with correct code
result = game.unlock_drawer("2584")
print("\nTest 3 - Correct drawer code:")
print(result)
assert game.drawer_unlocked is True
assert "key" in game.inventory

# Test 4: Examine painting
result = game.examine_object("painting")
print("\nTest 4 - Painting:")
print(result)
assert "7391" in result

# Test 5: Unlock exit door
result = game.unlock_door("7391")
print("\nTest 5 - Escape:")
print(result)
assert game.escaped is True

print("\n===== ALL TESTS PASSED SUCCESSFULLY! =====")

