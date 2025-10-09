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
        self.attack_cooldown = 0.5
        self.image = None

    def update(self):
        self.x = self.player.x
        self.y = self.player.y

    def render(self):
        image, temp, width, height = ImageManager.get_image(f"katana")
        scale = 2.0
        if self.player.direction == 1:
            image.draw(self.x, self.y, width * scale, height *scale)
        else:
            image.composite_draw(0, 'h', self.x, self.y, width * scale, height * scale)
            pass
