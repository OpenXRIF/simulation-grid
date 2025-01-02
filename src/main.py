from src.interface.game import game_loop
from src.constants import WELCOME_ASCII

# TODO: Implement text/cli interface (no PyGame)

goal_queue = [
    {
        "navigate": {
            "name": "Room 2106",
            "keywords": ["office", "zach", "WEEF"],
            "floor": 1,
        }
    },
    {},
]

if __name__ == "__main__":
    print(WELCOME_ASCII)
    game_loop()
