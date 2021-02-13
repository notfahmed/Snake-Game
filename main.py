import pygame
import sys
import random
from pygame.math import Vector2 as Vector


class Apple:
    def __init__(self):
        self.x = random.randint(0, cellNumber - 1)
        self.y = random.randint(0, cellNumber - 1)
        self.pos = Vector(self.x, self.y)

    def draw_apple(self):
        xPos = int(self.pos.x * cellSize)
        yPos = int(self.pos.y * cellSize)
        appleRect = pygame.Rect(xPos, yPos, cellSize, cellSize)
        pygame.draw.rect(screen, (255, 8, 0), appleRect)


class Snake:
    def __init__(self):
        self.body = [Vector(5, 10), Vector(6, 10), Vector(7, 10)]

    def draw_snake(self):
        for block in self.body:
            xPos = int(block.x * cellSize)
            yPos = int(block.y * cellSize)
            snakeRect = pygame.Rect(xPos, yPos, cellSize, cellSize)


pygame.init()
cellSize = 40
cellNumber = 20
screen = pygame.display.set_mode((cellNumber * cellSize, cellNumber * cellSize))
clock = pygame.time.Clock()

apple = Apple()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((175, 215, 70))
    apple.draw_apple()
    pygame.display.update()
    clock.tick(144)
