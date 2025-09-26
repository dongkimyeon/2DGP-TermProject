from Time import Time
from ImageManager import ImageManager
import pico2d
import SceneManager
import math

class Player:
    def __init__(self):
        self.hp = 80
        self.dash_count = 3
        self.state = 'idle'
        self.x = SceneManager.screen_width // 2
        self.y = SceneManager.screen_height // 2 + 10
        self.speed = 200
        self.direction = 0
        self.frame_count = 0
        self.frame_timer = 0.0
        self.jump_velocity = 0
        self.gravity = -2000
        self.weapon = None
        self.left_pressed = False
        self.right_pressed = False
        self.is_dashing = False
        self.dash_speed = 1500
        self.dash_duration = 0.15
        self.dash_timer = 0.0
        self.dash_direction = (0, 0)
        self.dash_recharge_time = 1.0
        self.is_jumping = False
        self.jump_power = 600
        self.ground_y = 45
        self.jump_count = 2

    def update(self):
        dt = Time.DeltaTime()

        self.jump_velocity += self.gravity * dt
        self.y += self.jump_velocity * dt

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
                self.state = 'jump' if self.y > self.ground_y else 'idle'
            else:
                # 마우스 방향으로 대쉬 (수평 및 수직)
                self.x += self.dash_direction[0] * self.dash_speed * dt
                self.y += self.dash_direction[1] * self.dash_speed * dt

        # 입력 처리
        events = pico2d.get_events()
        for event in events:
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
            if event.type == pico2d.SDL_MOUSEBUTTONDOWN:
                if event.button == pico2d.SDL_BUTTON_RIGHT and self.dash_count > 0:
                    mouse_x, mouse_y = event.x, SceneManager.screen_height - event.y
                    dx = mouse_x - self.x
                    dy = mouse_y - self.y
                    distance = math.sqrt(dx**2 + dy**2)
                    if distance != 0:
                        self.dash_direction = (dx / distance, dy / distance)
                        self.is_dashing = True
                        self.dash_timer = self.dash_duration
                        self.dash_count -= 1
                        print("대쉬: 방향", self.dash_direction)
                elif event.button == pico2d.SDL_BUTTON_LEFT:
                    print("공격")
            elif event.type == pico2d.SDL_KEYUP:
                if event.key == pico2d.SDLK_a:
                    self.left_pressed = False
                elif event.key == pico2d.SDLK_d:
                    self.right_pressed = False

        # 수평 이동
        if not self.is_dashing:
            if self.left_pressed and not self.right_pressed:
                self.direction = -1
                self.state = 'run' if self.y == self.ground_y else 'jump'
                self.x += self.direction * self.speed * dt
            elif self.right_pressed and not self.left_pressed:
                self.direction = 1
                self.state = 'run' if self.y == self.ground_y else 'jump'
                self.x += self.direction * self.speed * dt
            else:
                # 방향을 0으로 초기화하지 않고, 마지막 방향을 유지
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

    def render(self):
        image, frame_count, width, height = ImageManager.get_image(f"player_{self.state}")
        if frame_count > 1:
            frame = self.frame_count % frame_count
            if self.direction == -1:
                image.clip_composite_draw(frame * width // frame_count, 0, width // frame_count, height, 0, 'h', int(self.x), int(self.y) + height // 2, 100, 100)
            else:
                image.clip_draw(frame * width // frame_count, 0, width // frame_count, height, int(self.x), int(self.y) + height // 2, 100, 100)
        else:
            if self.direction == -1:
                image.composite_draw(0, 'h', int(self.x), int(self.y) + height // 2, 100, 100)
            else:
                image.draw(int(self.x), int(self.y) + height // 2, 100, 100)

player = Player()