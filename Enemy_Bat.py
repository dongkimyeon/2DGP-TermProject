from Time import Time
from ImageManager import ImageManager
import pico2d
import SceneManager
import math
from Player import player
from Bat_Attack_bullet import Bullet


class Bat:
    def __init__(self):
        self.health = 50
        self.attack_power = 12
        self.x = 0
        self.y = 0
        self.moveSpeed = 70  # Bat의 이동 속도(초당 픽셀)
        self.min_distance = 200  # 너무 가까울 때의 최소 거리
        self.frame = 0
        self.frame_count = 0
        self.frame_timer = 0.0
        self.state = 'move'  # 항상 move 상태
        self.is_hit = False
        self.is_dead = False
        self.width = 50
        self.height = 50
        self.detection_radius = 350
        self.attack_cooldown = 0.0  # 쿨타임 1초

    def attack(self):
        return self.attack_power

    def move(self):
        dx = player.x - self.x
        dy = player.y - self.y
        dist2 = dx * dx + dy * dy
        min_dist2 = self.min_distance ** 2
        max_dist2 = self.detection_radius ** 2
        dt = Time.DeltaTime()
        if dist2 < min_dist2:
            # 너무 가까우면 멀어짐
            angle = math.atan2(dy, dx)
            self.x -= math.cos(angle) * self.moveSpeed * dt
            self.y -= math.sin(angle) * self.moveSpeed * dt
        elif dist2 > max_dist2:
            # 너무 멀면 다가감
            angle = math.atan2(dy, dx)
            self.x += math.cos(angle) * self.moveSpeed * dt
            self.y += math.sin(angle) * self.moveSpeed * dt
        else:
            # 적당한 거리
            angle = math.atan2(dy, dx)
            self.x += math.cos(angle) * 50 * dt
            self.y += math.sin(angle) * 50 * dt



    def take_damage(self, damage):
        self.health -= damage

    def get_bb(self):
        half_width = self.width // 2
        half_height = self.height // 2
        return (self.x - half_width, self.y - half_height + 7, self.x + half_width, self.y + half_height + 5)

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        dt = Time.DeltaTime()

        self.move()

        # 플레이어 감지 및 발사
        dx = player.x - self.x
        dy = player.y - self.y
        dist2 = dx * dx + dy * dy
        if dist2 < self.detection_radius ** 2:
            if self.attack_cooldown <= 0:
                direction = math.atan2(dy, dx)
                Bullet().shot(self.x, self.y, direction, 300)
                self.attack_cooldown = 2.0  # 쿨타임 리셋
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt
        # 프레임 애니메이션
        self.frame_timer += dt
        if self.frame_timer > 0.1:
            self.frame_count += 1
            self.frame_timer = 0.0

    def render(self):
        image, frame_count, width, height = ImageManager.get_image(f"bat_move")
        frame = self.frame_count % frame_count
        if image:
            image.clip_draw(frame * width // frame_count, 0, width // frame_count, height, int(self.x), int(self.y) + height // 2, self.width, self.height)

    def is_dead(self):
        return self.health <= 0
