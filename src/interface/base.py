import pygame
from sys import exit as sysExit
import math

pygame.init()
winX, winY = 600, 400
SCREEN = pygame.display.set_mode((winX, winY))
CLOCK = pygame.time.Clock()
SCREEN.fill((0,0,0))
pygame.display.set_caption("BrainFlight Simulation Grid")

# Colours
BLACK = (0, 0, 0) # Walkable Nodes
WHITE = (255, 255, 255) # Barrier Nodes
YELLOW = (228, 245, 49) # Final Path Nodes
BLUE = (75, 66, 245) # Start and End Nodes
RED = (245, 102, 66) # Closed Nodes
GREEN = (87, 245, 66) # Open Nodes

# Classes
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
        global grid, closedNodes
        x, y = self.x, self.y
        if x > 0 and grid[x - 1][y].walkable == True and [x - 1, y] not in closedNodes:
            b.append([x - 1, y])
        if x < len(grid) - 1 and grid[x + 1][y].walkable == True and [x + 1, y] not in closedNodes:
            b.append([x + 1, y])
        if y > 0 and grid[x][y - 1].walkable == True and [x, y - 1] not in closedNodes:
            b.append([x, y - 1])
        if y < len(grid[0]) - 1 and grid[x][y + 1].walkable == True and [x, y + 1] not in closedNodes:
            b.append([x, y + 1])

    def setCost(self):
        global endX, endY, startX, startY
        self.gCost = math.sqrt((self.x - startX) ** 2 + (self.y - startY) ** 2) * 10
        self.hCost = math.sqrt((endX - self.x) ** 2 + (endY - self.y) ** 2) * 10
        self.fCost = self.gCost + self.hCost

