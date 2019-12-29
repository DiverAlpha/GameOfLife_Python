""""
Game of Life. Created by DiverAlpha

Rules of the game by John Conway
1. If a cell has less then 2 neighbours then the cell will die by underpopulation
2. If a cell has 2 or 3 neighbours, the cell stays alive
3. If a cell has more then 3 neighbours, the cell dies by overpopulation
4. A cell will get born when it has 3 neighbours

Keys to use:
Escape      Exit the game
Enter       Start a new game
Spade       Pause the game
Right arrow Step the game when it's paused
"""

# Import libs
import pygame
import random
import os
from random import randrange

# Some pygame stuff
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (750,30)
pygame.init()

# Define variables
numCol = 38              # Number of columns - change this to your favorite
numRow = 12              # Number of rows - change this to your favorite
windowSizeX = 1000      # Horizontal windowsize
windowSizeY = 1000      # Vertical winsowsize
generation = 0          # Keep track of evolution
gameStuck = False       # If nothing moves stop the game
debug = True            # Well... Just for fun
pause = False           # Hold the game
step = False            # Step to next generation

# Calculate column width and row height
colWidth = windowSizeX / numCol
rowHeight = windowSizeY / numRow
if colWidth < rowHeight: sizeCell = colWidth
else: sizeCell = rowHeight

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DRKGREEN = (0, 100, 0)
RED = (255, 0, 0)

# Create screen in pygame
my_clock = pygame.time.Clock()
screen = pygame.display.set_mode((windowSizeX, windowSizeY))
pygame.display.set_caption("John Conway's Game of Life")

# Create gameboards
gameOld = [[0] * numCol]                # Create the main game as a 2d array
for rows in range(numRow - 1):
    gameOld.append([0] * numCol)
gameNew = [row[:] for row in gameOld]   # Create gameNew to put results of calculations
gameTemp1 = [row[:] for row in gameOld] # Create gameTemp1 to keep track for progression with last game
gameTemp2 = [row[:] for row in gameOld] # Create gameTemp2 to keep track for progression with game before last game
gameNb = [row[:] for row in gameOld]    # Create gameNb to display number of neighbours counted

# Calculate number of neighbours
def getNeighbours(row, col):
    global numCol, numRow, debug
    count = 0       # Keep track of neighbours which are alive

    # find which cells are neighbours
    if col <= 1: colMin = 0
    else: colMin = col - 1

    if col >= numCol - 1: colMax = col
    else: colMax = col + 1

    if row < 1: rowMin = 0
    else: rowMin = row - 1

    if row >= numRow - 1: rowMax = row
    else: rowMax = row + 1

    # Check neighbours
    for r in range(rowMin, rowMax + 1):
        for c in range(colMin, colMax + 1):
            if gameOld[r][c] == 1:
                count += 1
                if col == c and row == r:
                    count -= 1

    return count

# Fill gameOld with some pseudo random values
def fillGame():
    global numRow, numCol, gameOld, gameNew, gameTemp1, gameTemp2, gameNb

    # Empty games
    gameOld = [[0] * numCol]
    for rows in range(numRow - 1):
        gameOld.append([0] * numCol)
    gameNew = [row[:] for row in gameOld]
    gameTemp1 = [row[:] for row in gameOld]
    gameTemp2 = [row[:] for row in gameOld]
    gameNb = [row[:] for row in gameOld]

    # Decide how many cells to fill
    numCells = round(numRow * numCol * random.uniform(0, 0.3))

    # Fill gameOld with new stuff
    temp = 0
    for i in range(numCells):
        gameOld[randrange(numRow)][randrange(numCol)] = 1
        temp += 1

# Preset to start game with a Glider (minimal size: col = 4, row = 4)
def presetGlider():
    gameOld[1][3] = 1
    gameOld[2][1] = 1
    gameOld[2][3] = 1
    gameOld[3][2] = 1
    gameOld[3][3] = 1

# Preset to start game with a Light weight spaceship (minimal size: col = 6, row = 8)
def presetLwss():
    gameOld[4][1] = 1
    gameOld[4][4] = 1
    gameOld[5][5] = 1
    gameOld[6][1] = 1
    gameOld[6][5] = 1
    gameOld[7][2] = 1
    gameOld[7][3] = 1
    gameOld[7][4] = 1
    gameOld[7][5] = 1

