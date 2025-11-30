from ResourceManager import ResourceManager
from Time import Time
from Player import player
from IceBullet import IceBullet
from Icicle import Icicle
from IceSpear import IceSpear
import SceneManager
import math
import random



class Boss:
    def __init__(self, x, y):
        self.max_health = 100
        self.health = self.max_health
        self.x = x
        self.y = y
        self.frame = 0
        self.frame_count = 0
        self.frame_timer = 0.0
        self.state = 'enter' # 'idle', 'attack', 'die', 'enter'
        self.pattern = 'none' # 'ice_bullet', 'ice_spear' , 'icicle_fall'
        self.dir = 0 # 1: right, -1: left
        self.is_hit = False
        self.width = 68
        self.height = 60

        self.attack_timer = 0.0

        self.has_shot = False

        # idle 시 한 번 이동 관련 변수
        self.is_moving = False
        self.move_target_x = self.x
        self.move_target_y = self.y
        self.move_speed = 400.0
        self.move_distance = 400.0

        self.max_distance_from_player = 500.0
        self.has_moved = False

        self.font = ResourceManager.get_font("default")
        self.map_manager = None  # 맵 매니저 참조

    def set_map_manager(self, map_manager):
        """맵 매니저 설정"""
        self.map_manager = map_manager

    def get_bb(self):
        half_width = self.width // 2
        half_height = self.height // 2
        return self.x - half_width, self.y - half_height + 7, self.x + half_width, self.y + half_height + 5
    def take_damage(self, damage):
        self.health -= damage

    def start_idle_movement(self, player_x, player_y):
        # 범위(move_distance) 내에서 랜덤한 좌표를 목표로 설정
        # 랜덤 반경과 각도를 선택
        rand_r = random.uniform(0, self.move_distance)
        rand_theta = random.uniform(0, math.tau)
        target_x = self.x + math.cos(rand_theta) * rand_r
        target_y = self.y + math.sin(rand_theta) * rand_r

        # 맵 경계 처리: SceneManager.active_scene.map_manager 사용
        try:
            mm = SceneManager.active_scene.map_manager
            min_x = mm.TILE_SIZE / 2.0
            min_y = mm.TILE_SIZE / 2.0
            max_x = mm.GRID_WIDTH * mm.TILE_SIZE - mm.TILE_SIZE / 2.0
            max_y = mm.GRID_HEIGHT * mm.TILE_SIZE - mm.TILE_SIZE / 2.0
        except Exception:
            # 안전망: 화면 크기 기반 제한
            min_x = 0
            min_y = 0
            max_x = SceneManager.screen_width
            max_y = SceneManager.screen_height

        # 클램핑
        target_x = max(min_x, min(max_x, target_x))
        target_y = max(min_y, min(max_y, target_y))

        # 목표 설정 및 상태 초기화
        self.move_target_x = target_x
        self.move_target_y = target_y
        self.is_moving = True
        self.has_moved = False

    def update(self):
        dt = Time.DeltaTime()

        if self.health <= 0:
            self.state = 'die'
        if self.state == 'die':
            if self.frame_count >= 29:
                self.frame_count = 29
                return


        dx = player.x - self.x
        dy = player.y - self.y
        angle = math.atan2(dy, dx)
        if angle > math.pi / 2 or angle < -math.pi / 2:
            self.dir = -1
        else:
            self.dir = 1

        prev_state = self.state

        #enter -> idle
        if self.state == 'enter':
            if self.frame_count >= 16:
                self.state = 'idle'
                self.frame_count = 0
        #idle -> attack
        elif self.state == 'idle':
            if self.attack_timer > 3.0:
                self.state = 'attack'
                self.frame_count = 0
                self.attack_timer = 0.0
                # 공격 시작 시 발사 플래그 리셋
                self.has_shot = False
                # 이동 동작이 있으면 중단
                self.is_moving = False
                self.has_moved = False

        #attack -> idle
        elif self.state == 'attack':
            # 프레임 타이밍에 맞춰 아이스불렛 발사 (부채꼴 5발, 한 번만)
            if self.frame_count == 6 and not self.has_shot:

                # 랜덤 패턴 선택
                import random
                self.pattern = random.choice(['ice_bullet', 'ice_spear', 'icicle_fall'])
                self.pattern = 'ice_bullet' # 디버그용 고정 패턴
                if self.pattern == 'ice_bullet':
                    # # 총알 개수와 스프레드 각도(라디안)
                    count = 5
                    step_deg = 10  # 각 탄 사이의 간격(도)
                    half_span = (step_deg * (count - 1)) / 2.0
                    # 생성
                    for i in range(count):
                        offset_deg = -half_span + i * step_deg
                        offset_rad = math.radians(offset_deg)
                        bullet_angle = angle + offset_rad
                        IceBullet().shot(self.x, self.y, bullet_angle)

                    pass
                if self.pattern == 'ice_spear':
                    # 맵의 양끝에서 창이 좌우로 날아오는 패턴
                    count = 4
                    y_offset = 200  # 총알 간격 (픽셀)
                    # 랜덤으로 스타트 지점 100 or 200
                    import random
                    random_start = random.choice([1, 2])
                    start_x = 0
                    if random_start == 1:
                        start_x = 50
                    else:
                        start_x = 1250

                    start_y = 70
                    for i in range(count):
                        IceSpear().shot(start_x, start_y)
                        start_y = start_y + y_offset


                if self.pattern == 'icicle_fall':
                    # 맵의 상단에서 아래로 얼음 조각이 떨어지는 패턴
                    count = 6
                    x_offset = 200  # 총알 간격 (픽셀)
                    # 랜덤으로 스타트 지점 100 or 200
                    import random
                    random_start = random.choice([1, 2])
                    start_x = random_start * 100
                    for i in range(count):
                        Icicle().shot(start_x)
                        start_x = start_x + x_offset
                    # self.has_shot = True

                self.has_shot = True

            if self.frame_count >= 11:
                self.state = 'idle'
                self.frame_count = 0
                self.attack_timer = 0.0
                # 공격 종료 시 플래그 리셋
                self.has_shot = False

        # 상태 변경 감지
        if prev_state != 'idle' and self.state == 'idle':
            self.start_idle_movement(player.x, player.y)

        # 이동 처리
        if self.is_moving:
            tx = self.move_target_x - self.x
            ty = self.move_target_y - self.y
            dist = math.hypot(tx, ty)
            if dist < 1.0:
                # 도착
                self.x = self.move_target_x
                self.y = self.move_target_y
                self.is_moving = False
                self.has_moved = True
            else:
                # 이동 방향 단위 벡터
                nx = tx / dist
                ny = ty / dist
                move_step = self.move_speed * dt

                if move_step >= dist:
                    self.x = self.move_target_x
                    self.y = self.move_target_y
                    self.is_moving = False
                    self.has_moved = True
                else:
                    self.x += nx * move_step
                    self.y += ny * move_step




        self.frame_timer += dt
        self.attack_timer += dt
        if self.frame_timer > 0.1:
            self.frame_count += 1
            self.frame_timer = 0.0


    def render(self, camera_x=0, camera_y=0, zoom=1.0):
        image, frame_count, width, height = ResourceManager.get_image(f"niflheim_{self.state}")
        # frame_count가 0인 경우를 안전 처리
        frame_count = max(1, frame_count)
        frame = self.frame_count % frame_count
        draw_x = int((self.x - camera_x) * zoom)
        draw_y = int((self.y - camera_y) * zoom) + int(height // 2 * zoom) - 10
        draw_w = int(self.width * zoom)
        draw_h = int(self.height * zoom)
        self.font.draw(10, 30, f'HP: {self.health}', (255, 0, 0))

        if image:
            if self.dir == 1:
                image.clip_draw(frame * width // frame_count, 0, width // frame_count, height, draw_x,
                                draw_y, draw_w, draw_h)
            else:
                image.clip_composite_draw(frame * width // frame_count, 0, width // frame_count, height, 0, 'h',
                                          draw_x, draw_y, draw_w, draw_h)


    def handle_collision(self, group, other):
        """충돌 처리: 카타나 이펙트와의 충돌을 처리합니다."""
        # 카타나 이펙트와 충돌한 경우 처리
        if group == 'katana_effect:boss':
            # 아직 해당 공격에 맞지 않았다면 데미지 적용
            try:
                if other.can_hit(self):
                    damage = other.get_damage()
                    self.take_damage(damage)
                    other.mark_hit(self)
            except Exception:
                # 안전망: other 객체에 해당 메서드가 없을 경우 무시
                pass

