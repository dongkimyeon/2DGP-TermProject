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
        self.y = SceneManager.screen_height // 2
        self.speed = 200
        self.direction = 0
        self.frame_count = 0
        self.frame_timer = 0.0
        self.jump_velocity = 0
        self.gravity = -800
        self.weapon = None
        self.left_pressed = False
        self.right_pressed = False
        self.is_dashing = False  # 대쉬 상태 추가
        self.dash_speed = 1500  # 대쉬 속도
        self.dash_duration = 0.2  # 대쉬 지속 시간 (초)
        self.dash_timer = 0.0  # 대쉬 타이머
        self.dash_direction = (0, 0)  # 대쉬 방향 (x, y)
        self.dash_recharge_time = 1.0  # 대쉬 재충전 시간 (초)

    def update(self):
        dt = Time.DeltaTime()

        # 대쉬 중일 때
        if self.is_dashing:
            self.dash_timer -= dt
            if self.dash_timer <= 0:
                self.is_dashing = False
                self.state = 'idle'
            else:
                # 대쉬 방향으로 이동
                self.x += self.dash_direction[0] * self.dash_speed * dt
                self.y += self.dash_direction[1] * self.dash_speed * dt


        events = pico2d.get_events()
        for event in events:
            if event.type == pico2d.SDL_KEYDOWN:
                if event.key == pico2d.SDLK_a:
                    self.left_pressed = True
                elif event.key == pico2d.SDLK_d:
                    self.right_pressed = True
                elif event.key == pico2d.SDLK_SPACE:
                    print("점프")
                    pass
            if event.type == pico2d.SDL_MOUSEBUTTONDOWN:
                if event.button == pico2d.SDL_BUTTON_RIGHT and self.dash_count > 0:
                    # 마우스 위치 가져오기
                    mouse_x, mouse_y = event.x, SceneManager.screen_height - event.y
                    # 마우스 방향 계산
                    dx = mouse_x - self.x
                    dy = mouse_y - self.y
                    distance = math.sqrt(dx**2 + dy**2)
                    if distance != 0:  # 0으로 나누기 방지
                        self.dash_direction = (dx / distance, dy / distance)
                        self.is_dashing = True
                        self.dash_timer = self.dash_duration
                        self.dash_count -= 1
                        self.state = 'dash'  # 대쉬 애니메이션용 상태
                        print("대쉬: 방향", self.dash_direction)
                elif event.button == pico2d.SDL_BUTTON_LEFT:
                    print("공격")
            elif event.type == pico2d.SDL_KEYUP:
                if event.key == pico2d.SDLK_a:
                    self.left_pressed = False
                elif event.key == pico2d.SDLK_d:
                    self.right_pressed = False

        # 방향 결정
        if self.left_pressed and not self.right_pressed:
            self.direction = -1
            self.state = 'run'
        elif self.right_pressed and not self.left_pressed:
            self.direction = 1
            self.state = 'run'
        elif not self.left_pressed and not self.right_pressed:
            self.direction = 0
            self.state = 'idle'

        if self.direction != 0:
            self.x += self.direction * self.speed * dt

        # 프레임 카운트
        self.frame_timer += dt
        if self.frame_timer > 0.1:
            self.frame_count += 1
            self.frame_timer = 0.0

        # 대쉬 쿨타임 : 대쉬 카운트 1증가
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
            image.clip_draw(frame * width // frame_count, 0, width // frame_count, height, int(self.x), int(self.y) + height // 2, 100, 100)
        else:
            image.draw(int(self.x), int(self.y) + height // 2)

player = Player()  # 모든 씬에서 공유할 수 있도록 전역 객체로 생성