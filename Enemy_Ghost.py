from Time import Time
from ResourceManager import ResourceManager
import pico2d
import SceneManager
import math
from Player import player



class Ghost:
    def __init__(self):
        self.health = 50
        self.attack_power = 12
        self.x = 0
        self.y = 0
        self.moveSpeed = 150  # Ghost의 이동 속도(초당 픽셀)

        self.frame = 0
        self.frame_count = 0
        self.frame_timer = 0.0
        self.direction = 1  # 1: 오른쪽, -1: 왼쪽
        self.state = 'move'  # 'move' , 'attack', 'attack_shot', 'move_shot'
        self.is_hit = False
        self.is_dead = False
        self.width = 50
        self.height = 50
        self.detection_radius = 350
        self.attack_cooldown = 0.0  # 쿨타임 1초
        self.map_manager = None  # 맵 매니저 참조

        self.shot_timer = 0.0
        self.shot_duration = 1.0

    def set_map_manager(self, map_manager):
        """맵 매니저 설정"""
        self.map_manager = map_manager

    def attack(self):
        return self.attack_power

    def move(self):
        dx = player.x - self.x
        dy = player.y - self.y

        if (player.x - self.x) ** 2 + (player.y - self.y) ** 2 < self.detection_radius ** 2:
            self.state = 'attack'
            angle = math.atan2(dy, dx)
            if(angle > math.pi/2 or angle < -math.pi/2):
                self.direction = -1
            else:
                self.direction = 1
            self.x += math.cos(angle) * self.moveSpeed * Time.DeltaTime()
            self.y += math.sin(angle) * self.moveSpeed * Time.DeltaTime()
        else:
            self.state = 'move'

    def take_damage(self, damage):
        self.health -= damage
        temp = self.state
        self.state = temp + '_shot'
        self.shot_timer = 0.0

    def get_damage(self):
        return self.attack_power

    def get_bb(self):
        half_width = self.width // 2
        half_height = self.height // 2
        return (self.x - half_width, self.y - half_height + 7, self.x + half_width, self.y + half_height + 5)

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        dt = Time.DeltaTime()

        # shot 타이머 업데이트 및 상태 해제
        if '_shot' in self.state:
            self.shot_timer += dt
            if self.shot_timer >= self.shot_duration:
                self.state = self.state.replace('_shot', '')
                self.shot_timer = 0.0

        self.move()
        # 프레임 애니메이션
        self.frame_timer += dt
        if self.frame_timer > 0.1:
            self.frame_count += 1
            self.frame_timer = 0.0

    def render(self, camera_x=0, camera_y=0, zoom=1.0):
        image, frame_count, width, height = ResourceManager.get_image(f"ghost_{self.state}")
        frame = self.frame_count % frame_count
        draw_x = int((self.x - camera_x) * zoom)
        draw_y = int((self.y - camera_y) * zoom) + int(height // 2 * zoom)
        draw_w = int(self.width * zoom)
        draw_h = int(self.height * zoom)
        if image:
            if self.direction == 1:
                image.clip_draw(frame * width // frame_count, 0, width // frame_count, height, draw_x,
                                draw_y, draw_w, draw_h)
            else:
                image.clip_composite_draw(frame * width // frame_count, 0, width // frame_count, height, 0, 'h',
                                          draw_x, draw_y, draw_w, draw_h)
    def is_dead(self):
        return self.health <= 0

    def handle_collision(self, group, other):
        if group == 'katana_effect:ghost':
            if other.can_hit(self):
                damage = other.get_damage()
                self.take_damage(damage)
                other.mark_hit(self)
