from ResourceManager import ResourceManager
from Time import Time
from Player import player
from IceBullet import IceBullet
from Icicle import Icicle
from IceSpear import IceSpear
import SceneManager
import math
import random
import pico2d


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

        self.enterSound = pico2d.load_wav('resources/sound/niflheim/niflheim_start.wav')
        self.enterSound.set_volume(32)
        self.icebulletSound = pico2d.load_wav('resources/sound/niflheim/ice_blast_projectile_spell_02.wav')
        self.icebulletSound.set_volume(32)
        self.icespearSound = pico2d.load_wav('resources/sound/niflheim/ice_spell_forming_shards_03.wav')
        self.icespearSound.set_volume(32)
        self.iciclefallSound = pico2d.load_wav('resources/sound/niflheim/ice_spell_freeze_small_04.wav')
        self.iciclefallSound.set_volume(32)


        self.enter_sound_played = False

    def set_map_manager(self, map_manager):
        """맵 매니저 설정"""
        self.map_manager = map_manager

    def get_bb(self):
        half_width = self.width // 2
        half_height = self.height // 2
        return self.x - half_width, self.y - half_height + 7, self.x + half_width, self.y + half_height + 5
    def take_damage(self, damage):
        # die 상태일 때는 데미지를 받지 않음
        if self.state == 'die':
            return
        self.health -= damage
        # 체력이 0 이하가 되면 die 상태로 전환
        if self.health <= 0:
            self.health = 0
            self.state = 'die'
            self.frame_count = 0
            self.is_moving = False
            self.has_moved = True

    def start_idle_movement(self, player_x, player_y):
        # 플레이어와의 거리에 따라 이동 목표 설정, 충돌 타일 피함
        try:
            mm = SceneManager.active_scene.map_manager
        except:
            mm = None

        dist_to_player = math.hypot(player_x - self.x, player_y - self.y)
        if dist_to_player > self.max_distance_from_player:
            # 플레이어에게 가까워지도록 이동
            angle_to_player = math.atan2(player_y - self.y, player_x - self.x)
            target_dist = min(dist_to_player - self.max_distance_from_player + random.uniform(0, 100), self.move_distance)
            target_x = self.x + math.cos(angle_to_player) * target_dist
            target_y = self.y + math.sin(angle_to_player) * target_dist
        else:
            # 랜덤 이동
            rand_r = random.uniform(0, self.move_distance)
            rand_theta = random.uniform(0, math.tau)
            target_x = self.x + math.cos(rand_theta) * rand_r
            target_y = self.y + math.sin(rand_theta) * rand_r

        # 맵 경계 처리
        if mm:
            min_x = mm.TILE_SIZE / 2.0
            min_y = mm.TILE_SIZE / 2.0
            max_x = mm.GRID_WIDTH * mm.TILE_SIZE - mm.TILE_SIZE / 2.0
            max_y = mm.GRID_HEIGHT * mm.TILE_SIZE - mm.TILE_SIZE / 2.0
        else:
            min_x = 0
            min_y = 0
            max_x = SceneManager.screen_width
            max_y = SceneManager.screen_height

        # 클램핑
        target_x = max(min_x, min(max_x, target_x))
        target_y = max(min_y, min(max_y, target_y))

        # 충돌 타일 확인 및 재시도 (바운딩 박스 전체 확인)
        for attempt in range(10):
            half_width = self.width // 2
            half_height = self.height // 2
            left = target_x - half_width
            bottom = target_y - half_height + 7
            right = target_x + half_width
            top = target_y + half_height + 5

            colliding_tiles = []
            if mm:
                colliding_tiles = mm.check_collision(left, bottom, right, top)

            if not colliding_tiles:
                # 충돌 없음
                self.move_target_x = target_x
                self.move_target_y = target_y
                self.is_moving = True
                self.has_moved = False
                return

            # 충돌 있음, 랜덤 조정
            rand_r = random.uniform(0, self.move_distance)
            rand_theta = random.uniform(0, math.tau)
            target_x = self.x + math.cos(rand_theta) * rand_r
            target_y = self.y + math.sin(rand_theta) * rand_r
            target_x = max(min_x, min(max_x, target_x))
            target_y = max(min_y, min(max_y, target_y))

        # 실패 시 현재 위치 유지
        self.move_target_x = self.x
        self.move_target_y = self.y
        self.is_moving = False
        self.has_moved = True

    def update(self):
        dt = Time.DeltaTime()

        # 체력이 0 이하면 die 상태로 전환
        if self.health <= 0 and self.state != 'die':
            self.state = 'die'
            self.frame_count = 0
            self.is_moving = False
            self.has_moved = True
            self.has_shot = False

        # die 상태일 때는 프레임 애니메이션만 처리하고 리턴
        if self.state == 'die':
            self.frame_timer += dt
            if self.frame_timer > 0.1:
                if self.frame_count < 29:
                    self.frame_count += 1
                self.frame_timer = 0.0
            return

        # 살아있을 때만 방향 전환 및 행동 처리
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
            # enter 사운드는 한 번만 재생
            if not self.enter_sound_played:
                self.enterSound.play()
                self.enter_sound_played = True

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
                #self.pattern = 'ice_bullet' # 디버그용 고정 패턴
                if self.pattern == 'ice_bullet':
                    # # 총알 개수와 스프레드 각도(라디안)
                    count = 5
                    step_deg = 10  # 각 탄 사이의 간격(도)
                    half_span = (step_deg * (count - 1)) / 2.0
                    # 생성
                    self.icebulletSound.play()
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
                    self.icespearSound.play()
                    for i in range(count):
                        IceSpear().shot(start_x, start_y)
                        start_y = start_y + y_offset
                if self.pattern == 'icicle_fall':
                    # 맵의 상단에서 아래로 얼음 조각이 떨어지는 패턴
                    count = 6
                    x_offset = 200  # 총알 간격 (픽셀)
                    # 랜덤으로 스타트 지점 100 or 200
                    self.iciclefallSound.play()
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
        elif group == 'weapon:enemy':
            # 플레이어 총알과 충돌
            try:
                dmg = other.get_damage() if hasattr(other, 'get_damage') else getattr(other, 'attack_power', 0)
                self.take_damage(dmg)
            except Exception:
                pass

    def check_tile_collision(self, new_x, new_y):
        """타일 충돌 체크 및 위치 보정"""
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

        # Y축 충돌 처리 먼저 (수직 방향에서만 충돌 체크)
        for tile in colliding_tiles:
            # 수직 충돌인지 먼저 확인 (X축 중심이 타일과 겹치는지)
            tile_center_x = (tile['left'] + tile['right']) / 2
            player_center_x = (old_left + old_right) / 2

            # X축 오버랩 체크 - 보스 중심이 타일 영역에 있는지
            x_overlap = (old_left < tile['right'] and old_right > tile['left'])

            if x_overlap:
                # 수직 충돌 처리 (Y축)
                if old_top <= tile['bottom'] and top > tile['bottom']:
                    # 위에서 타일에 부딪힘 (천장)
                    new_y = tile['bottom'] - half_height - 5
                elif old_bottom >= tile['top'] and bottom < tile['top']:
                    # 아래에서 타일에 착지
                    new_y = tile['top'] + half_height - 7

        # Y축 처리 후 업데이트된 위치로 X축 충돌 체크
        left = new_x - half_width
        bottom = new_y - half_height + 7
        right = new_x + half_width
        top = new_y + half_height + 5

        colliding_tiles_x = self.map_manager.check_collision(left, bottom, right, top)

        for tile in colliding_tiles_x:
            # Y축 오버랩 체크 - 수평 충돌인지 확인
            y_overlap = (bottom < tile['top'] and top > tile['bottom'])

            if y_overlap:
                # 수평 충돌 처리
                if old_right <= tile['left'] and right > tile['left']:
                    new_x = tile['left'] - half_width - 0.1
                elif old_left >= tile['right'] and left < tile['right']:
                    new_x = tile['right'] + half_width + 0.1

        return new_x, new_y
