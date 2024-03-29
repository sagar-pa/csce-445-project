import pygame
pygame.init()

import os
import sys
import operator
import json

import config
import character
import event

def save_and_exit(current_event, clues_collected, scene_name):
    profile = {
        "current_event_id": current_event.id,
        "clues_collected": clues_collected,
        "scene_name": scene_name
    }

    with open('profile.json', 'w') as f:
        json.dump(profile, f, indent=4)

    pygame.display.quit()
    pygame.quit()
    sys.exit()

def create_sades(screen, events):
    return character.Character(
        config.SADES['id'],
        config.SADES['left_images'],
        config.SADES['right_images'],
        config.SADES['up_images'],
        config.SADES['down_images'],
        config.SADES['x'],
        config.SADES['y'],
        config.SADES['speed'],
        config.SADES['boundaries_image_filename'],
        screen,
        config.SADES['main_character'],
        [e for e in events if e.clue]
    )

def create_rei(screen):
    return character.Character(
        config.REI['id'],
        config.REI['left_images'],
        config.REI['right_images'],
        config.REI['up_images'],
        config.REI['down_images'],
        config.REI['x'],
        config.REI['y'],
        config.REI['speed'],
        config.REI['boundaries_image_filename'],
        screen,
        config.REI['main_character']
    )

def get_profile():
    with open('profile.json') as f:
        j = json.load(f)

    return j

def get_clue_file_locations():
    with open(os.path.join('clues', 'clue_files.json')) as f:
        j = json.load(f)

    file_locations = []

    for directory, filename in j:
        file_locations.append(os.path.join('clues', directory, filename))

    return file_locations

def get_clue_images():
    file_locations = get_clue_file_locations()

    images = []

    for file_location in file_locations:
        image = pygame.image.load(file_location)
        image = pygame.transform.scale(image, (config.CLUE_WIDTH, config.CLUE_HEIGHT))
        images.append(image)

    return images

def create_boundaries():
    for scene_image_filename in config.SCENES.values():
        boundaries_image_filename = scene_image_filename.replace('.png', '-boundaries.png')
        character.Character.init_valid_locations(boundaries_image_filename)

def get_event_with_id(events, event_id):
    for e in events:
        if e.id == event_id:
            return e

    return None

def move_character(events, current_event, characters):
    """ Moves a character around the scene. Returns the current_event. If the character
        is done moving, this will be the next event. Otherwise, it will be the same
        as the one that was given.
    """
    current_character = [c for c in characters if c.id == current_event.character_id][0]

    target_x, target_y = current_event.movements[0][0], current_event.movements[0][1]

    if target_x < current_character.x:
        current_character.left(detect=False)
    elif target_x > current_character.x:
        current_character.right(detect=False)
    elif target_y < current_character.y:
        current_character.up(detect=False)
    elif target_y > current_character.y:
        current_character.down(detect=False)
    else:
        current_event.movements = current_event.movements[1:]

        if not current_event.movements:
            return get_event_with_id(events, current_event.trigger)

    return current_event

def get_done_collecting_clues_event(events, scene_name):
    for e in events:
        if e.trigger_on_done and e.scene == scene_name:
            return e

    return None

def control_sades(key, sades, scene_name):
    if key == pygame.K_RETURN:
        return sades.interact(scene_name)
    elif key == pygame.K_LEFT:
        sades.left()
    elif key == pygame.K_RIGHT:
        sades.right()
    elif key == pygame.K_UP:
        sades.up()
    elif key == pygame.K_DOWN:
        sades.down()

    return None

def control_selection(key, events, current_event):
    if key == pygame.K_RETURN:
        return get_event_with_id(events, current_event.get_selection_trigger_event_id())
    elif key == pygame.K_UP:
        current_event.selection_up()
    elif key == pygame.K_DOWN:
        current_event.selection_down()

    return current_event

def load_new_scene(scene_name, characters):
    scene_image = pygame.image.load(config.SCENES[scene_name])
    for c in characters:
        c.boundaries_image_filename = config.SCENES[scene_name].replace('.png', '-boundaries.png')
    return scene_image

