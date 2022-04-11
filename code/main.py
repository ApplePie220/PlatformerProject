import pygame
import sys

from settings import *
from level import Level
from game_data import level_0

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level(level_0, screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('black')
    level.run()

    pygame.display.set_caption("Приключения Тимоти Шаурмы")
    pygame.display.set_icon(pygame.image.load('graphics/icon/witch.gif'))
    pygame.display.update()
    clock.tick(60)
