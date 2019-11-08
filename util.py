import config

def get_scene_coordinates(main_character):
    x = (config.SCREEN_WIDTH / 2) - (main_character.width / 2) - main_character.x
    y = (config.SCREEN_HEIGHT / 2) - (main_character.height / 2) - main_character.y
    return x, y
