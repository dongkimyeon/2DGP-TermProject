from Player_Katana import Katana
from ImageManager import ImageManager
import pico2d
from Time import Time
import math

class KatanaEffect:
    def __init__(self, player):
        self.player = player
        self.x = player.x
        self.y = player.y
        self.frame_count = 0
        self.frame_timer = 0.0
        self.frame_duration = 0.05  # 프레임 전환 시간
        self.active = False
        self.angle = 0.0

    def start(self):
        self.active = True
        self.frame_count = 0
        self.frame_timer = 0.0

    def update(self):
        if not self.active:
            return

        dt = Time.DeltaTime()
        self.frame_timer += dt

        if self.frame_timer >= self.frame_duration:
            self.frame_timer -= self.frame_duration
            self.frame_count += 1
            if self.frame_count >= 9:  # 프레임 수에 맞게 조정
                self.active = False

        # 위치와 각도 갱신
        offset_radius = 40
        angle = self.player.weapon.angle  # 라디안 값
        self.x = self.player.x + offset_radius * math.cos(angle)
        self.y = self.player.y + offset_radius * math.sin(angle)
        self.angle = angle

    def render(self):
        if not self.active:
            return
        image, frame_count, width, height = ImageManager.get_image("katana_effect")
        if self.player.direction == 1:
            image.clip_composite_draw(self.frame_count * (width // frame_count), 0, width // frame_count, height,
                                      self.angle, 'none', self.x, self.y, width // frame_count, height)
        else:
            image.clip_composite_draw(self.frame_count * (width // frame_count), 0, width // frame_count, height,
                                      self.angle, 'v', self.x, self.y, width // frame_count, height)

