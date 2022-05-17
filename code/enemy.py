from random import randint
import pygame
from tile import AnimatedTile


class Enemy(AnimatedTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, '../graphics/enemies/run')
        self.rect.y += size - self.image.get_size()[1]
        self.speed = randint(1,3)

    # метод перемещения врагов
    def move(self):
        self.rect.x += self.speed

    # отражение спрайта, если враг движется вправо
    def reverse_img(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        self.speed *= -1

    def update(self, shift):
        self.rect.x += shift
        self.animate()
        self.move()
        self.reverse_img()
