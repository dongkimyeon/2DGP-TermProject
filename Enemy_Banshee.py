from Time import Time
from ResourceManager import ResourceManager
import pico2d
import SceneManager
import math
from Player import player
from Banshee_Attack_note import Note

class Banshee:
    def __init__(self):
        self.health = 50
        self.max_health = 50  # 최대 체력 추가
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
        self.detection_radius = 350
        self.attack_cooldown = 0.0
        self.note_fired = False
        self.direction = 1  # 1: 오른쪽, -1: 왼쪽
        self.map_manager = None  # 맵 매니저 참조

        self.shot_timer = 0.0
        self.shot_duration = 0.1

    def set_map_manager(self, map_manager):
        """맵 매니저 설정"""
        self.map_manager = map_manager

    def attack(self):
        return self.attack_power

    def take_damage(self, damage):
        self.health -= damage
        temp = self.state
        self.state = temp + '_shot'
        self.shot_timer = 0.0

    def get_bb(self):
        half_width = self.width // 2
        half_height = self.height // 2
        return (self.x - half_width, self.y - half_height + 7, self.x + half_width, self.y + half_height + 5)

    def get_damage(self):
        return self.attack_power

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

        dx = player.x - self.x
        dy = player.y - self.y

        angle = math.atan2(dy, dx)
        if (angle > math.pi / 2 or angle < -math.pi / 2):
            self.direction = -1
        else:
            self.direction = 1

        #플레이어 감지
        if(player.x - self.x)**2 + (player.y - self.y)**2 < self.detection_radius**2:
            if '_shot' not in self.state and self.state != 'attack' and self.state != 'attack_shot':
                self.state = 'attack'
                self.frame_count = 0
                self.note_fired = False
        # 프레임 애니메이션
        self.frame_timer += dt
        if self.frame_timer > 0.1:
            self.frame_count += 1
            self.frame_timer = 0.0
        # 공격 쿨타임 감소
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt




    def render(self, camera_x=0, camera_y=0, zoom=1.0):
        image, frame_count, width, height = ResourceManager.get_image(f"banshee_{self.state}")
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
            if self.state == 'attack' or self.state == 'attack_shot':
                if self.attack_cooldown <= 0:
                    if frame == frame_count - 1 and not self.note_fired:
                        # 16방향으로 Note 발사 (한 번만)
                        for i in range(16):
                            angle = (2 * math.pi / 16) * i
                            Note().shot(self.x, self.y, angle, 300)
                        self.note_fired = True
                        self.attack_cooldown = 3.0 # 쿨타임 리셋
                    if frame == frame_count - 1:
                        if '_shot' not in self.state:
                            self.state = 'idle'

        # 체력바 렌더링
        self.render_hp_bar(camera_x, camera_y, zoom)

    def render_hp_bar(self, camera_x=0, camera_y=0, zoom=1.0):
        """적 체력바 렌더링"""
        hp_bar_base, _, bar_width, bar_height = ResourceManager.get_image("enemy_hp_bar")
        hp_bar_gage, _, gage_width, gage_height = ResourceManager.get_image("enemy_hp_bar_gage")

        if not hp_bar_base or not hp_bar_gage:
            return

        # 체력바 위치
        bar_offset_y = -(int(self.height * 1.5) // 2 - 10)  # 하단으로 이동
        draw_x = int((self.x - camera_x) * zoom)
        draw_y = int((self.y - camera_y) * zoom) + int(bar_offset_y * zoom)

        # 체력 비율 계산
        hp_ratio = max(0, min(1, self.health / self.max_health))

        # 체력바 크기 증가 (1.5배)
        bar_scale = 2

        # 체력바 배경 렌더링
        hp_bar_base.draw(draw_x, draw_y, int(bar_width * zoom * bar_scale), int(bar_height * zoom))

        # 체력 게이지 렌더링 (비율만큼만 그리기)
        if hp_ratio > 0:
            # clip_draw로 비율만큼만 렌더링
            gage_draw_width = int(gage_width * hp_ratio)
            hp_bar_gage.clip_draw(0, 0, gage_draw_width, gage_height,
                                  draw_x - int((gage_width - gage_draw_width) / 2 * zoom * bar_scale),
                                  draw_y,
                                  int(gage_draw_width * zoom * bar_scale), int(gage_height * zoom))

    def is_dead(self):
        return self.health <= 0

    def handle_collision(self, group, other):
        """충돌 처리"""
        if group == 'katana_effect:banshee':
            # 카타나 이펙트와 충돌
            if other.can_hit(self):  # 아직 맞지 않았다면
                damage = other.get_damage()
                self.take_damage(damage)
                other.mark_hit(self)  # 맞은 것으로 표시
