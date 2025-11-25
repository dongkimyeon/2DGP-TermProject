from Time import Time
from ResourceManager import ResourceManager
import pico2d
import SceneManager
import math

class IceBullet:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 18
        self.height = 36
        self.speed = 0
        self.rotation = 0  # 렌더 시 사용할 고정 회전값(발사 직후 방향)
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
        half_width = 18 // 2
        half_height = 18 // 2
        return (self.x - half_width, self.y - half_height + 5  , self.x + half_width , self.y + half_height + 5 )

    def get_damage(self):
        return self.attack_power

    def shot(self, x, y, direction, speed=300):
        self.x = x
        self.y = y
        self.rotation = direction  # 발사 시 방향으로 초기 회전 고정
        self.direction = direction
        # 프레임 초기화하여 새로 발사될 때 애니메이션이 처음부터 재생되게 함
        self.frame_count = 0
        self.frame_timer = 0.0
        self.speed = speed
        SceneManager.active_scene.gameobjs.append(self)
        return self

    def update(self):
        dt = Time.DeltaTime()
        # 이동
        self.x += math.cos(self.direction) * self.speed * dt
        self.y += math.sin(self.direction) * self.speed * dt

        # 맵 타일과의 충돌 체크
        if self.map_manager:
            half_width = 18 // 2
            half_height = 18 // 2
            left = self.x - half_width
            bottom = self.y - half_height + 5
            right = self.x + half_width
            top = self.y + half_height + 5

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

    def handle_collision(self, group, other):
        """충돌 처리 - 플레이어와 충돌 시 사라짐"""
        # 플레이어와 충돌하면 사라짐
        if self in SceneManager.active_scene.gameobjs:
            SceneManager.active_scene.gameobjs.remove(self)

    def render(self, camera_x=0, camera_y=0, zoom=1.0):
        image, frame_count, width, height = ResourceManager.get_image(f"niflheim_ice_bullet")
        # 이미지 또는 프레임 정보가 유효하지 않으면 렌더링 건너뜀
        if not image or frame_count == 0:
            return
        # frame_count가 0인 경우 안전 처리
        frame_count = max(1, frame_count)
        frame = self.frame_count % frame_count
        draw_x = int((self.x - camera_x) * zoom)
        draw_y = int((self.y - camera_y) * zoom) + int(height // 2 * zoom)
        draw_w = int(self.width * zoom)
        draw_h = int(self.height * zoom)
        # 탄환이 발사될 때의 방향(rotation)을 사용해 초기 렌더링 시에도 올바르게 회전되도록 함
        # 만약 스프라이트의 기본 방향(예: 위)을 기준으로 보정이 필요하면 아래 OFFSET 값을 조정하세요.
        OFFSET = -math.pi/2  # 예: 스프라이트가 위를 향하면 -math.pi/2 등으로 설정
        angle = self.rotation + OFFSET
        image.clip_composite_draw(frame * width // frame_count, 0, width // frame_count, height,
                                  angle, '', draw_x, draw_y, draw_w, draw_h)
