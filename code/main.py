import pygame
import sys

from settings import *
from level import Level
from overworld import Overworld
from ui import UI


# класс для логи запуска внешнего мира
class Game:
    def __init__(self):

        # фичи уровня
        self.max_level = 0
        self.max_health = 100
        self.current_health = 100
        self.coins = 0

        # создание внешнего мира
        self.overworld = Overworld(0, self.max_level, screen, self.create_lvl)
        self.status = 'overworld'

        # интерфейс
        self.ui = UI(screen)

    def change_scores(self, amount):
        self.coins += amount

    def create_lvl(self, current_level):

        # внутрь класса level передаем методы из класса game чтобы вызвать их оттуда
        self.level = Level(current_level, screen, self.create_overworld, self.change_scores)
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
            self.ui.show_health(self.current_health, self.max_health)
            self.ui.show_scores(self.coins)


pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # screen.fill('grey')
    game.run()

    pygame.display.set_caption("Приключения Тимоти Шаурмы")
    pygame.display.set_icon(pygame.image.load('graphics/icon/plum1.png'))
    pygame.display.update()
    clock.tick(60)
