from pico2d import draw_rectangle

from Time import Time
from ResourceManager import ResourceManager
import pico2d
import SceneManager
import math
from Player_Katana import Katana
from Player_Katana_Effect import KatanaEffect
import Camera


class Player:
    def __init__(self):
        self.hp = 80
        self.max_hp = 80  # 최대 HP 추가
        self.dash_count = 3
        self.state = 'idle'
        self.x = SceneManager.screen_width // 2
        self.y = 128
        self.speed = 200
        self.direction = 0
        self.frame_count = 0
        self.frame_timer = 0.0
        self.jump_velocity = 0
        self.gravity = -2000
        self.left_pressed = False
        self.right_pressed = False
        self.is_dashing = False
        self.dash_speed = 1400
        self.dash_duration = 0.175
        self.dash_timer = 0.0
        self.dash_direction = (0, 0)
        self.dash_recharge_time = 1.0
        self.is_jumping = False
        self.jump_power = 800
        self.jump_count = 2
        self.width = 50
        self.height = 50
        self.weapon = Katana(self)
        self.katana_effect = KatanaEffect(self)
        self.chargingGage = 0.0
        self.is_charging = False
        self.max_chargingGage = 0.75
        self.map_manager = None  # 맵 매니저 참조
        self.is_grounded = False  # 땅에 닿아있는지 여부
        self.near_portal = None  # 근처에 있는 포탈 참조
        self.attack_cooldown = 0  # 공격 쿨타임 초기화
        self.base_attack_cooldown = 0.5  # 기본 공격 쿨타임
        self.attack_speed = 2.0 # 공격 속도 (1.0이 기본 속도)
        self.damage_cooldown = 0.0  # 적에게 데미지 받는 쿨타임
        self.damage_cooldown_time = 0.5  # 데미지 쿨타임 (0.5초)
        self.coin_count = 0  # 플레이어가 가진 코인 수

    def set_map_manager(self, map_manager):
        """맵 매니저 설정"""
        self.map_manager = map_manager

    def get_bb(self):
        half_width = self.width // 2
        half_height = self.height // 2
        return (self.x - half_width, self.y - half_height + 5, self.x + half_width, self.y + half_height + 5)

    def handle_collision(self, group, other):

        pass


    def check_tile_collision(self, new_x, new_y):
        """타일 충돌 체크 및 위치 보정"""
        if not self.map_manager:
            return new_x, new_y, False

        half_width = self.width // 2
        half_height = self.height // 2

        # 현재 위치의 충돌 박스
        old_left = self.x - half_width
        old_right = self.x + half_width
        old_bottom = self.y - half_height + 5
        old_top = self.y + half_height + 5

        # 새 위치에서의 충돌 박스
        left = new_x - half_width
        bottom = new_y - half_height + 5
        right = new_x + half_width
        top = new_y + half_height + 5

        # 충돌하는 타일들 가져오기
        colliding_tiles = self.map_manager.check_collision(left, bottom, right, top)

        grounded = False

        # Y축 충돌 처리 먼저 (수직 방향에서만 충돌 체크)
        for tile in colliding_tiles:
            # 수직 충돌인지 먼저 확인 (X축 중심이 타일과 겹치는지)
            tile_center_x = (tile['left'] + tile['right']) / 2
            player_center_x = (old_left + old_right) / 2

            # X축 오버랩 체크 - 플레이어 중심이 타일 영역에 있는지
            x_overlap = (old_left < tile['right'] and old_right > tile['left'])

            if x_overlap:
                # 수직 충돌 처리 (Y축)
                if old_top <= tile['bottom'] and top > tile['bottom']:
                    # 위에서 타일에 부딪힘 (천장)
                    new_y = tile['bottom'] - half_height - 5
                    self.jump_velocity = 0
                elif old_bottom >= tile['top'] and bottom < tile['top']:
                    # 아래에서 타일에 착지
                    new_y = tile['top'] + half_height - 5
                    self.jump_velocity = 0
                    grounded = True

        # Y축 처리 후 업데이트된 위치로 X축 충돌 체크
        left = new_x - half_width
        bottom = new_y - half_height + 5
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

        # 착지 여부 추가 체크: 발 아래에 타일이 있는지 확인
        if not grounded:
            # 발 바로 아래를 체크
            foot_left = new_x - half_width + 2
            foot_right = new_x + half_width - 2
            foot_bottom = new_y - half_height + 4
            foot_top = new_y - half_height + 6

            foot_tiles = self.map_manager.check_collision(foot_left, foot_bottom, foot_right, foot_top)
            if foot_tiles:
                grounded = True

        return new_x, new_y, grounded

    def update(self, camera_x, camera_y, zoom):
        dt = Time.DeltaTime()

        # 공격 쿨타임 감소
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt
        if self.damage_cooldown > 0:
            self.damage_cooldown -= dt
        new_x = self.x
        if not self.is_dashing:
            if self.left_pressed and not self.right_pressed:
                new_x = self.x - self.speed * dt
            elif self.right_pressed and not self.left_pressed:
                new_x = self.x + self.speed * dt

        # 중력 적용
        new_y = self.y
        if not self.is_dashing:
            self.jump_velocity += self.gravity * dt
            new_y = self.y + self.jump_velocity * dt
        else:
            # 대쉬 중
            new_x = self.x + self.dash_direction[0] * self.dash_speed * dt
            new_y = self.y + self.dash_direction[1] * self.dash_speed * dt

        # 충돌 체크 (X, Y 동시에)
        final_x, final_y, grounded = self.check_tile_collision(new_x, new_y)
        self.x = final_x
        self.y = final_y
        self.is_grounded = grounded

        # 착지 확인
        if self.is_grounded:
            self.is_jumping = False
            self.jump_count = 2  # 착지 시 점프 횟수 초기화
            if not self.is_dashing:
                if self.left_pressed or self.right_pressed:
                    self.state = 'run'
                else:
                    self.state = 'idle'
        else:
            # 공중에 있음
            if not self.is_dashing:
                self.is_jumping = True
                self.state = 'jump'

        # 대쉬 처리
        if self.is_dashing:
            self.dash_timer -= dt
            if self.dash_timer <= 0:
                self.is_dashing = False
                # 대쉬 종료 후 공중이면 점프 속도 유지
                if not self.is_grounded:
                    self.jump_velocity = max(self.jump_velocity, -400)
                    self.state = 'jump'
                else:
                    self.state = 'idle'

        # 차징 처리
        if self.is_charging:
            self.chargingGage += dt
            if self.chargingGage > self.max_chargingGage:
                self.chargingGage = self.max_chargingGage

        # 프레임 애니메이션
        self.frame_timer += dt
        if self.frame_timer > 0.1:
            self.frame_count += 1
            self.frame_timer = 0.0

        # 대쉬 쿨타임
        if not self.is_dashing and self.dash_count < 3:
            self.dash_timer += dt
            if self.dash_timer >= self.dash_recharge_time:
                self.dash_count += 1
                self.dash_timer = 0.0

        if self.weapon:
            self.weapon.update()
        if self.katana_effect:
            self.katana_effect.update()

    def handel_event(self, events):
        # 카메라와 SceneManager.mouse_world를 한 번만 읽음
        camera = Camera.Camera()
        camera_x, camera_y = camera.get_position()
        zoom = camera.get_zoom()
        mouse_world = getattr(SceneManager, 'mouse_world', None)

        for event in events:
            if event.type == pico2d.SDL_MOUSEMOTION:
                if mouse_world:
                    world_x, world_y = mouse_world
                else:
                    mouse_x = event.x
                    mouse_y = SceneManager.screen_height - event.y
                    world_x = mouse_x / zoom + camera_x
                    world_y = mouse_y / zoom + camera_y
                dx = world_x - self.x
                dy = world_y - self.y
                distance = math.hypot(dx, dy)
                self.direction = -1 if dx < 0 else 1 if dx > 0 else self.direction
                angle = math.atan2(dy, dx)
                self.weapon.angle = angle
            if event.type == pico2d.SDL_KEYDOWN:
                if event.key == pico2d.SDLK_a:
                    self.left_pressed = True
                elif event.key == pico2d.SDLK_d:
                    self.right_pressed = True
                elif event.key == pico2d.SDLK_SPACE and self.jump_count > 0:
                    self.jump_velocity = self.jump_power
                    self.jump_count -= 1
                    self.is_jumping = True
                    self.state = 'jump'
                elif event.key == pico2d.SDLK_p:
                    self.hp -= 10
                    print("플레이어 체력:", self.hp)
                elif event.key == pico2d.SDLK_f:
                    if self.near_portal:
                        return 'enter_portal'  # 포탈 진입 신호 반환
            if event.type == pico2d.SDL_MOUSEBUTTONDOWN:
                if mouse_world:
                    world_x, world_y = mouse_world
                else:
                    mouse_x = event.x
                    mouse_y = SceneManager.screen_height - event.y
                    world_x = mouse_x / zoom + camera_x
                    world_y = mouse_y / zoom + camera_y
                dx = world_x - self.x
                dy = world_y - self.y
                distance = math.hypot(dx, dy)
                if event.button == pico2d.SDL_BUTTON_RIGHT and self.dash_count > 0:
                    if distance != 0:
                        self.dash_direction = (dx / distance, dy / distance)
                        self.is_dashing = True
                        self.dash_timer = self.dash_duration
                        self.dash_count -= 1
                elif event.button == pico2d.SDL_BUTTON_LEFT:
                    self.is_charging = True
            if event.type == pico2d.SDL_MOUSEBUTTONUP:
                if event.button == pico2d.SDL_BUTTON_LEFT and self.is_charging:
                    # 공격 쿨타임 체크
                    if self.attack_cooldown <= 0:
                        print("공격 실행")
                        self.katana_effect.start()
                        self.is_charging = False
                        self.chargingGage = 0.0
                        # 공격속도에 따른 쿨타임 설정 (공격속도가 높을수록 쿨타임이 짧아짐)
                        self.attack_cooldown = self.base_attack_cooldown / self.attack_speed
                    else:
                        # 쿨타임 중에는 차징만 취소
                        self.is_charging = False
                        self.chargingGage = 0.0
            if event.type == pico2d.SDL_KEYUP:
                if event.key == pico2d.SDLK_a:
                    self.left_pressed = False
                elif event.key == pico2d.SDLK_d:
                    self.right_pressed = False

    def render(self, camera_x=0, camera_y=0, zoom=1.0):
        image, frame_count, width, height = ResourceManager.get_image(f"player_{self.state}")
        # 이미지 유효성 검사 및 frame_count 안전 처리
        if not image:
            return
        frame_count = max(1, frame_count)
        draw_x = int((self.x - camera_x) * zoom)
        draw_y = int((self.y - camera_y) * zoom) + int(height // 2 * zoom)
        draw_w = int(self.width * zoom)
        draw_h = int(self.height * zoom)
        if frame_count > 1:
            frame = self.frame_count % frame_count
            if self.direction == -1:
                image.clip_composite_draw(frame * width // frame_count, 0, width // frame_count, height, 0, 'h', draw_x,
                                          draw_y, draw_w, draw_h)
            else:
                image.clip_draw(frame * width // frame_count, 0, width // frame_count, height, draw_x, draw_y, draw_w,
                                draw_h)
        else:
            if self.direction == -1:
                image.composite_draw(0, 'h', draw_x, draw_y, draw_w, draw_h)
            else:
                image.draw(draw_x, draw_y, draw_w, draw_h)

        charging_gage_image, _, gage_width, gage_height = ResourceManager.get_image("charging_gage_bar")
        charging_gage_frame_image, _, frame_width, frame_height = ResourceManager.get_image("charging_gage_frame")
        charging_gage_offset_y = int(40 * zoom)
        if self.is_charging:
            gage_scale = self.chargingGage / self.max_chargingGage
            charging_gage_image.draw(draw_x, draw_y + charging_gage_offset_y, int(gage_width * gage_scale * 2 * zoom),
                                     int(gage_height * zoom))
            charging_gage_frame_image.draw(draw_x, draw_y + charging_gage_offset_y, int(frame_width * 2 * zoom),
                                           int(frame_height * zoom))

        if self.weapon:
            self.weapon.render(camera_x, camera_y, zoom)
        if self.katana_effect:
            self.katana_effect.render(camera_x, camera_y, zoom)
            left, bottom, right, top = self.katana_effect.get_bb()
            pico2d.draw_rectangle(
                (left - camera_x) * zoom, (bottom - camera_y) * zoom,
                (right - camera_x) * zoom, (top - camera_y) * zoom
            )








player = Player()