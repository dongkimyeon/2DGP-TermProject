import SceneManager
import pico2d
from Player import player
from MapManager import MapManager
from Boss_nifleheim import Boss
from IceBullet import IceBullet
from Camera import Camera
from Portal import Portal
import random
from ResourceManager import ResourceManager


class BossStageScene:
    def __init__(self):
        print("[BossStageScene] __init__()")

        self.gameobjs = []
        # MapManager 초기화 - 보스 스테이지용 맵 사용
        self.map_manager = MapManager(grid_width=100, grid_height=50, tile_size=16*1.5, filename='map2.txt')

        # 보스 생성
        boss = Boss(1200, 400)
        boss.set_map_manager(self.map_manager)
        self.gameobjs.append(boss)

        # 포탈 생성 (보스를 처치하면 활성화될 포탈)
        self.portal = Portal(2483, 1172)
        self.gameobjs.append(self.portal)

        self.camera = Camera()
        self.camera.set_target(player)

        # 플레이어에게 맵 매니저 설정
        player.set_map_manager(self.map_manager)

    def enter(self):
        print("[BossStageScene] enter()")
        pass

    def exit(self):
        print("[BossStageScene] exit()")

    def update(self):
        for obj in self.gameobjs:
            obj.update()
        self.camera.update()
        player.update(self.camera.mX, self.camera.mY, self.camera.zoom)

        self.handle_collisions()

        # 새로 생성된 발사체들에도 맵 매니저 설정
        for obj in self.gameobjs:
            if hasattr(obj, 'set_map_manager') and obj.map_manager is None:
                obj.set_map_manager(self.map_manager)

    def handle_collisions(self):
        # 먼저 플레이어의 포탈 근처 상태 초기화
        player.near_portal = None

        left_a, bottom_a, right_a, top_a = player.get_bb()
        for obj in self.gameobjs:
            left_b, bottom_b, right_b, top_b = obj.get_bb()
            if left_a > right_b: continue
            if right_a < left_b: continue
            if top_a < bottom_b: continue
            if bottom_a > top_b: continue

            # 각 객체마다 충돌처리 코드 추가
            if isinstance(obj, Portal):
                # 포탈과 충돌 중
                player.near_portal = obj
                print("Player near Portal!")

            elif isinstance(obj, Boss):
                print("Player collided with Boss!")
                player.hp -= 5

            elif isinstance(obj, IceBullet):
                print("Player collided with IceBullet!")
                player.hp -= 10

    def handle_events(self, events):
        """이벤트 처리"""
        self.update_mouse_from_events(events)

        # 플레이어 이벤트 처리
        result = player.handel_event(events)

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

