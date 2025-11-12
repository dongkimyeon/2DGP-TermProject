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
        self.dash_count = 3
        self.state = 'idle'
        self.x = SceneManager.screen_width // 2
        self.y = 120
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

    def set_map_manager(self, map_manager):
        """맵 매니저 설정"""
        self.map_manager = map_manager

    def get_bb(self):
        half_width = self.width // 2
        half_height = self.height // 2
        return (self.x - half_width, self.y - half_height + 5, self.x + half_width, self.y + half_height + 5)

    def handle_collision(self, group, other):
        """충돌 처리"""
        if group == 'player:tile':
            # 타일과의 충돌 처리
            pass

    def check_tile_collision(self, new_x, new_y):
        """타일 충돌 체크 및 위치 보정"""
        if not self.map_manager:
            return new_x, new_y, False

        half_width = self.width // 2
        half_height = self.height // 2

        # 새 위치에서의 충돌 박스
        left = new_x - half_width
        bottom = new_y - half_height + 5
        right = new_x + half_width
        top = new_y + half_height + 5

        # 충돌하는 타일들 가져오기
        colliding_tiles = self.map_manager.check_collision(left, bottom, right, top)

        grounded = False

        if colliding_tiles:
            # X축 충돌 체크
            old_left = self.x - half_width
            old_right = self.x + half_width

            # Y축 충돌 체크
            old_bottom = self.y - half_height + 5
            old_top = self.y + half_height + 5

            for tile in colliding_tiles:
                # 수평 충돌 처리
                if old_right <= tile['left'] and right > tile['left']:
                    new_x = tile['left'] - half_width
                elif old_left >= tile['right'] and left < tile['right']:
                    new_x = tile['right'] + half_width

                # 수직 충돌 처리
                if old_top <= tile['bottom'] and top > tile['bottom']:
                    # 위에서 타일에 부딪힘 (천장)
                    new_y = tile['bottom'] - half_height - 5
                    self.jump_velocity = 0
                elif old_bottom >= tile['top'] and bottom < tile['top']:
                    # 아래에서 타일에 착지
                    new_y = tile['top'] + half_height - 5
                    self.jump_velocity = 0
                    grounded = True

        return new_x, new_y, grounded

    def update(self, camera_x, camera_y, zoom):
        dt = Time.DeltaTime()

        # 중력 적용 (대쉬 중에는 중력 무시)
        if not self.is_dashing:
            self.jump_velocity += self.gravity * dt
            new_y = self.y + self.jump_velocity * dt
            new_x = self.x
        else:
            # 대쉬 중에는 중력 영향을 받지 않고 방향대로만 이동
            new_x = self.x + self.dash_direction[0] * self.dash_speed * dt
            new_y = self.y + self.dash_direction[1] * self.dash_speed * dt

        # 수평 이동 처리
        if not self.is_dashing:
            if self.left_pressed and not self.right_pressed:
                new_x = self.x - self.speed * dt
            elif self.right_pressed and not self.left_pressed:
                new_x = self.x + self.speed * dt

        # X축 충돌 체크 먼저
        temp_x, temp_y, _ = self.check_tile_collision(new_x, self.y)
        self.x = temp_x

        # Y축 충돌 체크 (중력 적용된 새로운 Y 위치)
        final_x, final_y, grounded = self.check_tile_collision(self.x, new_y)
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
                    print("공격 실행")
                    self.katana_effect.start()
                    self.is_charging = False
                    self.chargingGage = 0.0
            if event.type == pico2d.SDL_KEYUP:
                if event.key == pico2d.SDLK_a:
                    self.left_pressed = False
                elif event.key == pico2d.SDLK_d:
                    self.right_pressed = False

    def render(self, camera_x=0, camera_y=0, zoom=1.0):
        image, frame_count, width, height = ResourceManager.get_image(f"player_{self.state}")
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

        # font = ResourceManager.get_font("default")
        # font.draw(10, SceneManager.screen_height - 30, f'HP: {self.hp}', (255, 0, 0))




player = Player()