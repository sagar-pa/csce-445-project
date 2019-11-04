class Sades:
    def __init__(self, x, y, speed):
        self.left_images = ['left-1.png', 'left-2.png', 'left-3.png']
        self.right_images = ['right-1.png', 'right-2.png', 'right-3.png']
        self.up_images = ['up-1.png', 'up-2.png', 'up-3.png']
        self.down_images = ['down-1.png', 'down-2.png', 'down-3.png']

        self.x = x
        self.y = y

        self.speed = speed