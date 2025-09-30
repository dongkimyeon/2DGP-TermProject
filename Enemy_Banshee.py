from Time import Time
from ImageManager import ImageManager
import pico2d
import SceneManager
import math
from Player import player
from Banshee_Attack_note import Note


class Banshee:
    def __init__(self):
        self.health = 50
        self.attack_power = 12
        self.x = 0
        self.y = 0
        self.frame = 0
        self.frame_count = 0
        self.frame_timer = 0.0
        self.state = 'idle'  # 'idle', 'attack', 'hit'
        self.is_hit = False
        self.is_dead = False
        self.width = 50
        self.height = 50
        self.detection_radius = 350
        self.attack_cooldown = 2.0
        self.note_fired = False

    def attack(self):
        return self.attack_power

    def take_damage(self, damage):

        self.health -= damage
    def get_bb(self):
        half_width = self.width // 2
        half_height = self.height // 2
        return (self.x - half_width, self.y - half_height + 7, self.x + half_width, self.y + half_height + 5)

    def set_position(self, x, y):
        self.x = x
        self.y = y
    def update(self):
        dt = Time.DeltaTime()

        #플레이어 감지
        if(player.x - self.x)**2 + (player.y - self.y)**2 < self.detection_radius**2:
            if self.state != 'attack':
                self.state = 'attack'
                self.frame_count = 0
                self.note_fired = False
        # 프레임 애니메이션
        self.frame_timer += dt
        if self.frame_timer > 0.1:
            self.frame_count += 1
            self.frame_timer = 0.0



    def render(self):
        image, frame_count, width, height = ImageManager.get_image(f"banshee_{self.state}")
        frame = self.frame_count % frame_count
        if image:
            image.clip_draw(frame * width // frame_count, 0, width // frame_count, height, int(self.x), int(self.y) + height // 2, self.width, self.height)
            if self.state == 'attack':
                if frame == frame_count - 1 and not self.note_fired:
                    # 16방향으로 Note 발사 (한 번만)
                    for i in range(16):
                        angle = (2 * math.pi / 16) * i
                        Note().shot(self.x, self.y, angle, 300)
                    self.note_fired = True
                if frame == frame_count - 1:
                    self.state = 'idle'


        pass

    def is_dead(self):
        return self.health <= 0
