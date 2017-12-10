import numpy
import pygame
import time
from machine import Neural_Network

size = [800, 800]
grid = [20, 20]
tileSize = [size[0]/grid[0], size[1]/grid[1]]
food = [numpy.random.randint(0, 19), numpy.random.randint(0, 19)]
# food = [0, 19]
currentDir = 0

pygame.init()
screen = pygame.display.set_mode((size[0], size[1]))

# time.sleep(0.5)

class Snake:
    def __init__(self, startX, startY):
        self.tiles = [[startX, startY]]

    def display(self):
        for i in range(len(self.tiles)):
            pygame.draw.rect(screen, (255, 255, 255), (self.tiles[i][0] * tileSize[0], self.tiles[i][1] * tileSize[1], tileSize[0], tileSize[1]))

    def move(self, dir):
        if dir == 0:
            if self.tiles[0][0] != 0:
                self.tiles.insert(0, [self.tiles[0][0]-1, self.tiles[0][1]])
            else:
                self.tiles.insert(0, [grid[0]-1, self.tiles[0][1]])

        elif dir == 1:
            if self.tiles[0][0] != grid[0]-1:
                self.tiles.insert(0, [self.tiles[0][0]+1, self.tiles[0][1]])
            else:
                self.tiles.insert(0, [0, self.tiles[0][1]])

        elif dir == 2:
            if self.tiles[0][1] != 0:
                self.tiles.insert(0, [self.tiles[0][0], self.tiles[0][1]-1])
            else:
                self.tiles.insert(0, [self.tiles[0][0], grid[1]-1])

        elif dir == 3:
            if self.tiles[0][1] != grid[1]-1:
                self.tiles.insert(0, [self.tiles[0][0], self.tiles[0][1]+1])
            else:
                self.tiles.insert(0, [self.tiles[0][0], 0])

        self.tiles.__delitem__(len(self.tiles)-1)

    def eat(self):
        if self.tiles[0] == food:
            self.tiles.append(self.tiles[len(self.tiles)-1])
            return True
        return False

snake = Snake(0, 0)

net = Neural_Network((2, 8, 4))

# pygame.key.set_repeat(300)

running = True
while running:

    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

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
            if currentDir != 2:
                currentDir = 3

    snake.display()
    snake.move(currentDir)
    if snake.eat():
        food = [numpy.random.randint(0, 19), numpy.random.randint(0, 19)]

    pygame.draw.rect(screen, (0, 255, 0), (food[0] * tileSize[0], food[1]*tileSize[1], tileSize[0], tileSize[1]))

    pygame.display.update()