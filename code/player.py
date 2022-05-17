from math import sin
import pygame
from support import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, position, surface, jump_particles, change_health):
        super().__init__()

        # грузим изображения для анимации
        self.import_character()

        # устанавливаем скорость для анимации и индекс каждого кадра
        self.frame_index = 0
        self.animation_speed = 0.12

        # частицы
        self.import_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.12
        self.display_surface = surface
        self.jump_particles = jump_particles

        # создание физического тела персонажа
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=position)
        self.collision_rect = pygame.Rect(self.rect.topleft,
                                          (25, self.rect.height))

        # вектор направления для перемещения перса
        self.direction = pygame.math.Vector2(0, 0)

        # скорость перемещения перса
        self.speed = 4

        # настройка гравитации для прыжка и самого прыжка
        self.gravity = 0.8
        self.jump_speed = -16

        # статус по умолчанию
        self.status = 'idle'

        # настройка здоровья игрока и временной неуязвимости
        self.change_health = change_health
        self.temp_protect = False
        self.protect_duration = 700
        self.time_damage = 0

        # направление движение для анимации по умолчанию
        self.facing_right = True

        # состояния на земле по умолчанию
        # для корректной анимации
        self.on_ground = False
        self.on_celling = False
        self.on_left = False
        self.on_right = False

    # синусоидальные значения невидимости для анимации получения урона
    def sin_protect_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0

    # метод получения урона
    def get_damage(self, value=-50):
        if not self.temp_protect:
            # только смерть с двух ударов ударов, только хардкор
            self.change_health(value)
            self.temp_protect = True
            self.time_damage = pygame.time.get_ticks()

    def temp_protect_timer(self):
        if self.temp_protect:
            curr_time = pygame.time.get_ticks()
            if curr_time - self.time_damage >= self.protect_duration:
                self.temp_protect = False

    # функция для импортирования частиц для анимации
    def import_particles(self):
        self.particles_run = import_folder('../graphics/character/particles/run')

    # функция для импортирования изображения персонажа
    def import_character(self):
        character_path = '../graphics/character/'
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': []}
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    # функция для анимирования персонажа
    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
            self.rect.bottomleft = self.collision_rect.bottomleft
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image
            self.rect.bottomright = self.collision_rect.bottomright

        if self.temp_protect:
            get_sin_value = self.sin_protect_value()
            self.image.set_alpha(get_sin_value)
        else:
            self.image.set_alpha(255)

        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    # анимация частиц
    def dust_animate(self):
        if self.status == 'run' and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.particles_run):
                self.dust_frame_index = 0
            dust_particles = self.particles_run[int(self.dust_frame_index)]
            if self.facing_right:
                position = self.rect.bottomleft - pygame.math.Vector2(6, 10)
                self.display_surface.blit(dust_particles, position)
            else:
                position = self.rect.bottomright - pygame.math.Vector2(6, 10)
                flipped_dust_part = pygame.transform.flip(dust_particles, True, False)
                self.display_surface.blit(flipped_dust_part, position)

    # статуст персонажа (бежит, стоит, прыгает, падает)
    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    # функция перемещения персонажа на экране
    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0
        if (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and self.on_ground:
            self.jump()
            self.jump_particles(self.rect.midbottom)

    # функция гравитации прыжка
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.collision_rect.y += self.direction.y

    # функция прыжка персонажа
    def jump(self):
        self.direction.y = self.jump_speed

    # обновления персонажа на экране
    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.dust_animate()
        self.temp_protect_timer()
        self.sin_protect_value()
