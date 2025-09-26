from pico2d import clear_canvas, update_canvas

import SceneManager
import pico2d
from Time import Time
from ImageManager import ImageManager

temp = 0.0

class TitleScene:
    def __init__(self):
        print("[TitleScene] __init__() 호출")
        self.backCloud = ImageManager.get_image("player_idle")[0]


    def enter(self):
        print("[TitleScene] enter() - 이미지 로드")


    def exit(self):
        print("[TitleScene] exit() - 리소스 해제")
        del self.backCloud


    def update(self):
        # print("[TitleScene] update() 호출")
        events = pico2d.get_events()
        for event in events:
            if event.type == pico2d.SDL_KEYDOWN and event.key == pico2d.SDLK_SPACE:
                print("[TitleScene] 스페이스바 입력 감지, Stage1Scene으로 전환")
                SceneManager.load_scene("Stage1Scene")
        global temp
        temp += Time.DeltaTime()
        if temp > 1.0:
            temp = 0.0
            print("1초 경과")

    def render(self):
        self.backCloud.draw(100,100)
