from src.grid.node import GridNode


class Grid:
    def __init__(
        self,
        rows: int = 30,
        cols: int = 20,
    ):
        self.rows = rows
        self.cols = cols
        self.grid = [[GridNode() for _ in range(cols)] for _ in range(rows)]

    def get_node(self, x: int, y: int) -> GridNode:
        return self.grid[x][y]

    def set_node(self, x: int, y: int, node: GridNode):
        self.grid[x][y] = node

    def __str__(self):
        return "\n".join([" ".join([str(node) for node in row]) for row in self.grid])

    def __getitem__(self, index):
        return self.grid[index]

    def __iter__(self):
        for row in self.grid:
            for node in row:
                yield node


class TemplatedGrid(Grid):
    def __init__(self, template: str):
        """NOTE:
        Create a grid from a template. Requires a template string where
        each character represents a node type.

        Guidelines:
        - Newlines separate rows.
        - Each character represents a node type.
        - Characters can be any of the following:
            - "*": empty node
            - "%": wall node
            - "I": interactive node
        """
        super().__init__()
        self.template = template
        self.grid = self._create_grid_from_template()

    def _create_grid_from_template(self):
        """Create a grid from a template."""
        pass
