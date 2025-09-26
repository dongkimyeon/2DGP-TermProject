import SceneManager
import pico2d
from Time import Time

class Stage1Scene:
    def __init__(self):
        print("[Stage1Scene] __init__()")

    def enter(self):
        print("[Stage1Scene] enter()")

    def exit(self):
        print("[Stage1Scene] exit()")

    def update(self):

        events = pico2d.get_events()
        for event in events:
            if event.type == pico2d.SDL_KEYDOWN and event.key == pico2d.SDLK_SPACE:
                print("[Stage1Scene] 스페이스바 입력 감지, TitleScene으로 전환")
                SceneManager.load_scene("TitleScene")


    def render(self):

        pass
