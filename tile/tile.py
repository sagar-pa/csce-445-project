import pygame

class Tile:
    def __init__(self, filename, screen):
        self.screen = screen
        self.surface = self.get_surface(filename)

    def get_surface(self, filename):
        f = open(filename)
        lines = f.readlines()
        f.close()

        colors = []
        for line in lines:
            current = []

            current = line.split(',')
            if not current[-1].strip():
                current = current[:-1]

            current = [int_to_rgb(int(x)) for x in current]
            colors.append(current)

        print colors

        width = len(colors[0])
        height = len(colors)
        surface = pygame.Surface((width, height))

        for j in range(len(colors)):
            for i in range(len(colors[0])):
                surface.set_at((i, j), colors[j][i])

        return surface

    def draw(self, x, y):
        self.screen.blit(self.surface, (x, y))

def int_to_rgb(num):
    return (num & 255, (num >> 8) & 255, (num >> 16) & 255)
