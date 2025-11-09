from ResourceManager import ResourceManager
from Time import Time
from Player import player
from IceBullet import IceBullet
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
        self.pattern = 'none' # 'ice_bullet', 'ice_spear' , 'icicle_fall'
        self.dir = 0 # 1: right, -1: left
        self.is_hit = False
        self.width = 68
        self.height = 60

        self.attack_timer = 0.0

        self.font = ResourceManager.get_font("default")
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
        #idle -> attack
        elif self.state == 'idle':
            if self.attack_timer > 3.0:
                self.state = 'attack'
                self.frame_count = 0
                self.attack_timer = 0.0

        #attack -> idle
        elif self.state == 'attack':
            # 프레임 타이밍에 맞춰 아이스불렛 발사
            if self.frame_count == 6:
            # 프레임 타이밍에 맞춰 아이스불렛 발사 (부채꼴 5발, 한 번만)
                self.state = 'idle'
                # 총알 개수와 스프레드 각도(라디안)
                count = 5
                step_deg = 10  # 각 탄 사이의 간격(도)
                half_span = (step_deg * (count - 1)) / 2.0
                # 생성
                for i in range(count):
                    offset_deg = -half_span + i * step_deg
                    offset_rad = math.radians(offset_deg)
                    bullet_angle = angle + offset_rad
                    IceBullet().shot(self.x, self.y, bullet_angle, speed=350)

                self.frame_count = 0
                self.attack_timer = 0.0


        self.frame_timer += dt
        self.attack_timer += dt
        if self.frame_timer > 0.1:
            self.frame_count += 1
            self.frame_timer = 0.0


        print(self.frame_count)


    def render(self, camera_x=0, camera_y=0, zoom=1.0):
        image, frame_count, width, height = ResourceManager.get_image(f"niflheim_{self.state}")
        frame = self.frame_count % frame_count
        draw_x = int((self.x - camera_x) * zoom)
        draw_y = int((self.y - camera_y) * zoom) + int(height // 2 * zoom) - 10
        draw_w = int(self.width * zoom)
        draw_h = int(self.height * zoom)
        self.font.draw(10, 30, f'HP: {self.health}', (255, 0, 0))

        if image:
            if self.dir == 1:
                image.clip_draw(frame * width // frame_count, 0, width // frame_count, height, draw_x,
                                draw_y, draw_w, draw_h)
            else:
                image.clip_composite_draw(frame * width // frame_count, 0, width // frame_count, height, 0, 'h',
                                          draw_x, draw_y, draw_w, draw_h)
