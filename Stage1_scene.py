import SceneManager
import pico2d
from Time import Time
from ImageManager import ImageManager
from Player import player  # player 인스턴스를 import


class Stage1Scene:
    def __init__(self):
        print("[Stage1Scene] __init__()")
        self.backgroundLayer0, _, self.backgroundLayer0_width, self.backgroundLayer0_height = ImageManager.get_image("forest_back_Layer_0")
        self.backgroundLayer1, _, self.backgroundLayer1_width, self.backgroundLayer1_height = ImageManager.get_image("forest_back_Layer_1")
        self.backgroundLayer2, _, self.backgroundLayer2_width, self.backgroundLayer2_height = ImageManager.get_image("forest_back_Layer_2")

    def enter(self):
        print("[Stage1Scene] enter()")

    def exit(self):
        print("[Stage1Scene] exit()")

    def update(self):
        player.update()  # 기존 Player.update()를 player.update()로 수정



    def render(self):
        self.backgroundLayer0.draw(SceneManager.screen_width // 2, SceneManager.screen_height // 2, SceneManager.screen_width, SceneManager.screen_height)
        self.backgroundLayer1.draw(SceneManager.screen_width // 2, 150, (SceneManager.screen_width) * 2.0, (SceneManager.screen_height //1.5) * 2.0)
        self.backgroundLayer2.draw(SceneManager.screen_width // 2, 150, (SceneManager.screen_width) * 2.0 , (SceneManager.screen_height //1.5) * 2.0)
        player.render()  # 기존 Player.render()를 player.render()로 수정
