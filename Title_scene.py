from pico2d import clear_canvas, update_canvas

import SceneManager
import pico2d
from Time import Time
from ImageManager import ImageManager




class TitleScene:
    def __init__(self):
        print("[TitleScene] __init__()")
        self.backCloud, _, self.backCloud_width, self.backCloud_height = ImageManager.get_image("backCloud")
        self.frontCloud, _, self.frontCloud_width, self.frontCloud_height = ImageManager.get_image("frontCloud")
        self.backGround, _, self.backGround_width, self.backGround_height = ImageManager.get_image("titleBackground")
        self.mainLogo, _, self.mainLogo_width, self.mainLogo_height = ImageManager.get_image("mainlogo")
        self.screen_width = SceneManager.screen_width
        self.screen_height = SceneManager.screen_height
        self.backCloud_x = 0.0
        self.frontCloud_x = 0.0
        self.backCloud_speed = 80
        self.frontCloud_speed = 120


    def enter(self):
        print("[TitleScene] enter()")


    def exit(self):
        print("[TitleScene] exit()")
        self.backCloud = None
        self.frontCloud = None


    def update(self):
        dt = Time.DeltaTime()
        self.backCloud_x += self.backCloud_speed * dt
        self.frontCloud_x += self.frontCloud_speed * dt
        # 무한 스크롤: 이미지가 한 화면을 다 벗어나면 위치 리셋
        if self.backCloud_x >= self.screen_width:
            self.backCloud_x -= self.screen_width
        if self.frontCloud_x >= self.screen_width:
            self.frontCloud_x -= self.screen_width
        events = pico2d.get_events()
        for event in events:
            if event.type == pico2d.SDL_KEYDOWN and event.key == pico2d.SDLK_SPACE:
                print("[TitleScene] 스페이스바 입력 감지, Stage1Scene으로 전환")
                SceneManager.load_scene("Stage1Scene")


    def render(self):
        # background
        self.backGround.draw(self.screen_width // 2, self.screen_height // 2, self.screen_width, self.screen_height)

        # backCloud
        self.backCloud.draw(self.screen_width // 2 - self.backCloud_x, self.screen_height // 2, self.screen_width, self.screen_height)
        self.backCloud.draw(self.screen_width // 2 - self.backCloud_x + self.screen_width, self.screen_height // 2, self.screen_width, self.screen_height)
        # frontCloud
        self.frontCloud.draw(self.screen_width // 2 - self.frontCloud_x, self.screen_height // 2, self.screen_width, self.screen_height)
        self.frontCloud.draw(self.screen_width // 2 - self.frontCloud_x + self.screen_width, self.screen_height // 2, self.screen_width, self.screen_height)
        # mainLogo (중앙 상단)
        self.mainLogo.draw(self.screen_width // 2, self.screen_height - self.mainLogo_height // 2 - 300 , self.mainLogo_width * 5.0, self.mainLogo_height * 5.0)
