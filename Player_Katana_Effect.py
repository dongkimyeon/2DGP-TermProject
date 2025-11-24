from pico2d import draw_rectangle

from Player_Katana import Katana
from ResourceManager import ResourceManager
import pico2d
from Time import Time
import math
import random

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
        self.special_attack_damage = 25  # 차지 공격 데미지 20 ~ 25
        self.default_damage = 13  # 기본 공격 데미지 10 ~ 13
        self.image = None
        self.hit_enemies = set()  # 이번 공격에서 이미 맞은 적들을 추적
        #기본 공격 데미지 10 ~ 13
        #차지 공격 데미지 20 ~ 25

    def start(self):
        self.active = True
        self.hit_enemies.clear()  # 새 공격 시작 시 히트 리스트 초기화
        if self.player.chargingGage >= self.player.max_chargingGage:
            self.special_attack = True
            self.player.chargingGage = 0.0
        else:
            self.special_attack = False

        self.frame_count = 0
        self.frame_timer = 0.0

    def get_bb(self):
        if not self.active:
            return (0, 0, 0, 0)

        half_width = (self.width // 9) // 2
        half_height = self.height // 2
        if self.special_attack:
            return self.x - half_width*2, self.y - half_height *2, self.x + half_width*2, self.y + half_height*2
        else:
            return self.x - half_width, self.y - half_height, self.x + half_width, self.y + half_height

    def get_damage(self):
        # 랜덤 데미지 적용
        if self.special_attack:
            return random.randint(20, 25)  # 풀차지: 20~25
        else:
            return random.randint(10, 13)  # 기본: 10~13

    def can_hit(self, enemy):
        return id(enemy) not in self.hit_enemies

    def mark_hit(self, enemy):
        self.hit_enemies.add(id(enemy))

    def update(self):
        if not self.active:
            return

        dt = Time.DeltaTime()
        # 애니메이션 속도는 고정 (공격속도에 영향받지 않음)
        self.frame_timer += dt

        if self.frame_timer >= self.frame_duration:
            self.frame_timer -= self.frame_duration
            self.frame_count += 1
            if self.frame_count >= 9:  # 프레임 수에 맞게 조정
                self.active = False
                self.hit_enemies.clear()  # 공격 종료 시 히트 리스트 초기화

        # 위치와 각도 갱신
        offset_radius = 40
        angle = self.player.weapon.angle  # 라디안 값
        self.x = self.player.x + offset_radius * math.cos(angle)
        self.y = self.player.y + offset_radius * math.sin(angle)
        self.angle = angle

    def render(self, camera_x=0, camera_y=0, zoom=1.0):
        if not self.active:
            return
        scale = 1.0 * zoom
        if self.special_attack:
            self.image, frame_count, self.width, self.height = ResourceManager.get_image("katana_effect_ex")
            scale = 2.0 * zoom
        else:
            self.image, frame_count, self.width, self.height = ResourceManager.get_image("katana_effect")
            scale = 1.0 * zoom

        draw_x = (self.x - camera_x) * zoom
        draw_y = (self.y - camera_y) * zoom
        draw_w = int(self.width // frame_count * scale)
        draw_h = int(self.height * scale)
        if self.player.direction == 1:
            self.image.clip_composite_draw(self.frame_count * (self.width // frame_count), 0, self.width // frame_count, self.height,
                                      self.angle, 'none', draw_x, draw_y, draw_w, draw_h)
        else:
            self.image.clip_composite_draw(self.frame_count * (self.width // frame_count), 0, self.width // frame_count, self.height,
                                      self.angle, 'v', draw_x, draw_y, draw_w, draw_h)
