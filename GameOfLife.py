""""
Game of Life. Created by DiverAlpha

Rules of the game by John Conway
1. If a cell has less then 2 neighbours then the cell will die by underpopulation
2. If a cell has 2 or 3 neighbours, the cell stays alive
3. If a cell has more then 3 neighbours, the cell dies by overpopulation
4. A cell will get born when it has 3 neighbours
"""

# Import libs
import pygame
import random
from random import randrange
pygame.init()

# Define variables
numCol = 16 # number of columns
numRow = 16 # number of rows
windowSizeX = 800
windowSizeY = 800
screenCentreX = windowSizeX // 2
screenCentreY = windowSizeY // 2
generation = 0
gameStuck = False
debug = True

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DRKGREEN = (0, 100, 0)
RED = (255, 0, 0)

# Create screen in pygame
my_clock = pygame.time.Clock()
screen = pygame.display.set_mode((windowSizeX, windowSizeY))
pygame.display.set_caption("Game of Life")

# Create gameboard
gameOld = [[0] * numCol]
for rows in range(numRow - 1):
    gameOld.append([0] * numCol)
gameNew = [row[:] for row in gameOld] # create gameNew to put results of calculations
gameTemp1 = [row[:] for row in gameOld] # create gameTemp1 to keep track for progression with last game
gameTemp2 = [row[:] for row in gameOld] # create gameTemp2 to keep track for progression with game before last game
gameNb = [row[:] for row in gameOld] # create gameNb to display number of neighbours counted

# Calculate number of neighbours
def getNeighbours(row, col):
    global numCol, numRow, debug
    count = 0

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

# Fill in some values gameOld
def fillGame():
    global numRow, numCol
    numCells = round(numRow * numCol * random.uniform(0, 0.4))

    temp = 0
    for i in range(numCells):
        gameOld[randrange(numRow)][randrange(numCol)] = 1
        temp += 1

def preset32():
    gameOld[1][3] = 1
    gameOld[2][1] = 1
    gameOld[2][3] = 1
    gameOld[3][2] = 1
    gameOld[3][3] = 1

#fillGame()
preset32()

#print("gameOld")
#for i in range(numRow): # Print for debug
#    print(gameOld[i])
#print("")

# Mainloop
done = True
while done:
    mouseX = 0
    mouseY = 0
    mouseClick = False

    # Check events (inputs)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Escape, Stop game
                done = False
            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:  # Restart game
                gameStuck = False
                generation = 0
                fillGame()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouseClick = True
                mouseX = pygame.mouse.get_pos()[0]
                mouseY = pygame.mouse.get_pos()[1]

    # Calculate column width and row height
    colWidth = windowSizeX / numCol
    rowHeight = windowSizeY / numRow

    # Calculate Game of Life
    if not gameStuck:
        for r in range(numRow):
            for c in range(numCol):
                neighbours = getNeighbours(r, c)  # Get # of neighbours
                gameNb[r][c] = neighbours

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

    gameOld = [row[:] for row in gameNew]  # copy values of gameNew to gameOld

    # Fill screen with black
    screen.fill(BLACK)

    # Fill matrix with information from the game
    for r in range(numRow):
        for c in range(numCol):
            if gameOld[r][c] == 1:
                pygame.draw.rect(screen, DRKGREEN, [colWidth * c, rowHeight * r, colWidth, rowHeight], 0)

    # Draw lines for matrix
    for c in range(1, numCol):
        pygame.draw.line(screen, BLACK, [colWidth * c, 0], [colWidth * c, windowSizeY], 1)
    for r in range(1, numRow):
        pygame.draw.line(screen, BLACK, [0, rowHeight * r], [windowSizeX, rowHeight * r], 1)

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

    pygame.display.flip()
    my_clock.tick(2)

pygame.quit()