import pygame
pygame.init()

import os
import operator

import config
import character
import event

def run():
    pygame.key.set_repeat(1, 1)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    event.Event.screen = screen
    scene = pygame.image.load(os.path.join('maps', 'crime-scene.png'))
    current_event = None
    frames_to_skip = 0
    current_level = 'intro'

    if current_level == 'intro':
        events = event.Event.load_events(os.path.join('event', 'intro_events.json'))

    sades = character.Character(
        config.SADES['id'],
        config.SADES['left_images'],
        config.SADES['right_images'],
        config.SADES['up_images'],
        config.SADES['down_images'],
        config.SADES['x'],
        config.SADES['y'],
        config.SADES['speed'],
        config.SADES['boundaries_image_filename'],
        config.SADES['clues_image_filename'],
        screen,
        config.SADES['main_character'],
        [e for e in events if e.clue]
    )

    rei = character.Character(
        config.REI['id'],
        config.REI['left_images'],
        config.REI['right_images'],
        config.REI['up_images'],
        config.REI['down_images'],
        config.REI['x'],
        config.REI['y'],
        config.REI['speed'],
        config.REI['boundaries_image_filename'],
        config.REI['clues_image_filename'],
        screen,
        config.REI['main_character']
    )

    characters = [sades, rei]
    main_character = [c for c in characters if c.main_character == True][0]

    while True:
        if frames_to_skip:
            screen.fill([0, 0, 0])
            frames_to_skip -= 1

            current_event = [e for e in events if event.trigger_on_done]

            continue


        screen.fill([0, 0, 0])

        # If this is true, a character is being moved around.
        if current_event and current_event.character_id and current_event.movements:
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
                    previous_event_id = current_event.id

                    events.remove(current_event)
                    current_event = None

                    for game_event in events:
                        if game_event.trigger_event_id == previous_event_id:
                            current_event = game_event
                            break
        else:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    break

                if e.type == pygame.KEYDOWN:
                    if current_event:
                        if e.key == pygame.K_RETURN:
                            previous_event_id = current_event.id

                            events.remove(current_event)
                            current_event = None

                            for game_event in events:
                                if game_event.trigger_event_id == previous_event_id:
                                    current_event = game_event
                                    break

                    elif e.key == pygame.K_RETURN:
                        current_event = sades.interact()
                    elif e.key == pygame.K_LEFT:
                        sades.left()
                    elif e.key == pygame.K_RIGHT:
                        sades.right()
                    elif e.key == pygame.K_UP:
                        sades.up()
                    elif e.key == pygame.K_DOWN:
                        sades.down()
                    elif e.key == pygame.K_d:
                        frames_to_skip = 15
                        sades.up()
                        
        screen.blit(scene, main_character.get_relative_coordinates(0, 0))

        # don't draw characters on top of each other
        characters.sort(key=operator.attrgetter('y'))
        for c in characters:
            if c.main_character:
                c.draw()
            else:
                c.draw(main_character.get_relative_coordinates(c.x, c.y))

        if current_level == 'intro':
            # text box
            pygame.draw.rect(
                screen,
                [255, 255, 255],
                [config.SCREEN_WIDTH - config.TEXT_BOX_WIDTH, config.SCREEN_HEIGHT - config.TEXT_BOX_HEIGHT, config.TEXT_BOX_WIDTH, config.TEXT_BOX_HEIGHT],
            )
            
            # text box border
            pygame.draw.rect(
                screen,
                [0, 0, 0],
                [config.SCREEN_WIDTH - config.TEXT_BOX_WIDTH, config.SCREEN_HEIGHT - config.TEXT_BOX_HEIGHT, config.TEXT_BOX_WIDTH, config.TEXT_BOX_HEIGHT],
                2
            )
             
            for intro_event in events:
                if intro_event.entry:
                    current_event = intro_event

        if current_event:
            if current_event.text_only:
                screen.fill([255, 255, 255])

            current_event.blit_dialogue(top=current_event.text_only)

        pygame.display.update()
        clock.tick(config.FPS)

if __name__ == '__main__':
    run()
