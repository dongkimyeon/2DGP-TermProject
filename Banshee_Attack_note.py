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

        self.frame_count = 0
        self.frame_timer = 0.0

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def shot(self):
        pass

    def update(self):
        dt = Time.DeltaTime()

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
        pass


