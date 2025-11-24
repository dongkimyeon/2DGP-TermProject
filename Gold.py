from ResourceManager import ResourceManager
from Time import Time

class Gold:
    def __init__(self, x,y):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 10
        self.scale = 2.0
        self.frame_count = 0
        self.frame_timer = 0.0


    def get_bb(self):
        half_width = self.width // 2
        half_height = self.height // 2
        return (self.x - half_width * self.scale, self.y - half_height * self.scale, self.x + half_width * self.scale, self.y + half_height * self.scale)

    def update(self):
        dt = Time.DeltaTime()
        # 프레임 애니메이션
        self.frame_timer += dt
        if self.frame_timer > 0.1:
            self.frame_count += 1
            self.frame_timer = 0.0

    def handle_collision(self, group, other):
        """충돌 처리"""

    def render(self, camera_x=0, camera_y=0, zoom=1.0):
        image, frame_count, width, height = ResourceManager.get_image(f"gold")
        if frame_count == 0:
            # 애니메이션이 없는 경우
            draw_x = int((self.x - camera_x) * zoom)
            draw_y = int((self.y - camera_y) * zoom) + int(height // 2 * zoom)
            image.draw(draw_x, draw_y, self.width * self.scale * zoom, self.height * self.scale * zoom)
        else:
            # 애니메이션이 있는 경우
            frame = self.frame_count % frame_count
            draw_x = int((self.x - camera_x) * zoom)
            draw_y = int((self.y - camera_y) * zoom) + int(height // 2 * zoom)
            image.clip_draw(frame * width // frame_count, 0, width // frame_count, height,
                            draw_x, draw_y, self.width * self.scale * zoom, self.height * self.scale * zoom)