algorithm = False # When the user presses SPACE to start the algorithm.
pathFound = False # When the Final Node has been found.
leftDrag = False # Detecting Left-click mouse drag to set barrier nodes.
rightDrag = False # Detecting Right-click mouse drag to remove barrier nodes.
nodeSize = 20 # Pixel side-length of each node.
grid = [[Node(x, y) for y in range(winY // nodeSize)] for x in range(winX // nodeSize)]
startX, startY = 4, 5
endX, endY = 24, 17
openNodes = [[startX, startY]]
closedNodes = []
path = []

def setBarrier(x, y):
    global nodeSize, grid, algorithm, startX, startY, endX, endY
    if not algorithm and not pathFound and x < winX and y < winY:
        x = x // nodeSize
        y = y // nodeSize
        if x == startX and y == startY:
            grid[x][y].walkable = True
        else:
            if x == endX and y == endY:
                grid[x][y].walkable = True
            else:
                grid[x][y].walkable = False

def removeBarrier(x, y):
    global nodeSize, grid, algorithm
    if not algorithm and not pathFound and x < winX and y < winY:
        x = x // nodeSize
        y = y // nodeSize
        if grid[x][y].walkable == False:
            grid[x][y].walkable = True

def drawGrid():
    global nodeSize, grid, openNodes, closedNodes, startX, startY, endX, endY
    for n in grid:
        for Node in n:
            if Node.walkable == True:
                rect = pygame.Rect(Node.x * nodeSize, Node.y * nodeSize, nodeSize, nodeSize)
                pygame.draw.rect(SCREEN, BLACK, rect, 0)
            elif Node.walkable == False:
                rect = pygame.Rect(Node.x * nodeSize, Node.y * nodeSize, nodeSize, nodeSize)
                pygame.draw.rect(SCREEN, WHITE, rect, 0)
    for z in closedNodes:
        rect = pygame.Rect(z[0] * nodeSize, z[1] * nodeSize, nodeSize, nodeSize)
        pygame.draw.rect(SCREEN, RED, rect, 0)
    for k in openNodes:
        rect = pygame.Rect(k[0] * nodeSize, k[1] * nodeSize, nodeSize, nodeSize)
        pygame.draw.rect(SCREEN, GREEN, rect, 0)
    for x in path:
        rect = pygame.Rect(x[0] * nodeSize, x[1] * nodeSize, nodeSize, nodeSize)
        pygame.draw.rect(SCREEN, YELLOW, rect, 0)
    rect = pygame.Rect(startX * nodeSize, startY * nodeSize, nodeSize, nodeSize)
    pygame.draw.rect(SCREEN, BLUE, rect, 0)
    rect = pygame.Rect(endX * nodeSize, endY * nodeSize, nodeSize, nodeSize)
    pygame.draw.rect(SCREEN, BLUE, rect, 0)

def findPath():
    global startX, startY, endX, endY, grid
    currentX, currentY = endX, endY
    while True:
        previousNode = grid[currentX][currentY].previousNode
        previousX, previousY = previousNode.x, previousNode.y
        path.append([previousX, previousY])
        currentX, currentY = previousX, previousY
        if currentX == startX and currentY == startY:
            break

def game_loop():
    """Main game loop for the simulation."""
    global algorithm, openNodes, closedNodes, path, pathFound, startX, startY, endX, endY, leftDrag, rightDrag
    run = True

    print("-------- Simulation Started --------")

    while run:
        # Event Detection
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_SPACE: # Press "SPACE" key to start the Algorithm.
                    if not algorithm:
                        algorithm = True
                        print("-------- Simulation Running --------")
                elif event.key == pygame.K_ESCAPE: # Press "ESC" key to stop the Algorithm.
                    run = False
                elif event.key == pygame.K_1:
                    if not algorithm:
                        startX, startY = pygame.mouse.get_pos()[0] // nodeSize, pygame.mouse.get_pos()[1] // nodeSize
                        openNodes = [[startX, startY]]
                        grid[startX][startY].walkable = True
                elif event.key == pygame.K_2:
                    if not algorithm:
                        endX, endY = pygame.mouse.get_pos()[0] // nodeSize, pygame.mouse.get_pos()[1] // nodeSize
                        grid[endX][endY].walkable = True
            elif event.type == pygame.MOUSEBUTTONDOWN: # Drag mouse while holding left click to add barriers.
                if event.button == 1:    
                    leftDrag = True
                    mouseX, mouseY = event.pos
                    setBarrier(mouseX, mouseY)
                if event.button == 3:
                    rightDrag = True
                    mouseX, mouseY = event.pos
                    removeBarrier(mouseX, mouseY)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    leftDrag = False
                if event.button == 3:
                    rightDrag = False
            elif event.type == pygame.MOUSEMOTION:
                if leftDrag:
                    mouseX, mouseY = event.pos
                    setBarrier(mouseX, mouseY)
                elif rightDrag:
                    mouseX, mouseY = event.pos
                    removeBarrier(mouseX, mouseY)

        drawGrid()

        if algorithm and not pathFound:
            try:
                # Find the Current Node (Open Node with smallest fcost).
                current = openNodes[0]
                for i in openNodes:
                    if i != [startX, startY]:
                        grid[i[0]][i[1]].setCost()
                    if grid[i[0]][i[1]].fcost < grid[current[0]][current[1]].fcost:
                        current = i

                # Add Current Node to Closed Nodes.
                closedNodes.append(current)
                del openNodes[openNodes.index(current)]
                #print(current)
                
                # End Node found.
                if current == [endX, endY] or [endX, endY] in closedNodes:
                    findPath()
                    pathFound = True
                
                # Add Neighbours to Open Nodes.
                neighbours = []
                grid[current[0]][current[1]].setSurrounding(neighbours)
                for i in neighbours:
                    grid[i[0]][i[1]].previousNode = grid[current[0]][current[1]]
                    if i not in openNodes:
                        openNodes.append(i)

                pygame.time.delay(5)
            except:
                pass
        pygame.display.update()

    if not run:
        print("-------- Simulation Finished --------")
        pygame.quit()
        sysExit()
