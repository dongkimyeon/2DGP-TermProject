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


class Stage2Scene:
    def __init__(self):
        print("[Stage2Scene] __init__()")

        self.gameobjs = []
        # MapManager 초기화
        self.map_manager = MapManager(grid_width=100, grid_height=50, tile_size=16*1.5, filename='map1.txt')

        for _ in range(1):
            newBanshee = Banshee()
            rand_x = 400
            rand_y = random.randint(100, 400)
            newBanshee.set_position(rand_x, rand_y)
            newBanshee.set_map_manager(self.map_manager)  # 맵 매니저 설정
            self.gameobjs.append(newBanshee)
        for _ in range(1):
            newBat = Bat()
            rand_x = 300
            rand_y = random.randint(100, 400)
            newBat.set_position(rand_x, rand_y)
            newBat.set_map_manager(self.map_manager)  # 맵 매니저 설정
            self.gameobjs.append(newBat)
        for _ in range(1):
            newGhost = Ghost()
            rand_x = 200
            rand_y = random.randint(100, 400)
            newGhost.set_position(rand_x, rand_y)
            newGhost.set_map_manager(self.map_manager)  # 맵 매니저 설정
            self.gameobjs.append(newGhost)
        for _ in range(1):
            newSkel = Skel()
            rand_x = 100
            rand_y = random.randint(100, 400)
            newSkel.set_position(rand_x, rand_y)
            newSkel.set_map_manager(self.map_manager)  # 맵 매니저 설정
            self.gameobjs.append(newSkel)

        self.portal = Portal(2483,1172)
        self.gameobjs.append(self.portal)

        self.camera = Camera()
        self.camera.set_target(player)

        # PlayerUI 초기화
        self.player_ui = PlayerUI()

        # 플레이어에게 맵 매니저 설정
        player.set_map_manager(self.map_manager)

    def enter(self):
        print("[Stage2Scene] enter()")
        # 씬 진입 시 플레이어에게 이 씬의 맵 매니저를 다시 설정
        player.set_map_manager(self.map_manager)
        # 플레이어 위치 초기화
        player.x = 100
        player.y = 200

    def exit(self):
        print("[Stage2Scene] exit()")

    def update(self):
        for obj in self.gameobjs:
            #print("obj update")
            obj.update()
        self.camera.update()
        player.update(self.camera.mX, self.camera.mY, self.camera.zoom)

        # PlayerUI 업데이트 (LifeWave 애니메이션용)
        self.player_ui.update()

        self.handle_collisions()

        # 새로 생성된 발사체들에도 맵 매니저 설정
        for obj in self.gameobjs:
            if hasattr(obj, 'set_map_manager') and obj.map_manager is None:
                obj.set_map_manager(self.map_manager)

    def handle_collisions(self):
        # 먼저 플레이어의 포탈 근처 상태 초기화
        player.near_portal = None

        # 충돌 시 제거할 객체 리스트
        objects_to_remove = []

        left_a, bottom_a, right_a, top_a = player.get_bb()
        for obj in self.gameobjs:
            left_b, bottom_b, right_b, top_b = obj.get_bb()
            if left_a > right_b: continue
            if right_a < left_b: continue
            if top_a < bottom_b: continue
            if bottom_a > top_b: continue

            #각 객체마다 충돌처리 코드 추가
            if isinstance(obj, Portal):
                # 포탈과 충돌 중
                player.near_portal = obj
                print("Player near Portal! Press F to enter Boss Stage")

            elif isinstance(obj, Ghost):
                # 데미지 쿨타임 체크
                if player.damage_cooldown <= 0:
                    print("Player collided with Ghost!")
                    player.hp -= obj.get_damage()
                    player.damage_cooldown = player.damage_cooldown_time

            elif isinstance(obj, Note):
                print("Player collided with Note!")
                player.hp -= obj.get_damage()
                # Note를 제거 리스트에 추가
                objects_to_remove.append(obj)

            elif isinstance(obj, Bullet):
                print("Player collided with Bullet!")
                player.hp -= obj.get_damage()
                # Bullet도 제거 리스트에 추가
                objects_to_remove.append(obj)

            elif isinstance(obj, Gold):
                print("Player collected Gold!")
                # 골드 획득 처리
                objects_to_remove.append(obj)

            elif isinstance(obj, HpFairy):
                print("Player collected HP Fairy!")
                player.hp = min(player.hp + 30, player.max_hp)  # HP 30 회복
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
                            # 30% 확률로 HP 페어리, 70% 확률로 골드 드랍
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
                            # 30% 확률로 HP 페어리, 70% 확률로 골드 드랍
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
                            # 30% 확률로 HP 페어리, 70% 확률로 골드 드랍
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
                            # 30% 확률로 HP 페어리, 70% 확률로 골드 드랍
                            drop_item = self.drop_item(obj.x, obj.y)
                            if drop_item:
                                self.gameobjs.append(drop_item)

        # 충돌한 객체들을 gameobjs에서 제거
        for obj in objects_to_remove:
            if obj in self.gameobjs:
                self.gameobjs.remove(obj)

    def drop_item(self, x, y):
        """30% 확률로 HP 페어리, 70% 확률로 골드 드랍"""
        rand = random.random()
        if rand < 0.3:  # 30% 확률
            print(f"HP Fairy dropped at ({x}, {y})")
            return HpFairy(x, y)
        else:  # 70% 확률
            print(f"Gold dropped at ({x}, {y})")
            return Gold(x, y)

    def handle_events(self, events):
        """이벤트 처리 및 씬 전환 감지"""
        self.update_mouse_from_events(events)

        # 플레이어 이벤트 처리
        result = player.handel_event(events)

        # 포탈 진입 신호 확인 - 보스 스테이지로 전환
        if result == 'enter_portal':
            print("Entering Boss Stage...")
            SceneManager.load_scene("BossStageScene")
            return True

        return False

    def render(self):
        # 맵 타일 렌더링 (충돌 박스 표시 활성화)
        self.map_manager.render(self.camera.mX, self.camera.mY, self.camera.zoom, draw_collision_box=True)

        # 게임 오브젝트 렌더링
        for gameobj in self.gameobjs:
            gameobj.render(self.camera.mX, self.camera.mY, self.camera.zoom)
            left, bottom, right, top = gameobj.get_bb()
            pico2d.draw_rectangle(
                (left - self.camera.mX) * self.camera.zoom, (bottom - self.camera.mY) * self.camera.zoom,
                (right - self.camera.mX) * self.camera.zoom, (top - self.camera.mY) * self.camera.zoom
            )
        # 플레이어 렌더링
        player.render(self.camera.mX, self.camera.mY, self.camera.zoom)
        left, bottom, right, top = player.get_bb()
        pico2d.draw_rectangle(
            (left - self.camera.mX) * self.camera.zoom, (bottom - self.camera.mY) * self.camera.zoom,
            (right - self.camera.mX) * self.camera.zoom, (top - self.camera.mY) * self.camera.zoom
        )

        # PlayerUI 렌더링 (가장 마지막에)
        self.player_ui.render()

        # 포탈 근처에 있을 때 UI 표시
        if player.near_portal:
            font = ResourceManager.get_font("default")
            font.draw(SceneManager.screen_width // 2 - 100, SceneManager.screen_height - 50,
                     "Press F to Enter", (255, 255, 255))

    def update_mouse_from_events(self, events):
        """이벤트에서 마우스 좌표를 읽어 월드 좌표로 변환"""
        for event in events:
            if event.type in [pico2d.SDL_MOUSEMOTION, pico2d.SDL_MOUSEBUTTONDOWN, pico2d.SDL_MOUSEBUTTONUP]:
                mx = event.x
                # pico2d 이벤트 y는 위쪽이 0이므로 아래쪽 원점으로 변환
                my = SceneManager.screen_height - event.y

                # 화면 좌표를 월드 좌표로 변환
                wx = self.camera.mX + mx / self.camera.zoom
                wy = self.camera.mY + my / self.camera.zoom

                # 맵 경계 클램프
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

                # 전역으로 저장
                SceneManager.mouse_world = (wx, wy)
                self.mouse_world = (wx, wy)
                break
