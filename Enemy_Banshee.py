from Time import Time
from ImageManager import ImageManager
import pico2d
import SceneManager
import math


class Banshee:
    def __init__(self):
        self.health = 50
        self.attack_power = 12
        self.x = 0
        self.y = 0
        self.frame = 0
        self.frame_count = 0
        self.frame_timer = 0.0
        self.state = 'idle'  # 'idle', 'attack', 'hit'
        self.is_hit = False
        self.is_dead = False
        self.width = 50
        self.height = 50
        self.detection_radius = 200
        self.attack_cooldown = 2.0

    def attack(self):
        return self.attack_power

    def take_damage(self, damage):

        self.health -= damage

    def set_position(self, x, y):
        self.x = x
        self.y = y
    def update(self):
        dt = Time.DeltaTime()

        # 프레임 애니메이션
        self.frame_timer += dt
        if self.frame_timer > 0.1:
            self.frame_count += 1
            self.frame_timer = 0.0

    def render(self):
        image, frame_count, width, height = ImageManager.get_image(f"banshee_{self.state}")
        frame = self.frame_count % frame_count
        if image:
            image.clip_draw(frame * width // frame_count, 0, width // frame_count, height, int(self.x), int(self.y) + height // 2, self.width, self.height)
        pass

    def is_dead(self):
        return self.health <= 0
