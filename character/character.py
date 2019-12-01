import pygame
from PIL import Image
import config

class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_nearby(self):
        return [
            Coordinate(self.x - 1, self.y),
            Coordinate(self.x + 1, self.y),
            Coordinate(self.x, self.y - 1),
            Coordinate(self.x, self.y + 1),
        ]

    def __hash__(self):
        return self.x * 10000 + self.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return '({}, {})'.format(self.x, self.y)

class Character:
    valid_locations = {}
    clue_locations = []

    def __init__(self, id, left_images, right_images, up_images, down_images, x, y, speed, boundaries_image_filename, clues_image_filename, screen, main_character, clue_events=[]):
        self.id = id

        self.width = config.CHARACTER_WIDTH
        self.height = config.CHARACTER_HEIGHT

        left_images = [pygame.image.load(filename) for filename in left_images]
        right_images = [pygame.image.load(filename) for filename in right_images]
        up_images = [pygame.image.load(filename) for filename in up_images]
        down_images = [pygame.image.load(filename) for filename in down_images]

        left_images = [pygame.transform.scale(image, (self.width, self.height)) for image in left_images]
        right_images = [pygame.transform.scale(image, (self.width, self.height)) for image in right_images]
        up_images = [pygame.transform.scale(image, (self.width, self.height)) for image in up_images]
        down_images = [pygame.transform.scale(image, (self.width, self.height)) for image in down_images]

        self.frames = len(left_images)

        self.images = {}
        self.add_images(self.images, 'left', left_images)
        self.add_images(self.images, 'right', right_images)
        self.add_images(self.images, 'up', up_images)
        self.add_images(self.images, 'down', down_images)

        self.x = x
        self.y = y
        self.speed = speed

        self.boundaries_image_filename = boundaries_image_filename
        Character.init_valid_locations(boundaries_image_filename)

        self.direction = 'down'
        self.step = 0

        self.screen = screen

        self.main_character = main_character

        self.clue_events = clue_events

        Character.init_clue_locations([clue_event.clue for clue_event in self.clue_events])

    @staticmethod
    def get_locations_with_color(image_filename, color):
        pil_image = Image.open(image_filename)
        width, height = pil_image.size
        pil_image = pil_image.convert('RGB')

        locations = []

        for i in range(width):
            for j in range(height):
                pixel_color = pil_image.getpixel((i, j))
                if pixel_color[0] == color[0] and pixel_color[1] == color[1] and pixel_color[2] == color[2]:
                    locations.append(Coordinate(i, j))

        return locations

    @staticmethod
    def init_valid_locations(boundaries_image_filename):
        if boundaries_image_filename in Character.valid_locations:
            return

        Character.valid_locations[boundaries_image_filename] = set(Character.get_locations_with_color(boundaries_image_filename, [255, 255, 255]))
   
    @staticmethod
    def init_clue_locations(clue_rectangles):
        for clue_rectangle in clue_rectangles:
            locations = set()

            for i in range(clue_rectangle[0], clue_rectangle[0] + clue_rectangle[2]):
                for j in range(clue_rectangle[1], clue_rectangle[1] + clue_rectangle[3]):
                    locations.add(Coordinate(i, j))

            Character.clue_locations.append(locations)

    def __eq__(self, other):
        return self.id == other.id
        
    def __str__(self):
        return 'ID: {}'.format(self.id)

    def __repr__(self):
        return str(self)

    def is_clue_location(self, x, y):
        print x, y
        print Character.clue_locations

        for i in range(x, x + self.width, self.width / 5):
            for j in range(y, y + self.height, self.height / 5):
                for clue_blob in Character.clue_locations:
                    if Coordinate(i, j) in clue_blob:
                        return clue_blob

        return None

    def interact(self):
        y_offset = 0
        x_offset = 0

        if self.direction == 'up':
            x_offset = self.width / 2
            y_offset = -5
        elif self.direction == 'down':
            x_offset = self.width / 2
            y_offset = 5 + self.height
        elif self.direction == 'right':
            x_offset = 5 + self.width
            y_offset = self.height / 2
        elif self.direction == 'left':
            x_offset = -5
            y_offset = self.height / 2

        clue_blob = self.is_clue_location(self.x + x_offset, self.y + y_offset)

        if clue_blob:
            for clue_event in self.clue_events:
                if Coordinate(clue_event.clue[0], clue_event.clue[1]) in clue_blob:
                    return clue_event

        return None

    def add_images(self, images_dict, prefix, images):
        for i, image in enumerate(images):
            images_dict[prefix + str(i)] = image

    def is_valid_location(self, x, y):
        for i in range(x, x + self.width, self.width / 5):
            for j in range(y, y + self.height, self.height / 5):
                if Coordinate(i, j) not in Character.valid_locations[self.boundaries_image_filename]:
                    return False

        return True

    def draw(self, xy=None):
        self.step %= self.frames
        if not xy:
            center = ((config.SCREEN_WIDTH / 2) - (self.width / 2), (config.SCREEN_HEIGHT / 2) - (self.height / 2))
            self.screen.blit(self.images[self.direction + str(self.step)], center)
        else:
            self.screen.blit(self.images[self.direction + str(self.step)], (xy[0], xy[1]))

    def up(self, detect=True):
        if not detect or self.is_valid_location(self.x, self.y - self.speed):
            self.y -= self.speed

        self.direction = 'up'
        self.step += 1
    
    def down(self, detect=True):
        if not detect or self.is_valid_location(self.x, self.y + self.speed):
            self.y += self.speed

        self.direction = 'down'
        self.step += 1

    def left(self, detect=True):
        if not detect or self.is_valid_location(self.x - self.speed, self.y):
            self.x -= self.speed
            
        self.direction = 'left'
        self.step += 1

    def right(self, detect=True):
        if not detect or self.is_valid_location(self.x + self.speed, self.y):
            self.x += self.speed

        self.direction = 'right'
        self.step += 1

    def get_relative_coordinates(self, x, y):
        """ Returns coordinates of the scene, assuming this character is the 
            main character.
        """
        relative_x = (config.SCREEN_WIDTH / 2) - (self.width / 2) - self.x + x
        relative_y = (config.SCREEN_HEIGHT / 2) - (self.height / 2) - self.y + y
        return relative_x, relative_y
