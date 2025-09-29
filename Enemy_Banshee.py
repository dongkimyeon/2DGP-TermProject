from Time import Time
from ImageManager import ImageManager
import pico2d
import SceneManager
import math


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
        self.detection_radius = 200
        self.attack_cooldown = 2.0

    def attack(self):
        return self.attack_power

    def take_damage(self, damage):
        self.is_hit = True
        damage_taken = damage - self.defense
        if damage_taken < 0:
            damage_taken = 0
        self.health -= damage_taken
        return damage_taken

    def set_position(self, x, y):
        self.x = x
        self.y = y
    def update(self):
        pass
    def render(self):
        pass

    def is_dead(self):
        return self.health <= 0

