import pygame


class UI:
    def __init__(self, surface):
        self.display_surface = surface

        # монетки
        self.coin = pygame.image.load('../graphics/ui/coin1.png').convert_alpha()
        self.coin_rect = self.coin.get_rect(topleft=(50, 61))

        # здоровье
        self.health_bar = pygame.image.load('../graphics/ui/health_bar2.png').convert_alpha()
        self.health_bar_topleft = (54, 39)
        self.bar_max_length = 152
        self.bar_height = 4

        # шрифт
        self.font = pygame.font.Font('../graphics/ui/font.ttf', 20)

    def show_health(self, curr, full):
        self.display_surface.blit(self.health_bar, (20, 10))
        curr_health_ratio = curr / full
        curr_bar_length = self.bar_max_length * curr_health_ratio
        health_bar_rect = pygame.Rect(self.health_bar_topleft, (curr_bar_length, self.bar_height))
        pygame.draw.rect(self.display_surface, '#AD4A19', health_bar_rect)

    def show_scores(self, amount):
        self.display_surface.blit(self.coin, self.coin_rect)
        coin_amount = self.font.render(str(amount), False, '#EEE8AA')
        coin_amount_rect = coin_amount.get_rect(midleft=(self.coin_rect.right + 4, self.coin_rect.centery))
        self.display_surface.blit(coin_amount, coin_amount_rect)
