from Time import Time
from ImageManager import ImageManager
import pico2d
import SceneManager
import math


class Note:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.speed = 0
        self.direction = 0
        self.frame = 0
        self.frame_count = 0
        self.frame_timer = 0.0

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def shot(self):
        pass

    def update(self):
        pass

    def render(self):
        pass


