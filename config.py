import os

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700

TEXT_BOX_WIDTH = SCREEN_WIDTH
TEXT_BOX_HEIGHT = min(200, SCREEN_HEIGHT / 4)

FONT_SIZE = 20

CHARACTER_WIDTH = 32
CHARACTER_HEIGHT = 46

FPS = 15

SADES = {
    'id': 1,
    'left_images': [os.path.join('character', 'images', 'sades', 'left-1.png'), os.path.join('character', 'images', 'sades', 'left-2.png'), os.path.join('character', 'images', 'sades', 'left-1.png'), os.path.join('character', 'images', 'sades', 'left-3.png')],
    'right_images': [os.path.join('character', 'images', 'sades', 'right-1.png'), os.path.join('character', 'images', 'sades', 'right-2.png'), os.path.join('character', 'images', 'sades', 'right-1.png'), os.path.join('character', 'images', 'sades', 'right-3.png')],
    'up_images': [os.path.join('character', 'images', 'sades', 'up-1.png'), os.path.join('character', 'images', 'sades', 'up-2.png'), os.path.join('character', 'images', 'sades', 'up-1.png'), os.path.join('character', 'images', 'sades', 'up-3.png')],
    'down_images': [os.path.join('character', 'images', 'sades', 'down-1.png'), os.path.join('character', 'images', 'sades', 'down-2.png'), os.path.join('character', 'images', 'sades', 'down-1.png'), os.path.join('character', 'images', 'sades', 'down-3.png')],
    'x': 620, 
    'y': 1100, 
    'speed': 10,
    'boundaries_image_filename': os.path.join('maps', 'crime-scene-boundaries.png'),
    'clues_image_filename': os.path.join('maps', 'crime-scene-clues.png'),
    'main_character': True
}

REI = {
    'id': 2,
    'left_images': [os.path.join('character', 'images', 'rei.png')],
    'right_images': [os.path.join('character', 'images', 'rei.png')],
    'up_images': [os.path.join('character', 'images', 'rei.png')],
    'down_images': [os.path.join('character', 'images', 'rei.png')],
    'x': 620,
    'y': 890,
    'speed': 10,
    'boundaries_image_filename': os.path.join('maps', 'crime-scene-boundaries.png'),
    'clues_image_filename': os.path.join('maps', 'crime-scene-clues.png'),
    'main_character': False
}
