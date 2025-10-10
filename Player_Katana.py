from Time import Time
from ImageManager import ImageManager
import pico2d
import SceneManager
import math

class Katana:
    def __init__(self, player):
        self.player = player
        self.x = player.x
        self.y = player.y
        self.image = None
        self.angle = 0.0

    def update(self):
        self.x = self.player.x
        self.y = self.player.y


    def render(self):
        ImageType = None
        if self.player.direction == 1:
            ImageType = "katana_right"
        else:
            ImageType = "katana_left"
        image, temp, width, height = ImageManager.get_image(f"{ImageType}")
        scale = 2.0
        if self.player.direction == 1:
            image.rotate_draw(self.angle, self.x, self.y, width * scale, height * scale)
        else:
            image.rotate_draw(self.angle, self.x, self.y, width * scale, height * scale)

