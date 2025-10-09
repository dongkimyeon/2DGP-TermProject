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
from Enemy_Ghost import Ghost
from Enemy_Skel import Skel
import random


class Stage1Scene:
    def __init__(self):
        print("[Stage1Scene] __init__()")

        self.gameobjs = []
        # MapManager 초기화
        self.map_manager = MapManager(grid_width=20, grid_height=15, tile_size=32, filename='map.txt')

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

        for _ in range(2):
            newGhost = Ghost()
            rand_x = random.randint(100, 600)
            rand_y = random.randint(100, 400)
            newGhost.set_position(rand_x, rand_y)
            self.gameobjs.append(newGhost)

        for _ in range(2):
            newwSkel = Skel()
            rand_x = random.randint(100, 600)
            rand_y = random.randint(100, 400)
            newwSkel.set_position(rand_x, rand_y)
            self.gameobjs.append(newwSkel)


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

        self.handle_collisions()

    def handle_collisions(self):
        left_a, bottom_a, right_a, top_a = player.get_bb()
        for obj in self.gameobjs:
            left_b, bottom_b, right_b, top_b = obj.get_bb()
            if left_a > right_b: continue
            if right_a < left_b: continue
            if top_a < bottom_b: continue
            if bottom_a > top_b: continue

            #각 객체마다 충돌처리 코드 추가
            if isinstance(obj, Banshee):
                print("Player collided with Banshee!")
                player.hp -= obj.get_damage()

            elif isinstance(obj, Bat):
                print("Player collided with Bat!")
                player.hp -= obj.get_damage()

            elif isinstance(obj, Ghost):
                print("Player collided with Ghost!")
                player.hp -= obj.get_damage()

            elif isinstance(obj, Note):
                print("Player collided with Note!")
                player.hp -= obj.get_damage()

            elif isinstance(obj, Bullet):
                print("Player collided with Bullet!")
                player.hp -= obj.get_damage()

    def render(self):
               # 맵 타일 렌더링
        #self.map_manager.render()

        # 게임 오브젝트 렌더링
        for gameobj in self.gameobjs:
            #print("gameobj render")
            gameobj.render()
            pico2d.draw_rectangle(*gameobj.get_bb())
        # 플레이어 렌더링
        player.render()
        pico2d.draw_rectangle(*player.get_bb())

