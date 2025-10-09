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
        self.angle = 0.0

    def update(self):
        self.x = self.player.x
        self.y = self.player.y
        # 각도는 Player에서 직접 갱신됨

    def render(self):

        image, temp, width, height = ImageManager.get_image(f"katana")
        scale = 2.0
        # 마우스 방향으로 회전
        image.rotate_draw(self.angle, self.x, self.y, width * scale, height * scale)