# Preset to start game with a Light weight spaceship (minimal size: col = 38, row = 12)
def presetGliderGun():
    gameOld[1][25] = 1
    gameOld[2][23] = 1
    gameOld[2][25] = 1
    gameOld[3][13] = 1
    gameOld[3][14] = 1
    gameOld[3][21] = 1
    gameOld[3][22] = 1
    gameOld[3][35] = 1
    gameOld[3][36] = 1
    gameOld[4][12] = 1
    gameOld[4][16] = 1
    gameOld[4][21] = 1
    gameOld[4][22] = 1
    gameOld[4][35] = 1
    gameOld[4][36] = 1
    gameOld[5][1] = 1
    gameOld[5][2] = 1
    gameOld[5][11] = 1
    gameOld[5][17] = 1
    gameOld[5][21] = 1
    gameOld[5][22] = 1
    gameOld[6][1] = 1
    gameOld[6][2] = 1
    gameOld[6][11] = 1
    gameOld[6][15] = 1
    gameOld[6][17] = 1
    gameOld[6][18] = 1
    gameOld[6][23] = 1
    gameOld[6][25] = 1
    gameOld[7][11] = 1
    gameOld[7][17] = 1
    gameOld[7][25] = 1
    gameOld[8][12] = 1
    gameOld[8][16] = 1
    gameOld[9][13] = 1
    gameOld[9][14] = 1

# Start game with:
#fillGame()
#presetGlider()
#presetLwss()
presetGliderGun()

# Mainloop
done = True
while done:
    mouseX = 0
    mouseY = 0
    mouseClick = False

    # Check inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:   # Escape, Stop game
                done = False
            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:  # Restart game
                gameStuck = False
                generation = 0
                fillGame()
            elif event.key == pygame.K_SPACE:   # Space, Hold the game
                if pause: pause = False
                else: pause = True
            elif event.key == pygame.K_RIGHT:   # Arrow Right, Step to next generation when on hold
                step = True
        elif event.type == pygame.MOUSEBUTTONDOWN:  # Mouseclick detection
            if event.button == 1:
                mouseClick = True
                mouseX = pygame.mouse.get_pos()[0]
                mouseY = pygame.mouse.get_pos()[1]

    # Calculate Game of Life
    if not pause or step:
        step = False
        if not gameStuck:
            for r in range(numRow):
                for c in range(numCol):
                    neighbours = getNeighbours(r, c)  # Get # of neighbours
                    gameNb[r][c] = neighbours   # for debug purposes

                    if gameOld[r][c] == 1:
                        if neighbours < 2:
                            gameNew[r][c] = 0  # Die by cause of underpopulation
                        elif 2 <= neighbours <= 3:
                            gameNew[r][c] = 1  # Stay alive
                        elif neighbours > 3:
                            gameNew[r][c] = 0  # Die by cause of overpopulation
                    else:
                        if neighbours == 3:
                            gameNew[r][c] = 1  # Get born

            generation += 1

        # Check if  anything is changed
        if gameTemp1 == gameNew:
            gameStuck = True
        if gameTemp2 == gameNew:
            gameStuck = True
        else:
            gameTemp1 = [row[:] for row in gameNew]  # Copy values of gameNew to gameTemp1

        # Save gameNew to gameTemp2
        if generation % 2 == 0: gameTemp2 = [row[:] for row in gameNew]  # Copy values of gameNew to gameTemp2

        # Save gameNew to gameOld
        gameOld = [row[:] for row in gameNew]  # copy values of gameNew to gameOld

    # Fill screen with black
    screen.fill(BLACK)

    # Fill matrix with information from the game
    for r in range(numRow):
        for c in range(numCol):
            if gameOld[r][c] == 1:
                pygame.draw.rect(screen, DRKGREEN, [sizeCell * c, sizeCell * r, sizeCell, sizeCell], 0)

    # Draw lines for matrix
    if numCol < 500 and numRow < 500:
        for c in range(1, numCol):
            pygame.draw.line(screen, BLACK, [sizeCell * c, 0], [sizeCell * c, windowSizeY], 1)
        for r in range(1, numRow):
            pygame.draw.line(screen, BLACK, [0, sizeCell * r], [windowSizeX, sizeCell * r], 1)

    # Write text
    font = pygame.font.SysFont('Calibri', 20, True, False)
    text = font.render("Generation " + str(generation), True, RED)
    screen.blit(text, [50, 50])

    # If there is not enough movement anymore
    if gameStuck:
        pygame.draw.rect(screen, DRKGREEN, [windowSizeX / 2 - 100, windowSizeY / 2 - 50, 200, 100], 0)
        pygame.draw.rect(screen, GREEN, [windowSizeX / 2 - 100, windowSizeY / 2 - 50, 200, 100], 1)
        text = font.render("Play again", True, GREEN)
        screen.blit(text, [windowSizeX / 2 - (text.get_width() / 2), windowSizeY / 2 - (text.get_height() / 2)])
        if mouseClick:
            if windowSizeX / 2 - 100 < mouseX < windowSizeX / 2 + 100:
                if windowSizeY / 2 - 50 < mouseY < windowSizeY / 2 + 50:
                    generation = 0
                    gameStuck = False
                    fillGame()

    # If the game is put on hold
    if pause:
        text = font.render("Game on hold", True, RED)
        screen.blit(text, [windowSizeX / 2 - (text.get_width() / 2), 100])

    pygame.display.flip()
    my_clock.tick(5)

pygame.quit()