def run():
    # setup pygame
    pygame.key.set_repeat(1, 1)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    event.Event.screen = screen

    # setup current state
    profile = get_profile()
    events = event.Event.load_events(os.path.join('event', 'events.json'))
    current_event = get_event_with_id(events, profile['current_event_id'])
    most_recent_event = current_event
    prev_event = None
    frames = 0
    clues_collected = profile['clues_collected']

    # setup characters
    sades = create_sades(screen, events)
    rei = create_rei(screen)
    characters = [sades, rei]
    main_character = [c for c in characters if c.main_character == True][0]

    scene_name = profile['scene_name']
    scene_image = load_new_scene(scene_name, characters)

    clue_images = get_clue_images()

    # setup boundaries
    create_boundaries()

    while True:
        screen.fill([0, 0, 0])

        # If this is true, a character is being moved around.
        if current_event and current_event.character_id and current_event.movements:
            current_event = move_character(events, current_event, characters)
        else:
            for e in pygame.event.get():
                if e.type == pygame.KEYDOWN:
                    if current_event:
                        # half a second must pass before input is received again
                        if frames < (config.FPS / 2):
                            break

                        # text-based selection
                        if current_event.options:
                            current_event = control_selection(e.key, events, current_event)
                        elif e.key == pygame.K_RETURN:
                            current_event = get_event_with_id(events, current_event.trigger)

                            # skip events if the user hasn't collected the clues
                            while current_event and current_event.clues_necessary and not all(clue in set(clues_collected) for clue in current_event.clues_necessary):
                                current_event = get_event_with_id(events, current_event.trigger)

                    else:
                        # a fourth of a second must pass before input is received again
                        if frames < (config.FPS / 4):
                            break

                        current_event = control_sades(e.key, sades, scene_name)

                        if current_event and current_event.clue_id:
                            clues_collected.append(current_event.clue_id)

                        if e.key == pygame.K_d:
                            current_event = get_done_collecting_clues_event(events, scene_name)

                elif e.type == pygame.QUIT:
                    save_and_exit(most_recent_event, clues_collected, scene_name)
                        
        # blit the scene
        screen.blit(scene_image, main_character.get_relative_coordinates(0, 0))

        # don't draw characters on top of each other
        characters.sort(key=operator.attrgetter('y'))

        sades.draw()
        
        if scene_name == 'crime-scene':
            rei.draw(sades.get_relative_coordinates(rei.x, rei.y))

        # draw text box
        pygame.draw.rect(
            screen,
            [255, 255, 255],
            [config.SCREEN_WIDTH - config.TEXT_BOX_WIDTH, config.SCREEN_HEIGHT - config.TEXT_BOX_HEIGHT, config.TEXT_BOX_WIDTH, config.TEXT_BOX_HEIGHT],
        )
        
        # draw text box border
        pygame.draw.rect(
            screen,
            [0, 0, 0],
            [config.SCREEN_WIDTH - config.TEXT_BOX_WIDTH, config.SCREEN_HEIGHT - config.TEXT_BOX_HEIGHT, config.TEXT_BOX_WIDTH, config.TEXT_BOX_HEIGHT],
            2
        )

        # blit clues
        offset = config.SCREEN_WIDTH - (config.CLUE_WIDTH * config.NUMBER_OF_CLUES)
        pygame.draw.rect(screen, [255, 255, 255], [offset, 0, config.SCREEN_WIDTH, config.CLUE_HEIGHT])
        for i in range(config.NUMBER_OF_CLUES):
            if i + 1 in clues_collected:
                screen.blit(clue_images[i], (offset + i * config.CLUE_WIDTH, 0))

        # blit text
        if current_event:
            if current_event.text_only:
                screen.fill([255, 255, 255])

            current_event.blit_dialogue(top=current_event.text_only)

            if current_event.load_scene and scene_name != current_event.load_scene:
                scene_name = current_event.load_scene
                scene_image = load_new_scene(scene_name, characters)

            if current_event.teleport_to:
                sades.x, sades.y = current_event.teleport_to
                sades.direction = 'up'

            if current_event.game_over:
                save_and_exit(current_event, clues_collected, scene_name)

            most_recent_event = current_event

        if prev_event != current_event:
            frames = 0
        else:
            frames += 1

        prev_event = current_event

        pygame.display.update()
        clock.tick(config.FPS)

if __name__ == '__main__':
    run()
