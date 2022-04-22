import pygame
from support import import_csv_layout, import_graphics
from settings import tile_size, screen_height
from tile import Tile, StaticTile, Crate, AnimatedTile, Coin, Tree
from enemy import Enemy
from decoration import Sky
from player import Player
from particles import Particle


class Level:
    def __init__(self, level_data, surface):
        # настройка экрана и скорость прокрутки уровня
        self.display_surface = surface
        self.world_shift = 0

        # настройка ландшафта
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_group_tile(terrain_layout, 'terrain')

        # настройка травки
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_group_tile(grass_layout, 'grass')

        # настройка ящиков
        crate_layout = import_csv_layout(level_data['crates'])
        self.crate_sprites = self.create_group_tile(crate_layout, 'crates')

        # настройка монеток
        coin_layout = import_csv_layout(level_data['coins'])
        self.coin_sprites = self.create_group_tile(coin_layout, 'coins')

        # настройка деревьев на переднем плане
        fg_trees_layout = import_csv_layout(level_data['fg trees'])
        self.fg_trees_sprites = self.create_group_tile(fg_trees_layout, 'fg trees')

        # настройка деревьев на заднем плане
        bg_trees_layout = import_csv_layout(level_data['bg trees'])
        self.bg_trees_sprites = self.create_group_tile(bg_trees_layout, 'bg trees')

        # настройка врагов
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemies_sprite = self.create_group_tile(enemy_layout, 'enemies')

        # настройка ограничений для врагов
        constraint_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_group_tile(constraint_layout, 'constraints')

        # настройка игрока
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.purpose = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        # настройка декораций
        self.sky = Sky()
        level_width = len(terrain_layout[0]) * tile_size

    def create_group_tile(self, layout, type):
        sprite_group = pygame.sprite.Group()

        # перебираем каждый элемент внутри строки
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                if col != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    # натягиваем спрайты на блоки ландшафта
                    if type == 'terrain':
                        terrain_tile_list = import_graphics('graphics/terrain/tileset.png')
                        tile_surface = terrain_tile_list[int(col)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    # натягиваем спрайты на блоки травы
                    if type == 'grass':
                        grass_tile_list = import_graphics('graphics/terrain/grass_tiles.png')
                        tile_surface = grass_tile_list[int(col)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    # натягиваем спрайты на блоки ящиков
                    if type == 'crates':
                        sprite = Crate(tile_size, x, y)

                    if type == 'enemies':
                        sprite = Enemy(tile_size, x, y)

                    if type == 'constraints':
                        sprite = Tile(tile_size, x, y)

                    # накладываем спрайты на монетки
                    if type == 'coins':
                        if col == '0':
                            sprite = Coin(tile_size, x, y, 'graphics/coin/standart')
                        if col == '1':
                            sprite = Coin(tile_size, x, y, 'graphics/coin/pink')

                    # накладываем спрайты на деревья на переднем плане
                    if type == 'fg trees':
                        if col == '1':
                            sprite = Tree(tile_size, x, y, 'graphics/terrain/trees/onetree', 85)
                        if col == '2':
                            sprite = Tree(tile_size, x, y, 'graphics/terrain/trees/twotree', 118)
                        if col == '3':
                            sprite = Tree(tile_size, x, y, 'graphics/terrain/trees/threetree', 133)
                        if col == '5':
                            sprite = Tree(tile_size, x, y, 'graphics/terrain/trees/siztree', 100)
                        if col == '6':
                            sprite = Tree(tile_size, x, y, 'graphics/terrain/trees/fivetree', 82)

                    # накладываем спрайты на деревья на заднем плане
                    if type == 'bg trees':
                        if col == '0':
                            # 45 и остальные цифры - смещение спрайта на кол-во пикселов
                            sprite = Tree(tile_size, x, y, 'graphics/terrain/trees/seventree', 45)
                        if col == '1':
                            sprite = Tree(tile_size, x, y, 'graphics/terrain/trees/onetree', 85)
                        if col == '3':
                            sprite = Tree(tile_size, x, y, 'graphics/terrain/trees/threetree', 125)
                        if col == '5':
                            sprite = Tree(tile_size, x, y, 'graphics/terrain/trees/siztree', 150)
                        if col == '6':
                            sprite = Tree(tile_size, x, y, 'graphics/terrain/trees/fivetree', 82)

                    sprite_group.add(sprite)

        return sprite_group

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if col == '0':
                    sprite = Player((x, y),self.display_surface, self.jump_particles)
                    self.player.add(sprite)
                if col == '1':
                    hat_surface = pygame.image.load('graphics/character/end.png').convert_alpha()
                    sprite = StaticTile(tile_size, x, y, hat_surface)
                    self.purpose.add(sprite)

    # находился ли персонаж на земле
    def get_player_onground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            # если он не был на земле, значит был в воздухе
            self.player_on_ground = False

    # анимация чатсиц для приземления
    def create_land_particles(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(1, 17)
            else:
                offset = pygame.math.Vector2(-1, 17)
            land_particles = Particle(self.player.sprite.rect.midbottom - offset, 'land')
            self.dust_sprite.add(land_particles)

    # анимация частиц для прыжка
    def jump_particles(self, position):
        if self.player.sprite.facing_right:
            position -= pygame.math.Vector2(10, 5)
        else:
            position += pygame.math.Vector2(10, -5)
        jump_part_sprite = Particle(position, 'jump')
        self.dust_sprite.add(jump_part_sprite)

    def enemy_move_reverse(self):
        for enemy in self.enemies_sprite.sprites():
            # проверяем, сталкивается ли враг с ограничением
            # False - не разрешаем разрушения ограничения, если враг столкнулся с ним
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()

    def run(self):
        # отображение бэкграунда
        self.sky.draw(self.display_surface)

        # отображение деревьев на заднем плане
        self.bg_trees_sprites.update(self.world_shift)
        self.bg_trees_sprites.draw(self.display_surface)

        # отображаем ландшафт
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift)

        # отображение врагов и ограничений для них
        self.enemies_sprite.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_move_reverse()
        self.enemies_sprite.draw(self.display_surface)

        # отображение ящиков
        self.crate_sprites.update(self.world_shift)
        self.crate_sprites.draw(self.display_surface)

        # отображение деревьев на переднем плане
        self.fg_trees_sprites.update(self.world_shift)
        self.fg_trees_sprites.draw(self.display_surface)

        # отображение травы
        self.grass_sprites.draw(self.display_surface)
        self.grass_sprites.update(self.world_shift)

        # отображение монеток
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)

        # отображение игрока
        self.player.update()
        # TODO сделать спрайт игрока больше размером
        # а то совсем стыд, какая маленькая
        # её еле разглядишь среди блоков и остального, кошмарище...
        self.player.draw(self.display_surface)
        self.purpose.update(self.world_shift)
        self.purpose.draw(self.display_surface)

