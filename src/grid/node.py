import math

from typing import Callable
from enum import Enum


class NodeAttribute(Enum):
    EMPTY = "empty"
    WALL = "wall"
    INTERACTIVE = "interactive"


class GridNode(object):
    def __init__(
        self, attribute: NodeAttribute = NodeAttribute.EMPTY, walkable: bool = True
    ):
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


# TODO: Get rid of this old node system
class Node(object):
    def __init__(self, x, y, walkable=True):
        self.x = x
        self.y = y
        self.walkable = walkable
        self.gcost = 0
        self.hcost = 0
        self.fcost = 0
        self.previousNode = None

    def setSurrounding(self, b, grid, closed_nodes):
        x, y = self.x, self.y
        if x > 0 and grid[x - 1][y].walkable and [x - 1, y] not in closed_nodes:
            b.append([x - 1, y])
        if (
            x < len(grid) - 1
            and grid[x + 1][y].walkable
            and [x + 1, y] not in closed_nodes
        ):
            b.append([x + 1, y])
        if y > 0 and grid[x][y - 1].walkable and [x, y - 1] not in closed_nodes:
            b.append([x, y - 1])
        if (
            y < len(grid[0]) - 1
            and grid[x][y + 1].walkable
            and [x, y + 1] not in closed_nodes
        ):
            b.append([x, y + 1])

    def setCost(self, end_x, end_y, start_x, start_y):
        self.g_cost = math.sqrt((self.x - start_x) ** 2 + (self.y - start_y) ** 2) * 10
        self.h_cost = math.sqrt((end_x - self.x) ** 2 + (end_y - self.y) ** 2) * 10
        self.f_cost = self.g_cost + self.h_cost
