import os

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700

CHARACTER_WIDTH = 32
CHARACTER_HEIGHT = 46

FPS = 15

SADES = {
    'left_images': [os.path.join('character', 'images', 'sades', 'left-1.png'), os.path.join('character', 'images', 'sades', 'left-2.png'), os.path.join('character', 'images', 'sades', 'left-1.png'), os.path.join('character', 'images', 'sades', 'left-3.png')],
    'right_images': [os.path.join('character', 'images', 'sades', 'right-1.png'), os.path.join('character', 'images', 'sades', 'right-2.png'), os.path.join('character', 'images', 'sades', 'right-1.png'), os.path.join('character', 'images', 'sades', 'right-3.png')],
    'up_images': [os.path.join('character', 'images', 'sades', 'up-1.png'), os.path.join('character', 'images', 'sades', 'up-2.png'), os.path.join('character', 'images', 'sades', 'up-1.png'), os.path.join('character', 'images', 'sades', 'up-3.png')],
    'down_images': [os.path.join('character', 'images', 'sades', 'down-1.png'), os.path.join('character', 'images', 'sades', 'down-2.png'), os.path.join('character', 'images', 'sades', 'down-1.png'), os.path.join('character', 'images', 'sades', 'down-3.png')],
    'width': CHARACTER_WIDTH, 
    'height': CHARACTER_HEIGHT, 
    'x': 40, 
    'y': 310, 
    'speed': 10,
    'boundaries_image_filename': os.path.join('maps', 'crime-scene-boundaries.png'),
    'main_character': True
}
