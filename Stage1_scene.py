import SceneManager
import pico2d
from Time import Time
from Player import player  # player 인스턴스를 import


class Stage1Scene:
    def __init__(self):
        print("[Stage1Scene] __init__()")


    def enter(self):
        print("[Stage1Scene] enter()")

    def exit(self):
        print("[Stage1Scene] exit()")

    def update(self):
        player.update()  # 기존 Player.update()를 player.update()로 수정
        events = pico2d.get_events()
        for event in events:
            if event.type == pico2d.SDL_KEYDOWN and event.key == pico2d.SDLK_SPACE:
                print("[Stage1Scene] 스페이스바 입력 감지, TitleScene으로 전환")
                SceneManager.load_scene("TitleScene")


    def render(self):
        player.render()  # 기존 Player.render()를 player.render()로 수정
