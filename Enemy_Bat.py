from Time import Time
from ResourceManager import ResourceManager
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
        self.state = 'idle'  # 'idle' , 'move', 'shot'
        self.is_hit = False
        self.is_dead = False
        self.width = 50
        self.height = 50
        self.detection_radius = 350  # 플레이어 감지 범위
        self.attack_cooldown = 0.0  # 쿨타임 1초
        self.direction = 1
        self.map_manager = None  # 맵 매니저 참조
        self.player_detected = False  # 플레이어를 감지했는지 여부

        self.shot_timer = 0.0
        self.shot_duration = 0.1

    def set_map_manager(self, map_manager):
        """맵 매니저 설정"""
        self.map_manager = map_manager

    def attack(self):
        return self.attack_power

    def move(self):
        dx = player.x - self.x
        dy = player.y - self.y
        dist2 = dx * dx + dy * dy
        min_dist2 = self.min_distance ** 2
        max_dist2 = self.detection_radius ** 2
        dt = Time.DeltaTime()
        angle = math.atan2(dy, dx)
        if( angle > math.pi/2 or angle < -math.pi/2):
            self.direction = -1
        else:
            self.direction = 1

        # 플레이어 감지 체크
        if not self.player_detected and dist2 < max_dist2:
            self.player_detected = True
            if '_shot' not in self.state:
                self.state = 'move'
            print(f"Bat detected player at distance: {math.sqrt(dist2)}")

        # 플레이어를 감지한 경우에만 이동
        if self.player_detected:
            # 이동할 위치 계산
            new_x = self.x
            new_y = self.y

            if dist2 < min_dist2:
                # 너무 가까우면 멀어짐
                new_x = self.x - math.cos(angle) * self.moveSpeed * dt
                new_y = self.y - math.sin(angle) * self.moveSpeed * dt
            elif dist2 > max_dist2:
                # 너무 멀면 가까이 감
                new_x = self.x + math.cos(angle) * self.moveSpeed * dt
                new_y = self.y + math.sin(angle) * self.moveSpeed * dt
            else:
                # 적당한 거리에서 천천히 이동
                new_x = self.x + math.cos(angle) * 50 * dt
                new_y = self.y + math.sin(angle) * 50 * dt

            # 벽 충돌 체크 후 위치 업데이트
            final_x, final_y = self.check_wall_collision(new_x, new_y)
            self.x = final_x
            self.y = final_y

    def check_wall_collision(self, new_x, new_y):
        """벽 충돌 체크 및 위치 보정"""
        if not self.map_manager:
            return new_x, new_y

        half_width = self.width // 2
        half_height = self.height // 2

        # 현재 위치의 충돌 박스
        old_left = self.x - half_width
        old_right = self.x + half_width
        old_bottom = self.y - half_height + 7
        old_top = self.y + half_height + 5

        # 새 위치에서의 충돌 박스
        left = new_x - half_width
        bottom = new_y - half_height + 7
        right = new_x + half_width
        top = new_y + half_height + 5

        # 충돌하는 타일들 가져오기
        colliding_tiles = self.map_manager.check_collision(left, bottom, right, top)

        # Y축 충돌 처리 먼저
        for tile in colliding_tiles:
            x_overlap = (old_left < tile['right'] and old_right > tile['left'])

            if x_overlap:
                # 수직 충돌 처리 (Y축)
                if old_top <= tile['bottom'] and top > tile['bottom']:
                    # 위에서 타일에 부딪힘 (천장)
                    new_y = tile['bottom'] - half_height - 5
                elif old_bottom >= tile['top'] and bottom < tile['top']:
                    # 아래에서 타일에 부딪힘 (바닥)
                    new_y = tile['top'] + half_height - 7

        # Y축 처리 후 업데이트된 위치로 X축 충돌 체크
        left = new_x - half_width
        bottom = new_y - half_height + 7
        right = new_x + half_width
        top = new_y + half_height + 5

        colliding_tiles_x = self.map_manager.check_collision(left, bottom, right, top)

        for tile in colliding_tiles_x:
            # Y축 오버랩 체크
            y_overlap = (bottom < tile['top'] and top > tile['bottom'])

            if y_overlap:
                # 수평 충돌 처리
                if old_right <= tile['left'] and right > tile['left']:
                    # 왼쪽 벽에 부딪힘
                    new_x = tile['left'] - half_width - 0.1
                elif old_left >= tile['right'] and left < tile['right']:
                    # 오른쪽 벽에 부딪힘
                    new_x = tile['right'] + half_width + 0.1

        return new_x, new_y

    def get_damage(self):
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

        # 플레이어 감지 및 발사 (감지된 경우에만)
        if self.player_detected:
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

    def render(self, camera_x=0, camera_y=0, zoom=1.0):
        image, frame_count, width, height = ResourceManager.get_image(f"bat_{self.state}")
        if frame_count == 0:
            return
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
        """충돌 처리"""
        if group == 'katana_effect:bat':
            # 카타나 이펙트와 충돌
            if other.can_hit(self):  # 아직 맞지 않았다면
                damage = other.get_damage()
                self.take_damage(damage)
                other.mark_hit(self)  # 맞은 것으로 표시
                print(f"박쥐가 {damage} 데미지를 받았습니다! 남은 체력: {self.health}")
