from typing import Tuple

import pygame

from src.grid.grid import Grid
from src.constants import COLORS, MAX_WINDOW_WIDTH, MAX_WINDOW_HEIGHT


class GameInterface:
    def __init__(
        self, grid: Grid, starting_coords: Tuple[int, int] = (1, 1), node_size: int = 20
    ):
        self.window_width = grid.rows * node_size
        self.window_height = grid.cols * node_size

        if (
            self.window_width > MAX_WINDOW_WIDTH
            or self.window_height > MAX_WINDOW_HEIGHT
        ):
            raise ValueError("Grid dimensions exceed maximum window dimensions.")

        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        self.clock = pygame.time.Clock()

        self.grid = grid
        self.node_size = node_size
        self.start = starting_coords

    def setBarrier(self, mouse_x: int, mouse_y: int):
        if mouse_x < self.window_width and mouse_y < self.window_height:
            x = mouse_x // self.node_size
            y = mouse_y // self.node_size

            if x == self.start[0] and y == self.start[1]:
                self.grid[x][y].walkable = True
            else:
                self.grid[x][y].walkable = False

    def removeBarrier(self, mouse_x: int, mouse_y: int):
        if mouse_x < self.window_width and mouse_y < self.window_height:
            x = mouse_x // self.node_size
            y = mouse_y // self.node_size

            if not self.grid[x][y].walkable:
                self.grid[x][y].walkable = True

    def drawGrid(self):
        screen = self.screen
        node_size = self.node_size

        for x in range(len(self.grid.grid)):
            for y in range(len(self.grid.grid[x])):
                node = self.grid.grid[x][y]
                if node.walkable:
                    rect = pygame.Rect(
                        x * node_size, y * node_size, node_size, node_size
                    )
                    pygame.draw.rect(screen, COLORS["black"], rect, 0)
                else:
                    rect = pygame.Rect(
                        x * self.node_size, y * node_size, node_size, node_size
                    )
                    pygame.draw.rect(screen, COLORS["white"], rect, 0)

        # Robot Node
        rect = pygame.Rect(
            self.start[0] * node_size, self.start[1] * node_size, node_size, node_size
        )
        pygame.draw.rect(screen, COLORS["blue"], rect, 0)

    def run(self):
        """Main game loop for the simulation."""
        self.screen.fill((0, 0, 0))
        pygame.display.set_caption("BrainFlight Simulation Grid")

        left_drag = False  # Detecting Left-click mouse drag to set barrier nodes.
        right_drag = False  # Detecting Right-click mouse drag to remove barrier nodes.

        run = True

        print("-------- Simulation Started --------")

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # NOTE: Press "SPACE" key to start the episode.
                        print("-------- Simulation Running --------")
                    elif event.key == pygame.K_ESCAPE:
                        # NOTE: Press "ESC" key to stop the episode.
                        run = False
                    elif event.key == pygame.K_1:
                        self.start = (
                            pygame.mouse.get_pos()[0] // self.node_size,
                            pygame.mouse.get_pos()[1] // self.node_size,
                        )
                        self.grid[self.start[0]][self.start[1]].walkable = True
                elif (
                    event.type == pygame.MOUSEBUTTONDOWN
                ):  # NOTE: Drag mouse while holding left click to add barriers.
                    if event.button == 1:
                        left_drag = True
                        mouse_x, mouse_y = event.pos
                        self.setBarrier(mouse_x, mouse_y)
                    if event.button == 3:
                        right_drag = True
                        mouse_x, mouse_y = event.pos
                        self.removeBarrier(mouse_x, mouse_y)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        left_drag = False
                    if event.button == 3:
                        right_drag = False
                elif event.type == pygame.MOUSEMOTION:
                    if left_drag:
                        mouseX, mouseY = event.pos
                        self.setBarrier(mouseX, mouseY)
                    elif right_drag:
                        mouseX, mouseY = event.pos
                        self.removeBarrier(mouseX, mouseY)

            self.drawGrid()
            pygame.display.update()

        if not run:
            print("-------- Simulation Finished --------")
            pygame.quit()
