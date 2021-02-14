import pygame
import sys
import random
from pygame.math import Vector2 as Vector


class Apple:
    def __init__(self):
        self.randomize()

    def draw_apple(self):
        xPos = int(self.pos.x * cellSize)
        yPos = int(self.pos.y * cellSize)
        appleRect = pygame.Rect(xPos, yPos, cellSize, cellSize)
        screen.blit(apple, appleRect)

    def randomize(self):
        self.x = random.randint(0, cellNumber - 1)
        self.y = random.randint(0, cellNumber - 1)
        self.pos = Vector(self.x, self.y)


class Snake:
    def __init__(self):
        self.body = [Vector(7, 10), Vector(6, 10), Vector(5, 10)]
        self.direction = Vector(0, 0)
        self.newBlock = False

        self.headUp = pygame.image.load('Images/head_up.png').convert_alpha()
        self.headDown = pygame.image.load('Images/head_down.png').convert_alpha()
        self.headRight = pygame.image.load('Images/head_right.png').convert_alpha()
        self.headLeft = pygame.image.load('Images/head_left.png').convert_alpha()

        self.tailUp = pygame.image.load('Images/tail_up.png').convert_alpha()
        self.tailDown = pygame.image.load('Images/tail_down.png').convert_alpha()
        self.tailRight = pygame.image.load('Images/tail_right.png').convert_alpha()
        self.tailLeft = pygame.image.load('Images/tail_left.png').convert_alpha()

        self.bodyVertical = pygame.image.load('Images/body_vertical.png').convert_alpha()
        self.bodyHorizontal = pygame.image.load('Images/body_horizontal.png').convert_alpha()

        self.bodyTR = pygame.image.load('Images/body_tr.png').convert_alpha()
        self.bodyTL = pygame.image.load('Images/body_tl.png').convert_alpha()
        self.bodyBR = pygame.image.load('Images/body_br.png').convert_alpha()
        self.bodyBL = pygame.image.load('Images/body_bl.png').convert_alpha()

        self.crunchSound = pygame.mixer.Sound('Sound/crunch.wav')
        self.moveSound = pygame.mixer.Sound('Sound/move.wav')
        self.endSound = pygame.mixer.Sound('Sound/ending.wav')

        self.crunchSound.set_volume(0.1)
        self.moveSound.set_volume(0.1)
        self.endSound.set_volume(0.05)

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for i, block in enumerate(self.body):
            xPos = int(block.x * cellSize)
            yPos = int(block.y * cellSize)
            snakeRect = pygame.Rect(xPos, yPos, cellSize, cellSize)

            if i == 0:
                screen.blit(self.head, snakeRect)
            elif i == len(self.body) - 1:
                screen.blit(self.tail, snakeRect)
            else:
                previousBlock = self.body[i + 1] - block
                nextBlock = self.body[i - 1] - block
                if previousBlock.x == nextBlock.x:
                    screen.blit(self.bodyVertical, snakeRect)
                elif previousBlock.y == nextBlock.y:
                    screen.blit(self.bodyHorizontal, snakeRect)
                else:
                    if previousBlock.x == -1 and nextBlock.y == -1 or previousBlock.y == -1 and nextBlock.x == -1:
                        screen.blit(self.bodyTL, snakeRect)
                    elif previousBlock.x == -1 and nextBlock.y == 1 or previousBlock.y == 1 and nextBlock.x == -1:
                        screen.blit(self.bodyBL, snakeRect)
                    if previousBlock.x == 1 and nextBlock.y == -1 or previousBlock.y == -1 and nextBlock.x == 1:
                        screen.blit(self.bodyTR, snakeRect)
                    if previousBlock.x == 1 and nextBlock.y == 1 or previousBlock.y == 1 and nextBlock.x == 1:
                        screen.blit(self.bodyBR, snakeRect)

    def move_snake(self):
        if self.newBlock:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.newBlock = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.newBlock = True

    def update_head_graphics(self):
        head_rotation = self.body[1] - self.body[0]
        if head_rotation == Vector(1, 0):
            self.head = self.headLeft
        elif head_rotation == Vector(-1, 0):
            self.head = self.headRight
        elif head_rotation == Vector(0, 1):
            self.head = self.headUp
        elif head_rotation == Vector(0, -1):
            self.head = self.headDown

    def update_tail_graphics(self):
        tail_rotation = self.body[-2] - self.body[-1]
        if tail_rotation == Vector(1, 0):
            self.tail = self.tailLeft
        elif tail_rotation == Vector(-1, 0):
            self.tail = self.tailRight
        elif tail_rotation == Vector(0, 1):
            self.tail = self.tailUp
        elif tail_rotation == Vector(0, -1):
            self.tail = self.tailDown

    def play_crunch_sound(self):
        self.crunchSound.play()

    def play_move_sound(self):
        self.moveSound.play()

    def play_ending_sound(self):
        self.endSound.play()

    def reset(self):
        self.body = [Vector(7, 10), Vector(6, 10), Vector(5, 10)]


