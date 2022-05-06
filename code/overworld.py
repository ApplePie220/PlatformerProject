import pygame
from game_data import levels


class Overworld:
    def __init__(self, start_level, max_level, surface, create_lvl):
        # настройки
        self.display_surface = surface
        self.max_level = max_level
        self.current_level = start_level
        self.create_lvl = create_lvl

        # логика перемещения иконки
        self.moving = False
        self.move_direction = pygame.math.Vector2(0, 0)
        self.speed = 7

        # спрайты
        self.setup_nodes()
        self.setup_icon()

    # установка иконки игрока
    def setup_icon(self):
        self.icon = pygame.sprite.GroupSingle()
        # создание иконки на спрайте текущего уровня
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)

    # установка блоков уровней
    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()
        for index, node_data in enumerate(levels.values()):
            if index <= self.max_level:
                node_sprite = Node(node_data['node_pos'], 'available', self.speed)
                self.nodes.add(node_sprite)
            else:
                node_sprite = Node(node_data['node_pos'], 'locked', self.speed)
            self.nodes.add(node_sprite)

    # отрисовка маршрута между блоками уровней
    def draw_path(self):
        points = [node['node_pos'] for index, node in enumerate(levels.values())
                  if index <= self.max_level]
        pygame.draw.lines(self.display_surface, 'brown', False, points, 5)

    # обновление иконки игрока
    def upd_icon(self):
        if self.moving and self.move_direction:
            self.icon.sprite.position += self.move_direction * self.speed
            target_node = self.nodes.sprites()[self.current_level]
            # проверка на столкновение для остановки движения иконки
            if target_node.detect_zone.collidepoint(self.icon.sprite.position):
                self.moving = False
                self.move_direction = pygame.math.Vector2(0, 0)

    # считывание нажиманий на кнопки
    def input(self):
        keys = pygame.key.get_pressed()
        if not self.moving:
            if keys[pygame.K_RIGHT] and self.current_level < self.max_level:
                self.move_direction = self.get_movement_data('next')
                self.current_level += 1
                self.moving = True
            elif keys[pygame.K_LEFT] and self.current_level > 0:
                self.move_direction = self.get_movement_data('previous')
                self.current_level -= 1
                self.moving = True
            elif keys[pygame.K_SPACE]:
                self.create_lvl(self.current_level)

    # данные для конечного и начального перемещения
    def get_movement_data(self, target):
        start = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)
        if target == 'next':
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level + 1].rect.center)
        else:
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level - 1].rect.center)

        return (end - start).normalize()

    def run(self):
        # перемещение иконки игрока
        self.input()
        self.upd_icon()
        self.icon.update()
        # Отрисовка дорожек между уровнями
        self.draw_path()
        # отрисовка уровней
        self.nodes.draw(self.display_surface)
        # отрисовка иконки игрока
        self.icon.draw(self.display_surface)


# прямоугольники для дизайна уровней
class Node(pygame.sprite.Sprite):
    def __init__(self, position, stat, ic_speed):
        super().__init__()
        self.image = pygame.Surface((100, 100))
        if stat == 'available':
            self.image.fill('green')
        else:
            self.image.fill('red')
        self.rect = self.image.get_rect(center=position)
        self.detect_zone = pygame.Rect(self.rect.centerx - (ic_speed / 2),
                                       self.rect.centery - (ic_speed / 2),
                                       ic_speed, ic_speed)

# иконка игрока будет
class Icon(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.position = position
        self.image = pygame.Surface((20, 20))
        self.image.fill('pink')
        self.rect = self.image.get_rect(center=position)

    def update(self):
        self.rect.center = self.position
