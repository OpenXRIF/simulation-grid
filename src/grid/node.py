from typing import Callable
from enum import Enum

class NodeAttribute(Enum):
    EMPTY = "empty"
    WALL = "wall"
    INTERACTIVE = "interactive"

class GridNode(object):
    def __init__(self, attribute: NodeAttribute = NodeAttribute.EMPTY, walkable: bool = True):
        """Initialize a grid node."""
        self.attribute = attribute
        self.walkable = walkable

    def set_walkable(self, walkable: bool):
        """Set the walkable attribute of the grid node."""
        self.walkable = walkable

    def set_interaction(self, interaction_function: Callable):
        """Set the interaction attribute of the grid node."""
        self.attribute = NodeAttribute.INTERACTIVE
        self.interact = interaction_function
       
    def __str__(self):
        """Return the string representation of the grid node."""
        return str(self.attribute.value)