class Game:
    def __init__(self):
        self.apple = Apple()
        self.snake = Snake()
        self.grassColor = (167, 209, 61)

    def update(self):
        self.snake.move_snake()
        self.check_eat()
        self.check_collision()

    def draw_elements(self):
        self.draw_grass()
        self.apple.draw_apple()
        self.snake.draw_snake()
        self.draw_score()

    def move_up(self):
        if self.snake.direction.y != 1 and self.snake.direction.y != -1:
            self.snake.direction = Vector(0, -1)
            self.snake.play_move_sound()

    def move_down(self):
        if self.snake.direction.y != -1 and self.snake.direction.y != 1:
            self.snake.direction = Vector(0, 1)
            self.snake.play_move_sound()

    def move_right(self):
        if self.snake.direction.x != -1 and self.snake.direction.x != 1:
            self.snake.direction = Vector(1, 0)
            self.snake.play_move_sound()

    def move_left(self):
        if self.snake.direction.x != 1 and self.snake.direction.x != -1:
            self.snake.direction = Vector(-1, 0)
            self.snake.play_move_sound()

    def check_eat(self):
        if self.apple.pos == self.snake.body[0]:
            self.apple.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()

        for block in self.snake.body[1:]:
            if block == self.apple.pos:
                self.apple.randomize()

    def check_collision(self):
        if not 0 <= self.snake.body[0].x < cellNumber or not 0 <= self.snake.body[0].y < cellNumber:
            self.snake.play_ending_sound()
            self.end_game()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.end_game()

    def draw_grass(self):
        for row in range(cellNumber):
            if row % 2 == 0:
                for col in range(cellNumber):
                    if col % 2 == 0:
                        grassRect = pygame.Rect(col * cellSize, row * cellSize, cellSize, cellSize)
                        pygame.draw.rect(screen, self.grassColor, grassRect)
            else:
                for col in range(cellNumber):
                    if col % 2 != 0:
                        grassRect = pygame.Rect(col * cellSize, row * cellSize, cellSize, cellSize)
                        pygame.draw.rect(screen, self.grassColor, grassRect)

    def draw_score(self):
        scoreText = str(len(self.snake.body) - 3)
        scoreSurface = gameFont.render(scoreText, True, (56, 74, 12))
        x_pos = int(cellSize * cellNumber - 60)
        y_pos = int(cellSize * cellNumber - 40)
        scoreRect = scoreSurface.get_rect(center=(x_pos, y_pos))
        appleRect = apple.get_rect(midright=(scoreRect.left, scoreRect.centery))
        backgroundRect = pygame.Rect(appleRect.left, appleRect.top, appleRect.width + scoreRect.width + 6,
                                     appleRect.height)

        pygame.draw.rect(screen, (167, 209, 61), backgroundRect)
        screen.blit(scoreSurface, scoreRect)
        screen.blit(apple, appleRect)
        pygame.draw.rect(screen, (56, 74, 12), backgroundRect, 2)

    def end_game(self):
        self.snake.reset()
        self.direction = Vector(1, 0)


def start_game():
    global cellSize, cellNumber, screen, apple, game, gameFont

    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    cellSize = 40
    cellNumber = 20
    screen = pygame.display.set_mode((cellNumber * cellSize, cellNumber * cellSize))
    clock = pygame.time.Clock()
    apple = pygame.image.load('Images/apple.png').convert_alpha()
    game = Game()
    SCREEN_UPDATE = pygame.USEREVENT
    gameFont = pygame.font.Font(None, 25)

    pygame.time.set_timer(SCREEN_UPDATE, 150)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                game.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.move_up()
                if event.key == pygame.K_DOWN:
                    game.move_down()
                if event.key == pygame.K_LEFT:
                    game.move_left()
                if event.key == pygame.K_RIGHT:
                    game.move_right()
        screen.fill((175, 215, 70))
        game.draw_elements()
        pygame.display.update()
        clock.tick(144)


if __name__ == '__main__':
    start_game()
