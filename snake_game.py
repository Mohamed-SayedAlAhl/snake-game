import sys
import pygame
import time
import random
import os

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

width = 600
height = 400

def resource_path0(relative_path):
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__))
    )
    return os.path.join(base_path, relative_path)

image = pygame.image.load(resource_path0('icon.png'))
icon = pygame.image.load(resource_path0('icon.png'))
pygame.display.set_icon(icon)

display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()
SnakeSize = 10
FPS = 7

font_style = pygame.font.SysFont(None, 30)
heart = pygame.image.load(resource_path0('heart.png'))
heart = pygame.transform.scale(heart, (30, 30))

def message(msg, color, x, y):
    mesg = font_style.render(msg, True, color)
    display.blit(mesg, [x, y])

def draw_hearts(lives):
    for i in range(lives):
        display.blit(heart, (10 + i * 40, 10))

def reset_snake():
    x1 = width / 2
    y1 = height / 2
    x1_change = 0
    y1_change = 0
    snake_List = []
    Length_of_snake = 1
    return x1, y1, x1_change, y1_change, snake_List, Length_of_snake

def pause_game():
    global FPS
    while True:
        display.fill(white)
        message("Paused", black, width / 2 - 30, height / 2 - 30)
        message(f"Speed: {FPS} (+/-)", black, width / 2 - 60, height / 2)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS or event.key == pygame.K_EQUALS:
                    FPS += 1
                elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS or event.key == pygame.K_UNDERSCORE:
                    FPS -= 1
                    if FPS < 1:
                        FPS = 1
                elif event.key == pygame.K_p:
                    return

def gameLoop():
    global FPS
    score = 0
    lives = 3
    game_over = False
    game_close = False

    x1, y1, x1_change, y1_change, snake_List, Length_of_snake = reset_snake()

    foodx = round(random.randrange(0, width - SnakeSize) / 10.0) * 10.0
    foody = round(random.randrange(40, height - SnakeSize) / 10.0) * 10.0

    while not game_over:
        while game_close:
            display.fill(white)
            message(f"You Lost! Score: {score}", red, width / 6, height / 3)
            message(f"Lives: {lives}", red, width / 6, height / 3 + 30)
            message("Press Q-Quit or R-Play Again", red, width / 6, height / 3 + 60)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_r:
                        lives = 3
                        score = 0
                        x1, y1, x1_change, y1_change, snake_List, Length_of_snake = reset_snake()
                        game_close = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -SnakeSize
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = SnakeSize
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -SnakeSize
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = SnakeSize
                    x1_change = 0
                elif event.key == pygame.K_p:
                    pause_game()

        x1 += x1_change
        y1 += y1_change

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            lives -= 1
            if lives == 0:
                game_close = True
            else:
                x1, y1, x1_change, y1_change, snake_List, Length_of_snake = reset_snake()

        display.fill(white)
        pygame.draw.rect(display, red, [foodx, foody, SnakeSize, SnakeSize])

        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                lives -= 1
                if lives == 0:
                    game_close = True
                else:
                    x1, y1, x1_change, y1_change, snake_List, Length_of_snake = reset_snake()
                    break

        for segment in snake_List:
            pygame.draw.rect(display, black, [segment[0], segment[1], SnakeSize, SnakeSize])

        draw_hearts(lives)
        message(f"Score: {score}", black, width - 150, 10)
        message(f"Speed: {FPS} (+/-)", black, width - 150, 40)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            score += 10
            foodx = round(random.randrange(0, width - SnakeSize) / 10.0) * 10.0
            foody = round(random.randrange(40, height - SnakeSize) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(FPS)

    pygame.quit()
    sys.exit()

gameLoop()