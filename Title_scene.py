from pico2d import clear_canvas, update_canvas

import SceneManager
import pico2d
from Time import Time
from ImageManager import ImageManager


class TitleScene:
    def __init__(self):
        print("[TitleScene] __init__()")
        self.backCloud = ImageManager.get_image("backCloud")[0]
        self.frontCloud = ImageManager.get_image("frontCloud")[0]


    def enter(self):
        print("[TitleScene] enter()")


    def exit(self):
        print("[TitleScene] exit()")
        del self.backCloud


    def update(self):
        # print("[TitleScene] update() 호출")
        events = pico2d.get_events()
        for event in events:
            if event.type == pico2d.SDL_KEYDOWN and event.key == pico2d.SDLK_SPACE:
                print("[TitleScene] 스페이스바 입력 감지, Stage1Scene으로 전환")
                SceneManager.load_scene("Stage1Scene")


    def render(self):
        self.backCloud.draw(100,100)
        self.frontCloud.draw(200,200)
