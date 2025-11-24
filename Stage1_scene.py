import SceneManager
import pico2d
from Player import player
from MapManager import MapManager
from Enemy_Banshee import Banshee
from Banshee_Attack_note import Note
from Enemy_Bat import Bat
from Bat_Attack_bullet import Bullet
from Enemy_Ghost import Ghost
from Enemy_Skel import Skel
from Camera import Camera
from Portal import Portal
from Gold import Gold
from HpFairy import HpFairy
from PlayerUI import PlayerUI
import random
from ResourceManager import ResourceManager
from ObjectLoader import ObjectLoader


class Stage1Scene:
    def __init__(self):
        print("[Stage1Scene] __init__()")

        self.gameobjs = []
        # MapManager 초기화
        self.map_manager = MapManager(grid_width=100, grid_height=50, tile_size=16*1.5, filename='map.txt')

        # ObjectLoader를 사용하여 오브젝트 로드
        loaded_objects = ObjectLoader.load_from_file('stage1_object_coord.txt', self.map_manager)
        self.gameobjs.extend(loaded_objects)

        self.portal = Portal(2483, 1172)
        self.gameobjs.append(self.portal)

        self.camera = Camera()
        self.camera.set_target(player)

        # PlayerUI 초기화
        self.player_ui = PlayerUI()

        player.set_map_manager(self.map_manager)

    def enter(self):
        print("[Stage1Scene] enter()")
        player.set_map_manager(self.map_manager)
        player.x = 100
        player.y = 200

    def exit(self):
        print("[Stage1Scene] exit()")

    def update(self):
        for obj in self.gameobjs:
            obj.update()
        self.camera.update()
        player.update(self.camera.mX, self.camera.mY, self.camera.zoom)

        # PlayerUI 업데이트 (LifeWave 애니메이션용)
        self.player_ui.update()

        self.handle_collisions()

        for obj in self.gameobjs:
            if hasattr(obj, 'set_map_manager') and obj.map_manager is None:
                obj.set_map_manager(self.map_manager)

    def handle_collisions(self):
        player.near_portal = None
        objects_to_remove = []

        # 플레이어와 다른 객체들의 충돌 체크
        left_a, bottom_a, right_a, top_a = player.get_bb()
        for obj in self.gameobjs:
            left_b, bottom_b, right_b, top_b = obj.get_bb()
            if left_a > right_b: continue
            if right_a < left_b: continue
            if top_a < bottom_b: continue
            if bottom_a > top_b: continue

            if isinstance(obj, Portal):
                player.near_portal = obj
                print("Player near Portal! Press F to enter Stage 2")

            elif isinstance(obj, Ghost):
                # 데미지 쿨타임 체크
                if player.damage_cooldown <= 0:
                    print("Player collided with Ghost!")
                    player.hp -= obj.get_damage()
                    player.damage_cooldown = player.damage_cooldown_time

            elif isinstance(obj, Note):
                print("Player collided with Note!")
                player.hp -= obj.get_damage()
                objects_to_remove.append(obj)

            elif isinstance(obj, Bullet):
                print("Player collided with Bullet!")
                player.hp -= obj.get_damage()
                objects_to_remove.append(obj)

            elif isinstance(obj, Gold):
                print("Player collected Gold!")
                objects_to_remove.append(obj)

            elif isinstance(obj, HpFairy):
                print("Player collected HP Fairy!")
                player.hp = min(player.hp + 30, player.max_hp)
                objects_to_remove.append(obj)

        # 카타나 이펙트와 적들의 충돌 체크
        if player.katana_effect.active:
            katana_left, katana_bottom, katana_right, katana_top = player.katana_effect.get_bb()
            for obj in self.gameobjs:
                if isinstance(obj, Ghost):
                    obj_left, obj_bottom, obj_right, obj_top = obj.get_bb()

                    if not (katana_left > obj_right or katana_right < obj_left or
                            katana_top < obj_bottom or katana_bottom > obj_top):
                        obj.handle_collision('katana_effect:ghost', player.katana_effect)

                        if obj.health <= 0:
                            objects_to_remove.append(obj)
                            drop_item = self.drop_item(obj.x, obj.y)
                            if drop_item:
                                self.gameobjs.append(drop_item)

                elif isinstance(obj, Banshee):
                    obj_left, obj_bottom, obj_right, obj_top = obj.get_bb()

                    if not (katana_left > obj_right or katana_right < obj_left or
                            katana_top < obj_bottom or katana_bottom > obj_top):
                        obj.handle_collision('katana_effect:banshee', player.katana_effect)

                        if obj.health <= 0:
                            objects_to_remove.append(obj)
                            drop_item = self.drop_item(obj.x, obj.y)
                            if drop_item:
                                self.gameobjs.append(drop_item)

                elif isinstance(obj, Bat):
                    obj_left, obj_bottom, obj_right, obj_top = obj.get_bb()

                    if not (katana_left > obj_right or katana_right < obj_left or
                            katana_top < obj_bottom or katana_bottom > obj_top):
                        obj.handle_collision('katana_effect:bat', player.katana_effect)

                        if obj.health <= 0:
                            objects_to_remove.append(obj)
                            drop_item = self.drop_item(obj.x, obj.y)
                            if drop_item:
                                self.gameobjs.append(drop_item)

                elif isinstance(obj, Skel):
                    obj_left, obj_bottom, obj_right, obj_top = obj.get_bb()

                    if not (katana_left > obj_right or katana_right < obj_left or
                            katana_top < obj_bottom or katana_bottom > obj_top):
                        obj.handle_collision('katana_effect:skel', player.katana_effect)

                        if obj.health <= 0:
                            objects_to_remove.append(obj)
                            drop_item = self.drop_item(obj.x, obj.y)
                            if drop_item:
                                self.gameobjs.append(drop_item)

        for obj in objects_to_remove:
            if obj in self.gameobjs:
                self.gameobjs.remove(obj)

    def drop_item(self, x, y):
        """30% 확률로 HP 페어리, 70% 확률로 골드 드랍"""
        rand = random.random()
        if rand < 0.3:
            print(f"HP Fairy dropped at ({x}, {y})")
            return HpFairy(x, y)
        else:
            print(f"Gold dropped at ({x}, {y})")
            return Gold(x, y)

    def handle_events(self, events):
        self.update_mouse_from_events(events)

        result = player.handel_event(events)

        if result == 'enter_portal':
            print("Entering Stage 2...")
            SceneManager.load_scene("Stage2Scene")
            return True

        return False

    def render(self):
        self.map_manager.render(self.camera.mX, self.camera.mY, self.camera.zoom, draw_collision_box=True)

        for gameobj in self.gameobjs:
            gameobj.render(self.camera.mX, self.camera.mY, self.camera.zoom)
            left, bottom, right, top = gameobj.get_bb()
            pico2d.draw_rectangle(
                (left - self.camera.mX) * self.camera.zoom, (bottom - self.camera.mY) * self.camera.zoom,
                (right - self.camera.mX) * self.camera.zoom, (top - self.camera.mY) * self.camera.zoom
            )

        player.render(self.camera.mX, self.camera.mY, self.camera.zoom)
        left, bottom, right, top = player.get_bb()
        pico2d.draw_rectangle(
            (left - self.camera.mX) * self.camera.zoom, (bottom - self.camera.mY) * self.camera.zoom,
            (right - self.camera.mX) * self.camera.zoom, (top - self.camera.mY) * self.camera.zoom
        )

        # PlayerUI 렌더링
        self.player_ui.render()

        if player.near_portal:
            font = ResourceManager.get_font("default")
            font.draw(SceneManager.screen_width // 2 - 100, SceneManager.screen_height - 50,
                     "Press F to Enter", (255, 255, 255))

    def update_mouse_from_events(self, events):
        for event in events:
            if event.type in [pico2d.SDL_MOUSEMOTION, pico2d.SDL_MOUSEBUTTONDOWN, pico2d.SDL_MOUSEBUTTONUP]:
                mx = event.x
                my = SceneManager.screen_height - event.y

                wx = self.camera.mX + mx / self.camera.zoom
                wy = self.camera.mY + my / self.camera.zoom

                try:
                    mm = self.map_manager
                    min_x = mm.TILE_SIZE / 2.0
                    min_y = mm.TILE_SIZE / 2.0
                    max_x = mm.GRID_WIDTH * mm.TILE_SIZE - mm.TILE_SIZE / 2.0
                    max_y = mm.GRID_HEIGHT * mm.TILE_SIZE - mm.TILE_SIZE / 2.0
                except Exception:
                    min_x = 0
                    min_y = 0
                    max_x = SceneManager.screen_width
                    max_y = SceneManager.screen_height

                wx = max(min_x, min(max_x, wx))
                wy = max(min_y, min(max_y, wy))

                SceneManager.mouse_world = (wx, wy)
                self.mouse_world = (wx, wy)
                break
