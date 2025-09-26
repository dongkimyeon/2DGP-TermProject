from pico2d import clear_canvas, update_canvas

import SceneManager
import pico2d
from stage1_scene import Stage1Scene

class TitleScene:
    def __init__(self):
        print("[TitleScene] __init__() 호출")


    def enter(self):
        print("[TitleScene] enter() - 이미지 로드(생략)")


    def exit(self):
        print("[TitleScene] exit() - 리소스 해제(생략)")
     


    def update(self):
        #print("[TitleScene] update() 호출")
        events = pico2d.get_events()
        for event in events:
            if event.type == pico2d.SDL_KEYDOWN and event.key == pico2d.SDLK_SPACE:
                print("[TitleScene] 스페이스바 입력 감지, Stage1Scene으로 전환")
                SceneManager.load_scene("Stage1Scene")

    def render(self):

        pass
