from Time import Time
from ResourceManager import ResourceManager
import pico2d
import SceneManager
import math


class Player_Gun_Bullet:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 14 * 3
        self.height = 5 * 3
        self.speed = 0
        self.direction = 0
        self.attack_power = 12

        self.frame_count = 0
        self.frame_timer = 0.0
        self.map_manager = None  # 맵 매니저 참조

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def set_map_manager(self, map_manager):
        """맵 매니저 설정"""
        self.map_manager = map_manager

    def get_bb(self):
        # 회전된 총알의 네 모서리를 계산해서 축 정렬 경계 상자(AABB)를 반환합니다.
        # 기존에 사용하던 좌표 오프셋(하단 +2, 우측 -5)을 보존하여 계산합니다.
        cx = self.x
        cy = self.y
        # 오프셋 포함한 로컬 좌표
        left_off = - (self.width / 2)
        right_off = (self.width / 2) - 5
        bottom_off = - (self.height / 2) + 2
        top_off = (self.height / 2)

        corners = [
            (left_off, bottom_off),
            (right_off, bottom_off),
            (right_off, top_off),
            (left_off, top_off)
        ]

        cos_a = math.cos(self.direction)
        sin_a = math.sin(self.direction)

        rx = []
        ry = []
        for px, py in corners:
            # 회전 행렬 적용 (중심이 cx,cy)
            x_world = cx + (px * cos_a - py * sin_a)
            y_world = cy + (px * sin_a + py * cos_a)
            rx.append(x_world)
            ry.append(y_world)

        left = min(rx)
        right = max(rx)
        bottom = min(ry)
        top = max(ry)
        return (left, bottom, right, top)

    def get_damage(self):
        return self.attack_power

    def shot(self, x, y, direction, speed=300):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 1000
        SceneManager.active_scene.gameobjs.append(self)
        return self

    def update(self):
        dt = Time.DeltaTime()
        # 이동
        self.x += math.cos(self.direction) * self.speed * dt
        self.y += math.sin(self.direction) * self.speed * dt

        # 맵 타일과의 충돌 체크
        if self.map_manager:
            # get_bb()를 사용해 회전된 AABB로 충돌 체크
            left, bottom, right, top = self.get_bb()

            colliding_tiles = self.map_manager.check_collision(left, bottom, right, top)
            if colliding_tiles:
                # 벽에 닿으면 사라짐
                if self in SceneManager.active_scene.gameobjs:
                    SceneManager.active_scene.gameobjs.remove(self)
                return

        # 프레임 애니메이션
        self.frame_timer += dt
        if self.frame_timer > 0.1:
            self.frame_count += 1
            self.frame_timer = 0.0

    def render(self, camera_x=0, camera_y=0, zoom=1.0):
        image, frame_count, width, height = ResourceManager.get_image(f"gun_bullet")
        if not image:
            return
        # frame_count가 0인 경우 안전 처리
        frame_count = max(1, frame_count)
        frame = self.frame_count % frame_count
        draw_x = int((self.x - camera_x) * zoom)
        draw_y = int((self.y - camera_y) * zoom) + int(height // 2 * zoom)
        draw_w = int(self.width * zoom)
        draw_h = int(self.height * zoom)
        if image:
            # 발사 방향(self.direction, 라디안)에 따라 총알 이미지를 회전하여 그리기
            # clip_composite_draw(left, bottom, w, h, angle, flip, x, y, w, h)
            # angle은 라디안 단위이며 이미지 기본 방향이 오른쪽(0 라디안)이라고 가정함
            try:
                image.clip_composite_draw(frame * (width // frame_count), 0, width // frame_count, height,
                                          self.direction, '', draw_x, draw_y, draw_w, draw_h)
            except Exception:
                # pico2d 구현에 따라 함수명이 다를 수 있으므로 기본 clip_draw로 폴백
                image.clip_draw(frame * (width // frame_count), 0, width // frame_count, height, draw_x, draw_y, draw_w, draw_h)

    def handle_collision(self, group, other):
        """충돌 처리 - 플레이어와 충돌 시 사라짐"""
        if self in SceneManager.active_scene.gameobjs:
            SceneManager.active_scene.gameobjs.remove(self)
