from Time import Time
from ImageManager import ImageManager
import pico2d
import SceneManager
import math
from Player import player



class Ghost:
    def __init__(self):
        self.health = 50
        self.attack_power = 12
        self.x = 0
        self.y = 0
        self.moveSpeed = 150  # Bat의 이동 속도(초당 픽셀)

        self.frame = 0
        self.frame_count = 0
        self.frame_timer = 0.0
        self.state = 'move'  # 'move' , 'attack', 'attack_shot', 'move_shot'
        self.is_hit = False
        self.is_dead = False
        self.width = 50
        self.height = 50
        self.detection_radius = 350
        self.attack_cooldown = 0.0  # 쿨타임 1초

    def attack(self):
        return self.attack_power

    def move(self):
       pass


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

        self.move()
        # 프레임 애니메이션
        self.frame_timer += dt
        if self.frame_timer > 0.1:
            self.frame_count += 1
            self.frame_timer = 0.0

    def render(self):
        image, frame_count, width, height = ImageManager.get_image(f"ghost_{self.state}")
        frame = self.frame_count % frame_count
        if image:
            image.clip_draw(frame * width // frame_count, 0, width // frame_count, height, int(self.x), int(self.y) + height // 2, self.width, self.height)

    def is_dead(self):
        return self.health <= 0
