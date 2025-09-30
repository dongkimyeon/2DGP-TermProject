import SceneManager
import pico2d
from Time import Time
from ImageManager import ImageManager
from Player import player
from MapManager import MapManager
from Enemy_Banshee import Banshee
from Banshee_Attack_note import Note
from Enemy_Bat import Bat
from Bat_Attack_bullet import Bullet
import random


class Stage1Scene:
    def __init__(self):
        print("[Stage1Scene] __init__()")
        self.backgroundLayer0, _, self.backgroundLayer0_width, self.backgroundLayer0_height = ImageManager.get_image("forest_back_Layer_0")
        self.backgroundLayer1, _, self.backgroundLayer1_width, self.backgroundLayer1_height = ImageManager.get_image("forest_back_Layer_1")
        self.backgroundLayer2, _, self.backgroundLayer2_width, self.backgroundLayer2_height = ImageManager.get_image("forest_back_Layer_2")
        self.gameobjs = []
        # MapManager 초기화
        self.map_manager = MapManager(grid_width=20, grid_height=15, tile_size=32, filename='map.txt')
        # Banshee 10마리 랜덤 좌표로 생성
        for _ in range(2):
            newBanshee = Banshee()
            rand_x = random.randint(100, 600)
            rand_y = random.randint(100, 400)
            newBanshee.set_position(rand_x, rand_y)
            self.gameobjs.append(newBanshee)
        for _ in range(2):
            newBat = Bat()
            rand_x = random.randint(100, 600)
            rand_y = random.randint(100, 400)
            newBat.set_position(rand_x, rand_y)
            self.gameobjs.append(newBat)


    def enter(self):
        print("[Stage1Scene] enter()")
        # 맵 로드는 MapManager의 __init__에서 이미 처리됨
        pass

    def exit(self):
        print("[Stage1Scene] exit()")

    def update(self):
        for obj in self.gameobjs:
            #print("obj update")
            obj.update()
        player.update()



    def render(self):
        # 배경 레이어 렌더링
        self.backgroundLayer0.draw(SceneManager.screen_width // 2, SceneManager.screen_height // 2, SceneManager.screen_width, SceneManager.screen_height)
        self.backgroundLayer1.draw(SceneManager.screen_width // 2, 150, SceneManager.screen_width, SceneManager.screen_height // 1.5)
        self.backgroundLayer2.draw(SceneManager.screen_width // 2, 150, SceneManager.screen_width, SceneManager.screen_height // 1.5)
        # 맵 타일 렌더링
        self.map_manager.render()

        # 게임 오브젝트 렌더링
        for gameobj in self.gameobjs:
            #print("gameobj render")
            gameobj.render()
            pico2d.draw_rectangle(*gameobj.get_bb())
        # 플레이어 렌더링
        player.render()
        pico2d.draw_rectangle(*player.get_bb())

