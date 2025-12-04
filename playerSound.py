import pico2d


class PlayerSound:
    def __init__(self):
        self.jump_sound = pico2d.load_wav('Sound/jump.wav')
        self.jump_sound.set_volume(64)
        self.attack_sound = pico2d.load_wav('Sound/attack.wav')
        self.attack_sound.set_volume(64)
        self.hurt_sound = pico2d.load_wav('Sound/hurt.wav')
        self.hurt_sound.set_volume(64)
        self.die_sound = pico2d.load_wav('Sound/die.wav')
        self.die_sound.set_volume(64)


