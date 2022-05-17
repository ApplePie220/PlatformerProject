import pygame
from game_data import levels
from support import import_folder
from decoration import Background


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
        self.background = Background()

        # время
        self.start_time = pygame.time.get_ticks()
        self.input_allow = False
        self.timer_length = 500

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
                node_sprite = Node(node_data['node_pos'], 'available', self.speed,
                                   node_data['node_graphics'])
                self.nodes.add(node_sprite)
            else:
                node_sprite = Node(node_data['node_pos'], 'locked', self.speed,
                                   node_data['node_graphics'])
            self.nodes.add(node_sprite)

    # отрисовка маршрута между блоками уровней
    def draw_path(self):
        if self.max_level:
            points = [node['node_pos'] for index, node in enumerate(levels.values())
                      if index <= self.max_level]
            pygame.draw.lines(self.display_surface, '#a04f45', False, points, 5)

    # обновление иконки игрока
    def upd_icon(self):
        if self.moving and self.move_direction:
            self.icon.sprite.position += self.move_direction * self.speed
            target_node = self.nodes.sprites()[self.current_level]
            if target_node.detect_zone.collidepoint(self.icon.sprite.position):
                self.moving = False
                self.move_direction = pygame.math.Vector2(0, 0)

    # считывание нажиманий на кнопки
    def input(self):
        keys = pygame.key.get_pressed()
        if not self.moving and self.input_allow:
            if keys[pygame.K_RIGHT] and self.current_level < self.max_level:
                self.move_direction = self.get_movement_data('next')
                self.current_level += 1
                self.moving = True
            elif keys[pygame.K_LEFT] and self.current_level > 0:
                self.move_direction = self.get_movement_data('previous')
                self.current_level -= 1
                self.moving = True
            elif keys[pygame.K_RETURN]:
                self.create_lvl(self.current_level)

    def input_timer(self):
        if not self.input_allow:
            curr_time = pygame.time.get_ticks()
            if curr_time - self.start_time >= self.timer_length:
                self.input_allow = True

    # данные для конечного и начального перемещения
    def get_movement_data(self, target):
        start = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)
        if target == 'next':
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level + 1].rect.center)
        else:
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level - 1].rect.center)

        return (end - start).normalize()

    def run(self):
        self.input_timer()

        # перемещение иконки игрока
        self.input()
        self.upd_icon()
        self.icon.update()
        self.nodes.update()

        # отрисовка бэкрагунда
        self.background.draw(self.display_surface)

        # Отрисовка дорожек между уровнями
        self.draw_path()

        # отрисовка уровней
        self.nodes.draw(self.display_surface)

        # отрисовка иконки игрока
        self.icon.draw(self.display_surface)


# прямоугольники для дизайна уровней
class Node(pygame.sprite.Sprite):
    def __init__(self, position, stat, ic_speed, path):
        super().__init__()
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        if stat == 'available':
            self.stat = 'available'
        else:
            self.stat = 'locked'
        self.rect = self.image.get_rect(center=position)
        self.detect_zone = pygame.Rect(self.rect.centerx - (ic_speed / 2),
                                       self.rect.centery - (ic_speed / 2),
                                       ic_speed, ic_speed)

    # метод для анимации спрайтов блоков уровней
    def animate(self):
        self.frame_index += 0.1
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self):
        if self.stat == 'available':
            self.animate()
        else:
            tint_surf = self.image.copy()
            tint_surf.fill('black', None, pygame.BLEND_RGBA_MULT)
            self.image.blit(tint_surf, (0, 0))


class Icon(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.position = position
        self.image = pygame.image.load('../graphics/overworld/1.png').convert_alpha()
        self.rect = self.image.get_rect(center=position)

    def update(self):
        self.rect.center = self.position
