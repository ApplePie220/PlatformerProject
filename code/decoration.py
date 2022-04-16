import pygame
from settings import vertical_tile, tile_size, screen_width, screen_height
from tile import AnimatedTile


class Sky:
    def __init__(self):
        self.background_img = pygame.image.load('graphics/decoration/background/bg1_back.png').convert()
        # растягивание спрайтов бэкграунда
        self.background_img = pygame.transform.scale(self.background_img, (screen_width, screen_height))

    # Отрисовываем бэк
    def draw(self, surface):
        my_rect = (0, 0, screen_width, screen_height)
        surface.blit(self.background_img, my_rect)

