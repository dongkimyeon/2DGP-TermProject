from ResourceManager import ResourceManager
from Time import Time
from Player import player
import math

class Boss:
    def __init__(self, x, y):
        self.health = 1000
        self.x = x
        self.y = y
        self.frame = 0
        self.frame_count = 0
        self.frame_timer = 0.0
        self.state = 'enter' # 'idle', 'attack', 'die', 'enter'
        self.dir = 0 # 1: right, -1: left
        self.is_hit = False
        self.width = 50
        self.height = 50
        self.detection_radius = 350
    def get_bb(self):
        half_width = self.width // 2
        half_height = self.height // 2
        return self.x - half_width, self.y - half_height + 7, self.x + half_width, self.y + half_height + 5
    def take_damage(self, damage):
        self.health -= damage
    def update(self):
        dt = Time.DeltaTime()

        dx = player.x - self.x
        dy = player.y - self.y
        angle = math.atan2(dy, dx)
        if angle > math.pi / 2 or angle < -math.pi / 2:
            self.dir = -1
        else:
            self.dir = 1

        #enter -> idle
        if self.state == 'enter':
            if self.frame_count >= 16:
                self.state = 'idle'
                self.frame_count = 0

        if self.health <= 0:
            self.state = 'die'
        self.frame_timer += dt
        if self.frame_timer > 0.1:
            self.frame_count += 1
            self.frame_timer = 0.0

    def render(self, camera_x=0, camera_y=0, zoom=1.0):
        image, frame_count, width, height = ResourceManager.get_image(f"niflheim_{self.state}")
        print(image, frame_count, width, height)
        frame = self.frame_count % frame_count
        draw_x = int((self.x - camera_x) * zoom)
        draw_y = int((self.y - camera_y) * zoom) + int(height // 2 * zoom) - 10
        draw_w = int(self.width * zoom)
        draw_h = int(self.height * zoom)
        if image:
            if self.dir == 1:
                image.clip_draw(frame * width // frame_count, 0, width // frame_count, height, draw_x,
                                draw_y, draw_w, draw_h)
            else:
                image.clip_composite_draw(frame * width // frame_count, 0, width // frame_count, height, 0, 'h',
                                          draw_x, draw_y, draw_w, draw_h)


