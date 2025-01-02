import sys
import math

import pygame

# Colours
BLACK = (0, 0, 0)  # Walkable Nodes
WHITE = (255, 255, 255)  # Barrier Nodes
YELLOW = (228, 245, 49)  # Final Path Nodes
BLUE = (75, 66, 245)  # Start and End Nodes
RED = (245, 102, 66)  # Closed Nodes
GREEN = (87, 245, 66)  # Open Nodes

# Window Dimensions
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
screen.fill((0, 0, 0))
pygame.display.set_caption("BrainFlight Simulation Grid")


class Node(object):
    def __init__(self, x, y, walkable=True):
        self.x = x
        self.y = y
        self.walkable = walkable
        self.gcost = 0
        self.hcost = 0
        self.fcost = 0
        self.previousNode = None

    def setSurrounding(self, b):
        global grid, closed_nodes
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

    def setCost(self):
        global end_x, end_y, start_x, start_y
        self.g_cost = math.sqrt((self.x - start_x) ** 2 + (self.y - start_y) ** 2) * 10
        self.h_cost = math.sqrt((end_x - self.x) ** 2 + (end_y - self.y) ** 2) * 10
        self.f_cost = self.g_cost + self.h_cost


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


def drawGrid():
    global node_size, grid, openNodes, closed_nodes, start_x, start_y, end_x, end_y
    for n in grid:
        for Node in n:
            if Node.walkable:
                rect = pygame.Rect(
                    Node.x * node_size, Node.y * node_size, node_size, node_size
                )
                pygame.draw.rect(screen, BLACK, rect, 0)
            else:
                rect = pygame.Rect(
                    Node.x * node_size, Node.y * node_size, node_size, node_size
                )
                pygame.draw.rect(screen, WHITE, rect, 0)
    for z in closed_nodes:
        rect = pygame.Rect(z[0] * node_size, z[1] * node_size, node_size, node_size)
        pygame.draw.rect(screen, RED, rect, 0)
    for k in openNodes:
        rect = pygame.Rect(k[0] * node_size, k[1] * node_size, node_size, node_size)
        pygame.draw.rect(screen, GREEN, rect, 0)
    for x in path:
        rect = pygame.Rect(x[0] * node_size, x[1] * node_size, node_size, node_size)
        pygame.draw.rect(screen, YELLOW, rect, 0)
    rect = pygame.Rect(start_x * node_size, start_y * node_size, node_size, node_size)
    pygame.draw.rect(screen, BLUE, rect, 0)
    rect = pygame.Rect(end_x * node_size, end_y * node_size, node_size, node_size)
    pygame.draw.rect(screen, BLUE, rect, 0)


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
                ):  # Press "SPACE" key to start the Algorithm.
                    if not algorithm:
                        algorithm = True
                        print("-------- Simulation Running --------")
                elif (
                    event.key == pygame.K_ESCAPE
                ):  # Press "ESC" key to stop the Algorithm.
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
            ):  # Drag mouse while holding left click to add barriers.
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

        drawGrid()

        if algorithm and not path_found:
            try:
                # Find the Current Node (Open Node with smallest fcost).
                current = openNodes[0]
                for i in openNodes:
                    if i != [start_x, start_y]:
                        grid[i[0]][i[1]].setCost()
                    if grid[i[0]][i[1]].fcost < grid[current[0]][current[1]].fcost:
                        current = i

                # Add Current Node to Closed Nodes.
                closed_nodes.append(current)
                del openNodes[openNodes.index(current)]
                # print(current)

                # End Node found.
                if current == [end_x, end_y] or [end_x, end_y] in closed_nodes:
                    findPath()
                    path_found = True

                # Add Neighbours to Open Nodes.
                neighbours = []
                grid[current[0]][current[1]].setSurrounding(neighbours)
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
