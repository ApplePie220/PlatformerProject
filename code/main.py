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
        self.overworld = Overworld(1, self.max_level, screen, self.create_lvl)
        self.status = 'overworld'

    def create_lvl(self, current_level):
        self.level = Level(level_0, screen, current_level, self.create_overworld)
        self.status = 'level'

    def create_overworld(self, current_level, new_max_level):
        # откроется новый уровень, если выйграем
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_lvl)
        self.status = 'overworld'

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()


pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
# level = Level(level_0, screen)
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
