from Time import Time
from ImageManager import ImageManager
import pico2d
import SceneManager
import math


class Player:
    def __init__(self):
        # 상태별 이미지와 프레임 수 저장

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

    def update(self):
        dt = Time.DeltaTime()
        events = pico2d.get_events()
        for event in events:
            if event.type == pico2d.SDL_KEYDOWN:
                if event.key == pico2d.SDLK_LEFT:
                    self.direction = -1
                    self.state = 'run'
                elif event.key == pico2d.SDLK_RIGHT:
                    self.direction = 1
                    self.state = 'run'
            elif event.type == pico2d.SDL_KEYUP:
                if event.key == pico2d.SDLK_LEFT:
                    self.direction = 0
                    self.state = 'idle'
                elif event.key == pico2d.SDLK_RIGHT:
                    self.direction = 0
                    self.state = 'idle'
        if(self.state == 'run'):
            self.x += self.direction * self.speed * dt
        # 프레임 카운트
        self.frame_timer += dt
        if self.frame_timer > 0.16:
            self.frame_count += 1
            self.frame_timer = 0.0

    def render(self):
        image, frame_count, width, height = ImageManager.get_image(f"player_{self.state}")
        if frame_count > 1:
            frame = self.frame_count % frame_count
            image.clip_draw(frame * width // frame_count, 0, width // frame_count, height, int(self.x), int(self.y) + height // 2)
        else:
            image.draw(int(self.x), int(self.y) + height // 2)


player = Player()  # 모든 씬에서 공유할 수 있도록 전역 객체로 생성
