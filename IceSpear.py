from Time import Time
from ResourceManager import ResourceManager
import pico2d
import SceneManager
import math

class IceSpear:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 25
        self.height = 113
        self.speed = 1200
        self.attack_power = 12
        self.scale = 1.5
        self.frame_count = 0
        self.frame_timer = 0.0
        self.map_manager = None  # 맵 매니저 참조
        self.dir = 0
    def set_position(self, x, y):
        self.x = x
        self.y = y

    def set_map_manager(self, map_manager):
        """맵 매니저 설정"""
        self.map_manager = map_manager

    def get_bb(self):
        # 90도 회전 시 width와 height를 바꿔서 적용
        half_width = self.height // 2
        half_height = self.width // 2
        return (
            self.x - half_width * self.scale,
            self.y - half_height * self.scale + 55,
            self.x + half_width * self.scale,
            self.y + half_height * self.scale+ 55
        )

    def get_damage(self):
        return self.attack_power

    def shot(self, x, y):
        self.x = x
        self.y = y
        if x < 1000:
            self.dir = 1
        else:
            self.dir = 0
        self.frame_count = 0
        self.frame_timer = 0.0
        SceneManager.active_scene.gameobjs.append(self)
        return self

    def update(self):
        dt = Time.DeltaTime()
        # 프레임 애니메이션 (9 미만일 때만)
        if self.frame_count < 12:
            self.frame_timer += dt
            if self.frame_timer > 0.1:
                self.frame_count += 1
                self.frame_timer = 0.0

        # 10번째 프레임부터 떨어지기
        if self.frame_count >= 12:
            self.frame_count = 12 # 고정 (이제 애니메이션 로직이 안 타서 유지됨)
            if self.dir == 0:
                self.x -= self.speed * dt
            else:
                self.x += self.speed * dt

    def handle_collision(self, group, other):
        """충돌 처리 - 플레이어와 충돌 시 사라짐"""
        # 플레이어와 충돌하면 사라짐
        if self in SceneManager.active_scene.gameobjs:
            SceneManager.active_scene.gameobjs.remove(self)

    def render(self, camera_x=0, camera_y=0, zoom=1.0):
        image, frame_count, width, height = ResourceManager.get_image(f"niflheim_spear")
        # 이미지 또는 프레임 정보가 유효하지 않으면 렌더링 건너뜀
        if not image or frame_count == 0:
            return
        # frame_count가 0인 경우 안전 처리
        frame_count = max(1, frame_count)
        frame = self.frame_count % frame_count
        draw_x = int((self.x - camera_x) * zoom)

        # 애니메이션이 있는 경우

        radian = 0
        if self.dir == 0:
            radian = 1.5708
        else:
            radian = -1.5708
        frame = self.frame_count % frame_count
        draw_x = int((self.x - camera_x) * zoom)
        draw_y = int((self.y - camera_y) * zoom) + int(height // 2 * zoom)
        image.clip_composite_draw(frame * width // frame_count, 0, width // frame_count, height, radian, ' ',
                                  draw_x, draw_y, int(self.width * self.scale * zoom), int(self.height * self.scale * zoom))
