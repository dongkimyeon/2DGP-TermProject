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
        self.y = SceneManager.screen_height // 2
        self.speed = 200
        self.direction = 0
        self.frame_count = 0
        self.frame_timer = 0.0
        self.jump_velocity = 0
        self.gravity = -2000  # 중력 값 약간 완화 (-2200 -> -2000)
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
        self.ground_y = 40
        self.jump_count = 2
        self.width = 50
        self.height = 50
        self.weapon = Katana(self)
        self.katana_effect = KatanaEffect(self)
        self.chargingGage = 0.0
        self.is_charging = False
        self.max_chargingGage = 0.75

    def get_bb(self):
        half_width = self.width // 2
        half_height = self.height // 2
        return (self.x - half_width, self.y - half_height + 5, self.x + half_width, self.y + half_height + 5)
    def update(self, camera_x, camera_y, zoom):
        dt = Time.DeltaTime()
        #stateprint
        #print("Player State:", self.state)
        # 중력 적용 (대쉬 중에는 중력 무시)
        if not self.is_dashing:
            self.jump_velocity += self.gravity * dt
            self.y += self.jump_velocity * dt
        else:
            # 대쉬 중에는 중력 영향을 받지 않고 방향대로만 이동
            self.x += self.dash_direction[0] * self.dash_speed * dt
            self.y += self.dash_direction[1] * self.dash_speed * dt

        # 착지 확인
        if self.y <= self.ground_y:
            self.y = self.ground_y
            self.jump_velocity = 0
            self.is_jumping = False
            self.jump_count = 2  # 착지 시 점프 횟수 초기화
            if self.direction == 0 and not self.is_dashing:
                self.state = 'idle'
            elif self.direction != 0 and not self.is_dashing:
                self.state = 'run'
        else:
            self.is_jumping = True
            self.state = 'jump'

        # 대쉬 처리
        if self.is_dashing:
            self.dash_timer -= dt
            if self.dash_timer <= 0:
                self.is_dashing = False
                # 대쉬 종료 후 공중이면 점프 속도 유지
                if self.y > self.ground_y:
                    self.jump_velocity = max(self.jump_velocity, -400)  # 더 부드러운 하강을 위해 -500 -> -400
                    self.state = 'jump'
                else:
                    self.state = 'idle'
        # 차징 처리
        if self.is_charging:
            self.chargingGage += dt
            if self.chargingGage > self.max_chargingGage:
                self.chargingGage = self.max_chargingGage
            print(f"차징 중: {self.chargingGage:.2f} / {self.max_chargingGage}")
        # 수평 이동
        if not self.is_dashing:
            if self.left_pressed and not self.right_pressed:
                self.state = 'run' if self.y == self.ground_y else 'jump'
                self.x -=  self.speed * dt
            elif self.right_pressed and not self.left_pressed:
                self.state = 'run' if self.y == self.ground_y else 'jump'
                self.x +=  self.speed * dt
            else:
                self.state = 'idle' if self.y == self.ground_y else 'jump'

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
                print("대쉬 충전: 현재 대쉬 수", self.dash_count)

        if self.weapon:
            self.weapon.update()
        if self.katana_effect:
            self.katana_effect.update()
    def handel_event(self, events):
        for event in events:
            camera = Camera.Camera()
            camera_x, camera_y = camera.get_position()
            zoom = camera.get_zoom()
            if event.type == pico2d.SDL_MOUSEMOTION:
                mouse_x = event.x
                mouse_y = SceneManager.screen_height - event.y
                # 화면 좌표 → 월드 좌표 변환
                world_x = mouse_x / zoom + camera_x
                world_y = mouse_y / zoom + camera_y
                dx = world_x - self.x
                dy = world_y - self.y
                distance = math.sqrt(dx ** 2 + dy ** 2)
                self.direction = -1 if dx < 0 else 1 if dx > 0 else self.direction
                # 각도 계산 및 Katana에 전달
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
                mouse_x = event.x
                mouse_y = SceneManager.screen_height - event.y
                world_x = mouse_x / zoom + camera_x
                world_y = mouse_y / zoom + camera_y
                dx = world_x - self.x
                dy = world_y - self.y
                distance = math.sqrt(dx ** 2 + dy ** 2)
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