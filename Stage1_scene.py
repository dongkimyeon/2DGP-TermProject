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
import game_world


class Stage1Scene:
    def __init__(self):
        print("[Stage1Scene] __init__()")

        self.gameobjs = []

        self.map_manager = MapManager(grid_width=100, grid_height=50, tile_size=16*1.5, filename='map.txt')

        self.dead_sound = pico2d.load_wav('resources/sound/MonsterDie.wav')
        self.dead_sound.set_volume(32)

        self.exit_sound = pico2d.load_wav('resources/sound/DungeonOut.wav')
        self.exit_sound.set_volume(32)
    def enter(self):
        print("[Stage1Scene] enter()")
        loaded_objects = ObjectLoader.load_from_file('stage1_object_coord.txt', self.map_manager)
        self.gameobjs.extend(loaded_objects)

        self.portal = Portal(2483, 1172)
        self.gameobjs.append(self.portal)

        self.camera = Camera()
        self.camera.set_target(player)

        # PlayerUI 초기화
        self.player_ui = PlayerUI()

        SceneManager.play_time = 0.0
        SceneManager.play_timerOn = True
        player.set_map_manager(self.map_manager)
        player.x = 100
        player.y = 200

        #플레이어 모든 변수 초기화
        player.reset_for_stage()

        # collision pairs 초기화 후 등록
        game_world.clear_collision_pairs()

        # 플레이어와 적
        game_world.add_collision_pair('player:enemy', player, None)
        # 플레이어와 적 발사체
        game_world.add_collision_pair('player:enemy_projectile', player, None)
        # 카타나 이펙트와 적
        game_world.add_collision_pair('katana_effect:enemy', player.katana_effect, None)
        # 플레이어와 아이템
        game_world.add_collision_pair('player:gold', player, None)
        game_world.add_collision_pair('player:hpfairy', player, None)
        # 플레이어와 포탈
        game_world.add_collision_pair('player:portal', player, self.portal)

        # 적들을 collision pair에 등록
        from Enemy_Ghost import Ghost
        from Enemy_Banshee import Banshee
        from Enemy_Bat import Bat
        from Enemy_Skel import Skel
        from Gold import Gold
        from HpFairy import HpFairy

        for obj in self.gameobjs:
            if isinstance(obj, (Ghost, Banshee, Bat, Skel)):
                game_world.add_collision_pair('player:enemy', None, obj)
                game_world.add_collision_pair('katana_effect:enemy', None, obj)
                game_world.add_collision_pair('weapon:enemy', None, obj)
            if isinstance(obj, Gold):
                game_world.add_collision_pair('player:gold', None, obj)
            if isinstance(obj, HpFairy):
                game_world.add_collision_pair('player:hpfairy', None, obj)

    def exit(self):
        print("[Stage1Scene] exit()")
        self.exit_sound.play()
        self.gameobjs.clear()
        game_world.clear_collision_pairs()

    def update(self):
        for obj in self.gameobjs:
            obj.update()
        self.camera.update()
        player.update(self.camera.mX, self.camera.mY, self.camera.zoom)

        # PlayerUI 업데이트 (LifeWave 애니메이션용)
        self.player_ui.update()

        # 중앙화된 충돌 처리
        game_world.handle_collisions()

        # 적 체력이 0 이하인 경우 제거 및 드랍 처리
        objects_to_remove = []
        for obj in list(self.gameobjs):
            if hasattr(obj, 'health') and obj.health <= 0:
                from Enemy_Ghost import Ghost
                from Enemy_Banshee import Banshee
                from Enemy_Bat import Bat
                from Enemy_Skel import Skel
                if isinstance(obj, (Ghost, Banshee, Bat, Skel)):
                    objects_to_remove.append(obj)
                    drop_item = self.drop_item(obj.x, obj.y)
                    if drop_item:
                        self.gameobjs.append(drop_item)
                        from Gold import Gold
                        from HpFairy import HpFairy
                        if isinstance(drop_item, Gold):
                            game_world.add_collision_pair('player:gold', None, drop_item)
                        elif isinstance(drop_item, HpFairy):
                            game_world.add_collision_pair('player:hpfairy', None, drop_item)

        for obj in objects_to_remove:
            if obj in self.gameobjs:
                self.gameobjs.remove(obj)
                game_world.remove_collision_object(obj)

        for obj in self.gameobjs:
            if hasattr(obj, 'set_map_manager') and obj.map_manager is None:
                obj.set_map_manager(self.map_manager)

    def drop_item(self, x, y):
        """30% 확률로 HP 페어리, 70% 확률로 골드 드랍"""
        self.dead_sound.play()
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
