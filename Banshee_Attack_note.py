from Time import Time
from ImageManager import ImageManager
import pico2d
import SceneManager
import math


class Note:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 35
        self.height = 35
        self.speed = 0
        self.direction = 0
        self.attack_power = 12
        self.frame_count = 0
        self.frame_timer = 0.0

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def get_bb(self):
        half_width = self.width // 2
        half_height = self.height // 2
        return (self.x - half_width, self.y - half_height + 2 , self.x + half_width - 5, self.y + half_height )

    def get_damage(self):
        return self.attack_power

    def shot(self, x, y, direction, speed=300):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        SceneManager.active_scene.gameobjs.append(self)
        return self

    def update(self):
        dt = Time.DeltaTime()
        # 이동
        self.x += math.cos(self.direction) * self.speed * dt
        self.y += math.sin(self.direction) * self.speed * dt
        # 프레임 애니메이션
        self.frame_timer += dt
        if self.frame_timer > 0.1:
            self.frame_count += 1
            self.frame_timer = 0.0

    def render(self):
        image, frame_count, width, height = ImageManager.get_image(f"note")
        frame = self.frame_count % frame_count
        if image:
            image.clip_draw(frame * width // frame_count, 0, width // frame_count, height, int(self.x),
                            int(self.y) + height // 2, self.width, self.height)
