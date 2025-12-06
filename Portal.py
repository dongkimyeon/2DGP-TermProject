from ResourceManager import ResourceManager

class Portal:
    def __init__(self, x,y):
        self.x = x
        self.y = y
        self.width = 27
        self.height = 31
        self.scale = 2.0
        self.is_player_nearby = False  # 플레이어가 근처에 있는지 여부
        self.is_active = False  # 포탈 활성화 상태 (모든 적 처치 후)


    def activate(self):
        """포탈 활성화"""
        self.is_active = True

    def deactivate(self):
        """포탈 비활성화"""
        self.is_active = False

    def get_bb(self):
        half_width = self.width // 2
        half_height = self.height // 2
        return (self.x - half_width * self.scale, self.y - half_height * self.scale + 10, self.x + half_width * self.scale, self.y + half_height * self.scale + 10)

    def update(self):
        pass

    def handle_collision(self, group, other):
        """충돌 처리"""
        if group == 'player:portal':
            # 포탈이 활성화되어 있을 때만 플레이어 근처 표시
            if self.is_active:
                self.is_player_nearby = True

    def render(self, camera_x=0, camera_y=0, zoom=1.0):
        image, frame_count, width, height = ResourceManager.get_image(f"gate")
        draw_x = int((self.x - camera_x) * zoom)
        draw_y = int((self.y - camera_y) * zoom) + int(height // 2 * zoom)

        # 포탈이 비활성화 상태면 반투명하게 렌더링
        if not self.is_active:
            image.opacify(0.5)  # 30% 불투명도

        image.draw(draw_x, draw_y, self.width * self.scale * zoom, self.height * self.scale * zoom)

        if not self.is_active:
            image.opacify(1.0)  # 원래대로 복구
