import os
import pygame
import json

import config

class Event:
    font = pygame.font.Font(os.path.join('event', 'consolas.ttf'), 20)
    text_width, text_height = font.size(' ')

    screen = None

    @staticmethod
    def event_dict_to_event(event_dict):
        return Event(
            event_dict['id'],
            event_dict['dialogue'],
            event_dict['text_only'],
            character_id=event_dict.get('character_id', None),
            hint=event_dict.get('hint', None),
            entry=event_dict.get('entry', None),
            trigger_event_id=event_dict.get('trigger_event_id', None),
            movements=event_dict.get('movements', None),
            options=event_dict.get('options', []),
            clue=event_dict.get('clue', None),
            teleport_to=event_dict.get('teleport_to', None),
            trigger_on_done=event_dict.get('trigger_on_done', None)
        )

    @staticmethod
    def load_events(filename):
        with open(filename, 'r') as f:
            s = f.read()

        j = json.loads(s)

        events = []
        for event_dict in j:
            events.append(Event.event_dict_to_event(event_dict))

        return events

    def __init__(self, id, dialogue, text_only, character_id=None, hint=None, entry=False, trigger_event_id=None, movements=None, options=[], clue=None, teleport_to=None, trigger_on_done=None):
        """ Character should be included if a character is saying the dialogue.
            Hint should be included if interacting with a hint triggers the
            dialogue. Entry should be True if the dialogue occurs automatically.
            Event should be given if this event always occurs after the given event.
            Movements should be a list of movements that the given character should
            perform after the given dialogue.
        """
        self.id = id
        self.dialogue = dialogue.replace('\n', ' ')
        self.text_only = text_only
        self.character_id = character_id
        self.hint = hint
        self.entry = entry
        self.trigger_event_id = trigger_event_id
        self.movements = movements
        self.options = options
        self.selection = 0
        self.clue = clue
        self.teleport_to = teleport_to
        self.trigger_on_done = trigger_on_done

    def __hash__(self):
        return hash(id)

    def __str__(self):
        return 'ID: {}'.format(self.id)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.id == other.id

    def blit_dialogue(self, top=False):
        remaining = self.dialogue
        offset = 0

        while remaining.strip():
            last_character_location = min((config.TEXT_BOX_WIDTH / Event.text_width) - 2, len(remaining))

            while last_character_location != len(remaining) and remaining[last_character_location] != ' ':
                last_character_location -= 1
        
            text = Event.font.render(remaining[:last_character_location], False, [0, 0, 0]) 

            if top:
                Event.screen.blit(text, [3, offset + 3]) 
            else:
                Event.screen.blit(text, [config.SCREEN_WIDTH - config.TEXT_BOX_WIDTH + 3, offset + config.SCREEN_HEIGHT - config.TEXT_BOX_HEIGHT + 3]) 

            while last_character_location < len(remaining) and remaining[last_character_location] == ' ':
                last_character_location += 1

            remaining = remaining[last_character_location:]
            offset += Event.text_height + 3

        for i, option in enumerate(self.options):
            if i == self.selection:
                option = '> ' + option
            else:
                option = '  ' + option
                
            text = Event.font.render(option, False, [0, 0, 0]) 

            if top:
                Event.screen.blit(text, [3, offset + 3]) 
            else:
                Event.screen.blit(text, [config.SCREEN_WIDTH - config.TEXT_BOX_WIDTH + 3, offset + config.SCREEN_HEIGHT - config.TEXT_BOX_HEIGHT + 3]) 

    def selection_up(self):
        self.selection -= 1
        self.selection %= len(self.options)

    def selection_down(self):
        self.selection += 1
        self.selection %= len(self.options)
