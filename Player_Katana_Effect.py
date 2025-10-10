from pico2d import draw_rectangle

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
        self.width = 62
        self.height = 81
        self.special_attack = False
        self.special_attack_damage = 30
        self.default_damage = 10
        self.image = None


    def start(self):
        self.active = True
        if self.player.chargingGage >= self.player.max_chargingGage:
            self.special_attack = True
            self.player.chargingGage = 0.0
        else:
            self.special_attack = False

        self.frame_count = 0
        self.frame_timer = 0.0

    def get_bb(self):
        if  not self.active:
            return (0, 0, 0, 0)

        half_width = (self.width // 9) // 2
        half_height = self.height // 2
        if self.special_attack:
            return self.x - half_width*2, self.y - half_height *2, self.x + half_width*2, self.y + half_height*2
        else:
            return self.x - half_width, self.y - half_height, self.x + half_width, self.y + half_height

    def get_damage(self):
        if self.special_attack:
            return self.special_attack_damage
        else:
            return self.default_damage

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
        scale = 1.0
        if self.special_attack:
            self.image, frame_count, self.width, self.height = ImageManager.get_image("katana_effect_ex")
            scale = 2.0
        else:
            self.image, frame_count, self.width, self.height = ImageManager.get_image("katana_effect")
            scale = 1.0

        if self.player.direction == 1:
            self.image.clip_composite_draw(self.frame_count * (self.width // frame_count), 0, self.width // frame_count, self.height,
                                      self.angle, 'none', self.x, self.y, self.width // frame_count * scale, self.height * scale)
        else:
            self.image.clip_composite_draw(self.frame_count * (self.width // frame_count), 0, self.width // frame_count, self.height,
                                      self.angle, 'v', self.x, self.y, self.width // frame_count * scale, self.height * scale)
