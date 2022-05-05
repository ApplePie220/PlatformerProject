import pygame
from game_data import levels


class Overworld:
    def __init__(self, start_level, max_level, surface):
        # настройки
        self.display_surface = surface
        self.max_level = max_level
        self.current_level = start_level

        # спрайты
        self.setup_nodes()

    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()
        for index, node_data in enumerate(levels.values()):
            if index <= self.max_level:
                node_sprite = Node(node_data['node_pos'], 'available')
                self.nodes.add(node_sprite)
            else:
                node_sprite = Node(node_data['node_pos'], 'locked')
            self.nodes.add(node_sprite)

    def draw_path(self):
        points = [node['node_pos'] for index, node in enumerate(levels.values())
                  if index <= self.max_level]
        pygame.draw.lines(self.display_surface, 'brown', False, points, 5)

    def run(self):
        self.draw_path()
        self.nodes.draw(self.display_surface)


# спрайты для дизайна уровней
class Node(pygame.sprite.Sprite):
    def __init__(self, position, stat):
        super().__init__()
        self.image = pygame.Surface((100, 90))
        if stat == 'available':
            self.image.fill('green')
        else:
            self.image.fill('red')
        self.rect = self.image.get_rect(center=position)


# иконка игрока будет
class Icon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
