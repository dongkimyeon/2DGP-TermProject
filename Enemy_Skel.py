from Time import Time
from ResourceManager import ResourceManager
import pico2d
import SceneManager
import math
from Player import player



class Skel:
    def __init__(self):
        self.health = 50
        self.attack_power = 12
        self.x = 0
        self.y = 0
        self.moveSpeed = 100  # Sekl 이동 속도(초당 픽셀)
        self.frame = 0
        self.frame_count = 0
        self.frame_timer = 0.0
        self.direction = 1  # 1: 오른쪽, -1: 왼쪽
        self.state = 'move'  # 'move' , 'attack', 'idle', 'move_shot', 'attack_shot' , 'idle_shot'
        self.is_hit = False
        self.is_dead = False
        self.width = 50
        self.height = 50
        self.detection_radius = 350
        self.attack_radius = 50
        self.attack_cooldown = 0.0  # 쿨타임 1초
        self.is_attacking = False  # 공격 애니메이션 진행 중 여부
        self.attack_frame_max = 0  # 공격 애니메이션 프레임 수
        self.attack_direction = 1  # 공격 시작 시 방향 고정용
        self.map_manager = None  # 맵 매니저 참조
        self.attack_hit_applied = False

        self.shot_timer = 0.0
        self.shot_duration = 0.1

    def set_map_manager(self, map_manager):
        """맵 매니저 설정"""
        self.map_manager = map_manager

    def attack(self):
        return self.attack_power

    def move(self):
        #플레이어 방향으로 이동
        dx = player.x - self.x
        dy = player.y - self.y
        angle = math.atan2(dy, dx)
        if( angle > math.pi/2 or angle < -math.pi/2):
            self.direction = -1
        else:
            self.direction = 1
        self.x += math.cos(angle) * self.moveSpeed * Time.DeltaTime()
        # 공격 상태 진입 조건
        if (player.x - self.x) ** 2 + (player.y - self.y) ** 2 < self.attack_radius ** 2 and not self.is_attacking:
            self.state = 'attack'
            self.is_attacking = True
            self.attack_direction = self.direction
            # 공격 애니메이션 프레임 수 저장
            _, frame_count, _, _ = ResourceManager.get_image(f"skel_attack")
            self.attack_frame_max = frame_count
            self.frame_count = 0



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

        # 공격 중이 아닐 때만 방향 업데이트
        if not self.is_attacking:
            dx = player.x - self.x
            dy = player.y - self.y
            angle = math.atan2(dy, dx)
            if (angle > math.pi / 2 or angle < -math.pi / 2):
                self.direction = -1
            else:
                self.direction = 1
        else:
            # 공격 중일 때는 공격 시작 시의 방향 유지
            self.direction = self.attack_direction

        # 공격 중이면 애니메이션 끝날 때까지 상태 유지
        if self.is_attacking:
            if '_shot' not in self.state:
                self.state = 'attack'
            # 공격 애니메이션 3번째 프레임(인덱스 2)에서 플레이어와 충돌 체크
            current_frame = self.frame_count % self.attack_frame_max if self.attack_frame_max > 0 else 0
            if current_frame == 2 and not self.attack_hit_applied:
                # 플레이어와 충돌 체크
                left_a, bottom_a, right_a, top_a = player.get_bb()
                left_b, bottom_b, right_b, top_b = self.get_bb()

                # 충돌 확인
                if not (left_a > right_b or right_a < left_b or top_a < bottom_b or bottom_a > top_b):
                    print(f"Skel이 플레이어를 공격! 데미지: {self.attack_power}")
                    player.hp -= self.attack_power
                    self.attack_hit_applied = True
        else:
            # 플레이어 감지
            if (player.x - self.x) ** 2 + (player.y - self.y) ** 2 < self.detection_radius ** 2:
                if '_shot' not in self.state:
                    self.state = 'move'
                self.move()
            else:
                if '_shot' not in self.state:
                    self.state = 'idle'

        # 프레임 애니메이션
        self.frame_timer += dt
        if self.frame_timer > 0.1:
            self.frame_count += 1
            self.frame_timer = 0.0
            # 공격 애니메이션이 끝나면 상태 복귀
            if self.is_attacking and self.frame_count >= self.attack_frame_max:
                self.is_attacking = False
                self.attack_hit_applied = False  # 히트 플래그 리셋
                # 공격 후 플레이어 위치에 따라 상태 결정
                if '_shot' not in self.state:
                    if (player.x - self.x) ** 2 + (player.y - self.y) ** 2 < self.detection_radius ** 2:
                        self.state = 'move'
                    else:
                        self.state = 'idle'

    def render(self, camera_x=0, camera_y=0, zoom=1.0):
        image, frame_count, width, height = ResourceManager.get_image(f"skel_{self.state}")
        if frame_count == 0:
            return
        frame = self.frame_count % frame_count
        draw_x = int((self.x - camera_x) * zoom)
        draw_y = int((self.y - camera_y) * zoom) + int(height // 2 * zoom)
        if image:
            if self.direction == 1:
                if self.state == 'attack' or self.state == 'attack_shot':
                    image.clip_draw(frame * width // frame_count, 0, width // frame_count, height,
                                    int(draw_x + 22 * 1.5 * zoom), int(draw_y + 15 * zoom), int((self.width * 2.0) * 1.5 * zoom), int((self.height * 1.6) * 1.5 * zoom))
                else:
                    image.clip_draw(frame * width // frame_count, 0, width // frame_count, height,
                                    draw_x, draw_y, int(self.width * 1.5 * zoom), int(self.height * 1.5 * zoom))
            else:
                if self.state == 'attack' or self.state == 'attack_shot':
                    image.clip_composite_draw(frame * width // frame_count, 0, width // frame_count, height, 0, 'h',
                                              int(draw_x - 22 * 1.5 * zoom), int(draw_y + 15 * zoom), int((self.width * 2.0) * 1.5 * zoom), int((self.height * 1.6) * 1.5 * zoom))
                else:
                    image.clip_composite_draw(frame * width // frame_count, 0, width // frame_count, height, 0, 'h',
                                          draw_x, draw_y, int(self.width * 1.5 * zoom), int(self.height * 1.5 * zoom))
    def is_dead(self):
        return self.health <= 0

    def handle_collision(self, group, other):
        if group == 'katana_effect:skel':
            # 카타나 이펙트와 충돌
            if other.can_hit(self):  # 아직 맞지 않았다면
                damage = other.get_damage()
                self.take_damage(damage)
                other.mark_hit(self)  # 맞은 것으로 표시
                print(f"스켈이 {damage} 데미지를 받았습니다! 남은 체력: {self.health}")
