import tile
import config

import os
import pygame
import pytmx

def load_tmx(filename, screen):
    tmx_data = pytmx.TiledMap(os.path.join('maps', 'crime-scene.tmx'))
    image = tmx_data.get_tile_image(0, 0, '10')
    screen.blit(image, 0, 0)

def run():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))

    blood = tile.Tile(os.path.join('tile', 'data', 'blood.csv'), screen)
    floor = tile.Tile(os.path.join('tile', 'data', 'carpet.csv'), screen)
    furniture = tile.Tile(os.path.join('tile', 'data', 'furniture.csv'), screen)
    kitchen = tile.Tile(os.path.join('tile', 'data', 'kitchen.csv'), screen)
    table_items = tile.Tile(os.path.join('tile', 'data', 'table_items.csv'), screen)
    wall_items = tile.Tile(os.path.join('tile', 'data', 'wall_items.csv'), screen)
    walls_sides = tile.Tile(os.path.join('tile', 'data', 'walls_sides.csv'), screen)
    walls = tile.Tile(os.path.join('tile', 'data', 'walls.csv'), screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break

        # floor.draw(0, 0)
        # blood.draw(30, 0)
        # furniture.draw(60, 0)
        kitchen.draw(90, 0)
        # table_items.draw(120, 0)
        # wall_items.draw(150, 0)
        # walls_sides.draw(180, 0)
        # walls.draw(210, 0)

        pygame.display.update()
        clock.tick(12)

if __name__ == '__main__':
    run()
