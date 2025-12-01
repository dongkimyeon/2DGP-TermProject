from Time import Time
from ResourceManager import ResourceManager
import pico2d
import SceneManager
import math

class Gun:
    def __init__(self, player):
        self.player = player
        self.x = player.x
        self.y = player.y
        self.image = None
        self.angle = 0.0

    def update(self):
        self.x = self.player.x
        self.y = self.player.y


    def render(self, camera_x=0, camera_y=0, zoom=1.0):
        ImageType = None
        if self.player.direction == 1:
            ImageType = "gun_right"
        else:
            ImageType = "gun_left"
        image, temp, width, height = ResourceManager.get_image(f"{ImageType}")
        scale = 2.0 * zoom
        draw_x = (self.x - camera_x) * zoom
        draw_y = (self.y - camera_y) * zoom
        image.rotate_draw(self.angle, draw_x, draw_y, int(width * scale), int(height * scale))
