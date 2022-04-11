import pygame
from support import import_csv_layout, import_graphics
from settings import tile_size
from tile import Tile, StaticTile, Crate


class Level:
    def __init__(self, level_data, surface):
        # настройка экрана и скорость прокрутки уровня
        self.display_surface = surface
        self.world_shift = -5

        # настройка ландшафта
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_group_tile(terrain_layout, 'terrain')

        # настройка травки
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_group_tile(grass_layout, 'grass')

        # настройка ящиков
        crate_layout = import_csv_layout(level_data['crates'])
        self.crate_sprites = self.create_group_tile(crate_layout, 'crates')

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


                    sprite_group.add(sprite)

        return sprite_group

    def run(self):
        # отображаем ландшафт
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift)

        # отображение травы
        self.grass_sprites.draw(self.display_surface)
        self.grass_sprites.update(self.world_shift)

        # отображение ящиков
        self.crate_sprites.update(self.world_shift)
        self.crate_sprites.draw(self.display_surface)
