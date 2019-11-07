import config
import character

import os
import pygame
import pytmx

def run():
    pygame.init()
    pygame.key.set_repeat(1, 1)

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    scene = pygame.image.load(os.path.join('maps', 'crime-scene.png'))

    sades = character.Character(
        config.SADES['left_images'],
        config.SADES['right_images'],
        config.SADES['up_images'],
        config.SADES['down_images'],
        config.SADES['x'],
        config.SADES['y'],
        config.SADES['speed'],
        config.SADES['boundaries_image_filename'],
        screen
    )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    sades.left()
                if event.key == pygame.K_RIGHT:
                    sades.right()
                if event.key == pygame.K_UP:
                    sades.up()
                if event.key == pygame.K_DOWN:
                    sades.down()

        screen.blit(scene, (0, 0))

        sades.draw()

        pygame.display.update()
        clock.tick(config.FPS)

if __name__ == '__main__':
    run()
