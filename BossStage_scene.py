# BossStageScene.py (기존 코드에 BossUI 관련 부분만 업데이트된 버전, 전체 파일 제공)
from pico2d import load_image

import SceneManager
import pico2d
from Player import player
from MapManager import MapManager
from Boss_nifleheim import Boss
from IceBullet import IceBullet
from IceSpear import IceSpear
from Icicle import Icicle
from Camera import Camera
from Portal import Portal
from PlayerUI import PlayerUI
from BossUI import BossUI
import random
from ResourceManager import ResourceManager
import os
import game_world


class BossStageScene:
    def __init__(self):
        print("[BossStageScene] __init__()")
        self.background = load_image('resources/images/Map/StageMapTile/IceBackGround.png')
        self.gameobjs = []
        # MapManager 초기화 - 보스 스테이지용 맵 사용
        self.map_manager = MapManager(grid_width=100, grid_height=50, tile_size=16*1.5, filename='map2.txt')


    def enter(self):
        print("[BossStageScene] enter()")
        # 보스 생성
        boss = Boss(593, 500)
        boss.set_map_manager(self.map_manager)
        self.gameobjs.append(boss)
        self.is_created_portal = False

        self.camera = Camera()
        self.camera.set_target(player)

        # PlayerUI 초기화
        self.player_ui = PlayerUI()

        # BossUI 초기화 (보스 참조)
        self.boss_ui = BossUI(boss)

        # 플레이어에게 맵 매니저 설정
        player.set_map_manager(self.map_manager)
        player.x = 100
        player.y = 128

        # collision pairs 초기화 후 등록
        game_world.clear_collision_pairs()

        # 플레이어와 보스
        game_world.add_collision_pair('player:enemy', player, boss)
        # 카타나 이펙트와 보스
        game_world.add_collision_pair('katana_effect:enemy', player.katana_effect, boss)
        # 플레이어 무기와 보스
        game_world.add_collision_pair('weapon:enemy', None, boss)
        # 플레이어와 보스 발사체
        game_world.add_collision_pair('player:enemy_projectile', player, None)

    def exit(self):
        print("[BossStageScene] exit()")
        # UI 정리
        try:
            self.player_ui = None
        except Exception:
            pass
        try:
            self.boss_ui = None
        except Exception:
            pass
        self.gameobjs.clear()
        game_world.clear_collision_pairs()

    def update(self):
        for obj in self.gameobjs:
            obj.update()
        self.camera.update()
        player.update(self.camera.mX, self.camera.mY, self.camera.zoom)

        # PlayerUI 업데이트 (LifeWave 애니메이션용)
        self.player_ui.update()

        # BossUI 업데이트
        try:
            if hasattr(self, 'boss_ui') and self.boss_ui is not None:
                self.boss_ui.update()
        except Exception:
            pass

        # 중앙화된 충돌 처리
        game_world.handle_collisions()

        # 새로 생성된 발사체들에도 맵 매니저 설정
        for obj in self.gameobjs:
            if hasattr(obj, 'set_map_manager') and obj.map_manager is None:
                obj.set_map_manager(self.map_manager)

        #보스가 죽으면 포탈 생성
        if not self.is_created_portal:
            #보스 체력 확인
            for obj in self.gameobjs:
                if isinstance(obj, Boss) and obj.health <= 0:
                    SceneManager.play_timerOn = False
                    portal = Portal(593, 335)
                    self.gameobjs.append(portal)
                    # 포탈을 collision pair에 등록
                    game_world.add_collision_pair('player:portal', player, portal)
                    self.is_created_portal = True



    def handle_events(self, events):
        """이벤트 처리"""
        self.update_mouse_from_events(events)

        # 플레이어 이벤트 처리
        result = player.handel_event(events)

        for event in events:
            if event.type == pico2d.SDL_KEYDOWN:
                if event.key == pico2d.SDLK_n:
                    print('asd')
                    for obj in self.gameobjs:
                        if isinstance(obj, Boss):
                            obj.health = 0

        # 포탈 진입 신호 처리: 보스 스테이지에서는 랭킹 씬으로 이동
        if result == 'enter_portal':
            # 플레이 타임 저장 (초 단위 소수점 3자리)
            try:
                path = os.path.join(os.path.dirname(__file__), 'record.txt')
                with open(path, 'a', encoding='utf-8') as f:
                    f.write(f"{SceneManager.play_time:.3f}\n")
            except Exception as e:
                print("[BossStageScene] record save failed:", e)

            SceneManager.load_scene("RankingScene")
            return True

        return False

    def render(self):
        # 맵 타일 렌더링 (충돌 박스 표시 활성화)
        self.background.draw(SceneManager.screen_width // 2, SceneManager.screen_height // 2, SceneManager.screen_width,
                             SceneManager.screen_height)

        self.map_manager.render(self.camera.mX, self.camera.mY, self.camera.zoom, draw_collision_box=True)

        # 게임 오브젝트 렌더링
        for gameobj in self.gameobjs:
            gameobj.render(self.camera.mX, self.camera.mY, self.camera.zoom)
            left, bottom, right, top = gameobj.get_bb()

        # 플레이어 렌더링
        player.render(self.camera.mX, self.camera.mY, self.camera.zoom)
        left, bottom, right, top = player.get_bb()
        pico2d.draw_rectangle(
            (left - self.camera.mX) * self.camera.zoom, (bottom - self.camera.mY) * self.camera.zoom,
            (right - self.camera.mX) * self.camera.zoom, (top - self.camera.mY) * self.camera.zoom
        )

        # PlayerUI 렌더링
        self.player_ui.render()

        self.boss_ui.render()



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