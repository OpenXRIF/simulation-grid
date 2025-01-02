import sys

import pygame

from src.grid.node import Node
from src.constants import COLORS

# Window Dimensions
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400

algorithm = False  # When the user presses SPACE to start the algorithm.
path_found = False  # When the Final Node has been found.
left_drag = False  # Detecting Left-click mouse drag to set barrier nodes.
right_drag = False  # Detecting Right-click mouse drag to remove barrier nodes.
node_size = 20  # Pixel side-length of each node.
grid = [
    [Node(x, y) for y in range(WINDOW_HEIGHT // node_size)]
    for x in range(WINDOW_WIDTH // node_size)
]
start_x, start_y = 4, 5
end_x, end_y = 24, 17
openNodes = [[start_x, start_y]]
closed_nodes = []
path = []


def setBarrier(x, y):
    global node_size, grid, algorithm, start_x, start_y, end_x, end_y
    if not algorithm and not path_found and x < WINDOW_WIDTH and y < WINDOW_HEIGHT:
        x = x // node_size
        y = y // node_size
        if x == start_x and y == start_y:
            grid[x][y].walkable = True
        else:
            if x == end_x and y == end_y:
                grid[x][y].walkable = True
            else:
                grid[x][y].walkable = False


def removeBarrier(x, y):
    global node_size, grid, algorithm
    if not algorithm and not path_found and x < WINDOW_WIDTH and y < WINDOW_HEIGHT:
        x = x // node_size
        y = y // node_size
        if not grid[x][y].walkable:
            grid[x][y].walkable = True


def drawGrid(screen: pygame.Surface):
    global node_size, grid, openNodes, closed_nodes, start_x, start_y, end_x, end_y
    for n in grid:
        for node in n:
            if node.walkable:
                rect = pygame.Rect(
                    node.x * node_size, node.y * node_size, node_size, node_size
                )
                pygame.draw.rect(screen, COLORS["black"], rect, 0)
            else:
                rect = pygame.Rect(
                    node.x * node_size, node.y * node_size, node_size, node_size
                )
                pygame.draw.rect(screen, COLORS["white"], rect, 0)
    for z in closed_nodes:
        rect = pygame.Rect(z[0] * node_size, z[1] * node_size, node_size, node_size)
        pygame.draw.rect(screen, COLORS["red"], rect, 0)
    for k in openNodes:
        rect = pygame.Rect(k[0] * node_size, k[1] * node_size, node_size, node_size)
        pygame.draw.rect(screen, COLORS["green"], rect, 0)
    for x in path:
        rect = pygame.Rect(x[0] * node_size, x[1] * node_size, node_size, node_size)
        pygame.draw.rect(screen, COLORS["yellow"], rect, 0)
    rect = pygame.Rect(start_x * node_size, start_y * node_size, node_size, node_size)
    pygame.draw.rect(screen, COLORS["blue"], rect, 0)
    rect = pygame.Rect(end_x * node_size, end_y * node_size, node_size, node_size)
    pygame.draw.rect(screen, COLORS["blue"], rect, 0)


def findPath():
    global start_x, start_y, end_x, end_y, grid
    currentX, currentY = end_x, end_y
    while True:
        previousNode = grid[currentX][currentY].previousNode
        previousX, previousY = previousNode.x, previousNode.y
        path.append([previousX, previousY])
        currentX, currentY = previousX, previousY
        if currentX == start_x and currentY == start_y:
            break


def game_loop():
    """Main game loop for the simulation."""
    global \
        algorithm, \
        openNodes, \
        closed_nodes, \
        path, \
        path_found, \
        start_x, \
        start_y, \
        end_x, \
        end_y, \
        left_drag, \
        right_drag

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()  # noqa: F841
    screen.fill((0, 0, 0))
    pygame.display.set_caption("BrainFlight Simulation Grid")

    run = True

    print("-------- Simulation Started --------")

    while run:
        # Event Detection
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if (
                    event.key == pygame.K_SPACE
                ):  # NOTE: Press "SPACE" key to start the Algorithm.
                    if not algorithm:
                        algorithm = True
                        print("-------- Simulation Running --------")
                elif (
                    event.key == pygame.K_ESCAPE
                ):  # NOTE: Press "ESC" key to stop the Algorithm.
                    run = False
                elif event.key == pygame.K_1:
                    if not algorithm:
                        start_x, start_y = (
                            pygame.mouse.get_pos()[0] // node_size,
                            pygame.mouse.get_pos()[1] // node_size,
                        )
                        openNodes = [[start_x, start_y]]
                        grid[start_x][start_y].walkable = True
                elif event.key == pygame.K_2:
                    if not algorithm:
                        end_x, end_y = (
                            pygame.mouse.get_pos()[0] // node_size,
                            pygame.mouse.get_pos()[1] // node_size,
                        )
                        grid[end_x][end_y].walkable = True
            elif (
                event.type == pygame.MOUSEBUTTONDOWN
            ):  # NOTE: Drag mouse while holding left click to add barriers.
                if event.button == 1:
                    left_drag = True
                    mouseX, mouseY = event.pos
                    setBarrier(mouseX, mouseY)
                if event.button == 3:
                    right_drag = True
                    mouseX, mouseY = event.pos
                    removeBarrier(mouseX, mouseY)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    left_drag = False
                if event.button == 3:
                    right_drag = False
            elif event.type == pygame.MOUSEMOTION:
                if left_drag:
                    mouseX, mouseY = event.pos
                    setBarrier(mouseX, mouseY)
                elif right_drag:
                    mouseX, mouseY = event.pos
                    removeBarrier(mouseX, mouseY)

        drawGrid(screen)

        if algorithm and not path_found:
            try:
                # Find the Current Node (Open Node with smallest fcost).
                current = openNodes[0]
                for i in openNodes:
                    if i != [start_x, start_y]:
                        grid[i[0]][i[1]].setCost(end_x, end_y, start_x, start_y)
                    if grid[i[0]][i[1]].fcost < grid[current[0]][current[1]].fcost:
                        current = i

                # Add Current Node to Closed Nodes.
                closed_nodes.append(current)
                del openNodes[openNodes.index(current)]

                # End Node found.
                if current == [end_x, end_y] or [end_x, end_y] in closed_nodes:
                    findPath()
                    path_found = True

                # Add Neighbours to Open Nodes.
                neighbours = []
                grid[current[0]][current[1]].setSurrounding(
                    neighbours, grid, closed_nodes
                )
                for i in neighbours:
                    grid[i[0]][i[1]].previousNode = grid[current[0]][current[1]]
                    if i not in openNodes:
                        openNodes.append(i)

                pygame.time.delay(5)
            except Exception as e:
                print(f"Error: {e}")
        pygame.display.update()

    if not run:
        print("-------- Simulation Finished --------")
        pygame.quit()
        sys.exit()
