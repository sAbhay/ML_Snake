import numpy
import pygame
from pygame.locals import *
from machine import Neural_Network

def distance(p0, p1):
    return numpy.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

displaying = True

size = [100, 100]
grid = [10, 10]
tileSize = [size[0]/grid[0], size[1]/grid[1]]

food = [numpy.random.randint(0, grid[0]-1), numpy.random.randint(0, grid[1]-1)]

addedTime = 5 * grid[0]

tiles = []

for i in range(0, grid[0]):
    tiles.append([])
    for j in range(0, grid[1]):
        tiles[i].append(0)

tiles[food[0]][food[1]] = 3

currentDir = 0

pygame.init()

flags = DOUBLEBUF
screen = pygame.display.set_mode((size[0], size[1]), flags)
screen.set_alpha(None)

timer = addedTime
score = 0
highScore = -addedTime
length = 1
longestLength = 1

gen = 0
iteration = 0

died = False

class Snake:
    def __init__(self, startX, startY):
        self.tiles = [[startX, startY]]
        self.prevLast = self.tiles[len(self.tiles)-1]

    def display(self):
        for i in range(len(self.tiles)-1):
            pygame.draw.rect(screen, (255, 255, 255), (self.tiles[i+1][0] * tileSize[0], self.tiles[i+1][1] * tileSize[1], tileSize[0], tileSize[1]))
        pygame.draw.rect(screen, (255, 0, 0), (self.tiles[0][0] * tileSize[0], self.tiles[0][1] * tileSize[1], tileSize[0], tileSize[1]))

    def updateTiles(self):
        for i in self.tiles:
            tiles[int(i[0])][int(i[1])] = 1
        tiles[int(self.tiles[0][0])][int(self.tiles[0][1])] = 2

    def move(self, dir):
        self.prevLast = self.tiles[len(self.tiles) - 1]

        if dir == 0:
            self.tiles.insert(0, [(self.tiles[0][0]-1) % grid[0], self.tiles[0][1]])

        elif dir == 1:
            self.tiles.insert(0, [(self.tiles[0][0]+1) % grid[0], self.tiles[0][1]])

        elif dir == 2:
            self.tiles.insert(0, [self.tiles[0][0], (self.tiles[0][1]-1) % grid[1]])

        elif dir == 3:
            self.tiles.insert(0, [self.tiles[0][0], (self.tiles[0][1]+1) % grid[1]])

        self.tiles.__delitem__(len(self.tiles)-1)

    def eat(self):
        if self.tiles[0][0] == food[0] and self.tiles[0][1] == food[1]:
            self.tiles.append([self.prevLast[0], self.prevLast[1]])
            return True
        return False

    def die(self):
        if self.tiles.__len__() > 1:
            for i in range(1, len(self.tiles)):
                if self.tiles[i] == self.tiles[0]:
                    return True
        return False

    def clearSnake(self):
        self.tiles.clear()
        self.tiles.append([0, 0])

    def checkObstacles(self):
        output = []

        if any(t[0] == ((self.tiles[0][0]-1)%grid[0]) for t in self.tiles) and any(t[1] == self.tiles[0][1] for t in self.tiles):
            output.append(1)
        else:
            output.append(0)

        if any(t[0] == ((self.tiles[0][0]+1)%grid[0]) for t in self.tiles) and any(t[1] == self.tiles[0][1] for t in self.tiles):
            output.append(1)
        else:
            output.append(0)

        if any(t[1] == ((self.tiles[0][1]-1)%grid[1]) for t in self.tiles) and any(t[0] == self.tiles[0][0] for t in self.tiles):
            output.append(1)
        else:
            output.append(0)

        if any(t[1] == ((self.tiles[0][1]+1)%grid[1]) for t in self.tiles) and any(t[0] == self.tiles[0][0] for t in self.tiles):
            output.append(1)
        else:
            output.append(0)

        return output

snake = Snake(grid[0]/2, grid[1]/2)

net = Neural_Network([3*grid[0]*grid[1], 4])

running = True
while running:

    if displaying:
        screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if currentDir != 1:
                    currentDir = 0

            elif event.key == pygame.K_RIGHT:
                if currentDir != 0:
                    currentDir = 1

            elif event.key == pygame.K_UP:
                if currentDir != 3:
                    currentDir = 2

            elif event.key == pygame.K_DOWN:
                if currentDir != 2:
                    currentDir = 3

        if event.type == pygame.MOUSEBUTTONDOWN:
            # displaying = True
            pass

    # netInput = snake.checkObstacles()
    #
    # angle = numpy.arctan2((snake.tiles[0][1]*tileSize[1]) - (food[currentFood][1]*tileSize[1]), (snake.tiles[0][0]*tileSize[0]) - (food[currentFood][0]*tileSize[0]))
    # netInput.append(angle)
    #
    # dist = distance(snake.tiles[0], food[currentFood])
    # netInput.append(dist)

    snake.updateTiles()

    netInput = []

    for i in range(0, len(tiles)):
        for j in range(0, len(tiles[i])):
            temp = tiles[int((i + snake.tiles[0][0]) % grid[0])][int((j + snake.tiles[0][1]) % grid[1])]
            if temp >= 2:
                temp -= 1
            for k in range(0, 3):
                if temp == k:
                    netInput.append(1)
                else:
                    netInput.append(0)

    currentDir = net.getAnswer(netInput)

    snake.move(currentDir)

    timer -= 1
    score -= 1/snake.tiles.__len__()

    if snake.eat():
        food = [numpy.random.randint(0, grid[0]-1), numpy.random.randint(0, grid[1]-1)]
        length += 1

        notDone = True
        while notDone:
            if any(food == t for t in snake.tiles):
                food = [numpy.random.randint(0, grid[0]-1), numpy.random.randint(0, grid[1]-1)]
                notDone = True
            else:
                notDone = False

        tiles[food[0]][food[1]] = 3

        score += 1000
        timer += addedTime

    if displaying:
        snake.display()

    if snake.die() or timer <= 0:
        if snake.die():
            score -= 200
            died = True
            snake.clearSnake()
        else:
            died = False

        if length > longestLength:
            longestLength = length
        
        if score > highScore:
            highScore = score
            net.bestWB()
            variantNum = 0
            with open("wb.txt", 'w') as text:
                # text.write(str(highScore))
                text.write(str(net.wb))
                text.close()

            gen += 1
            iteration = 0

        print("Gen: " + str(gen) + ", Iteration: " + str(iteration) + ", High Score: " + str(int(highScore)) + ", Score: "
              + str(int(score)) + ", Longest Length: " + str(longestLength) + ", Length: " + str(length) + ", Died: " + str(died))

        net.neat(50)
        score = 0
        snake.clearSnake()
        snake.__init__(grid[0]/2, grid[1]/2)
        timer = addedTime
        iteration += 1
        length = 1
        tiles[food[0]][food[1]] = 3

    if len(snake.tiles) != length:
        running = False

    if displaying:
        pygame.draw.rect(screen, (0, 255, 0), (food[0] * tileSize[0], food[1]*tileSize[1], tileSize[0], tileSize[1]))

        pygame.display.update()

pygame.quit()