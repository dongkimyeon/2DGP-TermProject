from Time import Time
from ResourceManager import ResourceManager
import pico2d
import SceneManager
import math
import game_world


class Note:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 35
        self.height = 35
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
        half_width = self.width // 2
        half_height = self.height // 2
        return (self.x - half_width, self.y - half_height + 2 , self.x + half_width - 5, self.y + half_height )

    def get_damage(self):
        return self.attack_power

    def shot(self, x, y, direction, speed=300):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        SceneManager.active_scene.gameobjs.append(self)
        # game_world에 플레이어-적 발사체 충돌 페어에 이 노트를 등록
        game_world.add_collision_pair('player:enemy_projectile', None, self)
        return self

    def update(self):
        dt = Time.DeltaTime()
        # 이동
        self.x += math.cos(self.direction) * self.speed * dt
        self.y += math.sin(self.direction) * self.speed * dt

        # 맵 타일과의 충돌 체크
        if self.map_manager:
            half_width = self.width // 2
            half_height = self.height // 2
            left = self.x - half_width
            bottom = self.y - half_height + 2
            right = self.x + half_width - 5
            top = self.y + half_height

            colliding_tiles = self.map_manager.check_collision(left, bottom, right, top)
            if colliding_tiles:
                # 벽에 닿으면 사라짐
                if self in SceneManager.active_scene.gameobjs:
                    SceneManager.active_scene.gameobjs.remove(self)
                # collision pair에서 제거
                game_world.remove_collision_object(self)
                return

        # 프레임 애니메이션
        self.frame_timer += dt
        if self.frame_timer > 0.1:
            self.frame_count += 1
            self.frame_timer = 0.0

    def render(self, camera_x=0, camera_y=0, zoom=1.0):
        image, frame_count, width, height = ResourceManager.get_image(f"note")
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
            image.clip_draw(frame * width // frame_count, 0, width // frame_count, height, draw_x,
                            draw_y, draw_w, draw_h)

    def handle_collision(self, group, other):
        """충돌 처리 - 플레이어와 충돌 시 사라짐"""
        if self in SceneManager.active_scene.gameobjs:
            SceneManager.active_scene.gameobjs.remove(self)
        # collision pair에서 제거
        game_world.remove_collision_object(self)
