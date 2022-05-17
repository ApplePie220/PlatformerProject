import pygame
from support import import_folder


class Particle(pygame.sprite.Sprite):
    def __init__(self, position, type):
        super().__init__()
        self.frame_index = 0
        self.animate_speed = 0.5
        if type == 'jump':
            self.frames = import_folder('../graphics/character/particles/jump')
        if type == 'land':
            self.frames = import_folder('../graphics/character/particles/land')
        if type == 'exploision':
            self.frames = import_folder('../graphics/enemies/explosion')
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=position)

    # анимация частиц
    def animate(self):
        self.frame_index += self.animate_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self, x_shift):
        self.animate()
        self.rect.x += x_shift
