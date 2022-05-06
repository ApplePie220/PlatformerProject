import pygame
import sys

from settings import *
from level import Level
from game_data import level_0
from overworld import Overworld


# класс для логи запуска внешнего мира
class Game:
    def __init__(self):
        self.max_level = 2
        self.overworld = Overworld(0, self.max_level, screen)

    def run(self):
        self.overworld.run()


pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level(level_0, screen)
game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('grey')
    game.run()
    # level.run()

    pygame.display.set_caption("Приключения Тимоти Шаурмы")
    pygame.display.set_icon(pygame.image.load('graphics/icon/witch.gif'))
    pygame.display.update()
    clock.tick(60)
