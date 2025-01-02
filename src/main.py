from src.interface.game import GameInterface
from src.constants import WELCOME_ASCII
from src.grid.grid import Grid

# TODO: Implement text/cli interface (no PyGame)

goal_queue = [
    {
        "navigate": {
            "name": "Coffee and Donuts",
            "x": 1,
            "y": 10,
            "floor": 1,
            "keywords": ["coffee", "food and drink", "snacks"],
            "aliases": ["E7 Cafe", "CnD"],
        }
    },
    {"speak": "Can I have the key?"},
    {"wait": 10},
    {
        "navigate": {
            "name": "RoboHub Entrance",
            "x": 1,
            "y": 1,
            "floor": 1,
            "keywords": ["workshop", "robots"],
        }
    },
]

grid = Grid(rows=60, cols=30)
game = GameInterface(grid)

if __name__ == "__main__":
    print(WELCOME_ASCII)
    game.run()
