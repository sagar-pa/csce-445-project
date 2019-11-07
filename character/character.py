import pygame
from PIL import Image
import config

class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return self.x * 10000 + self.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return '({}, {})'.format(self.x, self.y)

class Character:
    valid_locations = {}

    def __init__(self, left_images, right_images, up_images, down_images, x, y, speed, boundaries_image_filename, screen):
        self.width = config.SADES['width']
        self.height = config.SADES['height']

        left_images = [pygame.image.load(filename) for filename in left_images]
        right_images = [pygame.image.load(filename) for filename in right_images]
        up_images = [pygame.image.load(filename) for filename in up_images]
        down_images = [pygame.image.load(filename) for filename in down_images]

        left_images = [pygame.transform.scale(image, (self.width, self.height)) for image in left_images]
        right_images = [pygame.transform.scale(image, (self.width, self.height)) for image in right_images]
        up_images = [pygame.transform.scale(image, (self.width, self.height)) for image in up_images]
        down_images = [pygame.transform.scale(image, (self.width, self.height)) for image in down_images]

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

    @staticmethod
    def init_valid_locations(boundaries_image_filename):
        if boundaries_image_filename in Character.valid_locations:
            return

        pil_image = Image.open(boundaries_image_filename)
        width, height = pil_image.size
        pil_image = pil_image.convert('RGB')

        valid_locations = set()

        for i in range(width):
            for j in range(height):
                pixel_color = pil_image.getpixel((i, j))
                if sum(pixel_color[0:3]) == 765:
                    valid_locations.add(Coordinate(i, j))

        Character.valid_locations[boundaries_image_filename] = valid_locations
        
    def add_images(self, images_dict, prefix, images):
        for i, image in enumerate(images):
            images_dict[prefix + str(i)] = image

    def is_valid_location(self, x, y):
        top_left_valid = Coordinate(x, y) in Character.valid_locations[self.boundaries_image_filename]
        bottom_right_valid = Coordinate(x + self.width, y + self.height) in Character.valid_locations[self.boundaries_image_filename]

        print x, y, x + self.width, y + self.height, top_left_valid, bottom_right_valid

        return top_left_valid and bottom_right_valid

    def draw(self):
        self.step %= 3
        self.screen.blit(self.images[self.direction + str(self.step)], (self.x, self.y))

    def up(self):
        if self.is_valid_location(self.x, self.y - self.speed):
            self.y -= self.speed

        self.direction = 'up'
        self.step += 1
    
    def down(self):
        if self.is_valid_location(self.x, self.y + self.speed):
            self.y += self.speed

        self.direction = 'down'
        self.step += 1

    def left(self):
        if self.is_valid_location(self.x - self.speed, self.y):
            self.x -= self.speed
            
        self.direction = 'left'
        self.step += 1

    def right(self):
        if self.is_valid_location(self.x + self.speed, self.y):
            self.x += self.speed

        self.direction = 'right'
        self.step += 1
