from support import import_folder
import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, shift):
        self.rect.x += shift


class StaticTile(Tile):
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface


class Crate(StaticTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, pygame.image.load('../graphics/terrain/boxe.png').convert_alpha())
        # смещение дле ящиков, чтобы не парили в воздухе
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft=(x, offset_y))


class AnimatedTile(Tile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

    def animate(self):
        # frame_index - с какой скоростью будут меняеться изображения
        self.frame_index += 0.2
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    # функция для запуска анимации
    def update(self, shift):
        self.animate()
        self.rect.x += shift


class Coin(AnimatedTile):
    def __init__(self, size, x, y, path, value):
        super().__init__(size, x, y, path)
        # смещаем спрайт на центр блока
        center_x = x + int(size / 2)
        center_y = y + int(size / 2)
        self.rect = self.image.get_rect(center=(center_x, center_y))

        # вес каждой монетки
        self.value = value


class Tree(AnimatedTile):
    def __init__(self, size, x, y, path, offset):
        super().__init__(size, x, y, path)
        offset_y = y - offset
        self.rect.topleft = (x, offset_y)
