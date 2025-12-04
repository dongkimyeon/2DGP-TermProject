
import pico2d

class SoundManager:
    def __init__(self):
        self.katanaSound = pico2d.load_wav("resources/sound/MeleeWeapon/katana.wav")
        self.jumpSound = pico2d.load_wav('resources/sound/player/jump.wav')
        self.walkSound1 = pico2d.load_wav("resources/sounds/player/step_lth1.wav")
        self.walkSound2 = pico2d.load_wav("resources/sounds/player/step_lth2.wav")
        self.walkSound3 = pico2d.load_wav("resources/sounds/player/step_lth3.wav")
        self.walkSound4 = pico2d.load_wav("resources/sounds/player/step_lth4.wav")
        self.dashSound = pico2d.load_wav("resources/sounds/player/dash.wav")
        self.gunFireSound = pico2d.load_wav("resources/sounds/weapon/LongDistanceWeapon/RifleFire.wav")
        self.getFairySound = pico2d.load_wav("resources/sounds/player/Get_Fairy.wav")
        self.getCoinSound = pico2d.load_wav("resources/sounds/player/gold_collect.wav")
        self.damagedSound = pico2d.load_wav("resources/sounds/player/Hit_Player.wav")
        self.katanaSound.set_volume(32)
        self.jumpSound.set_volume(32)
        self.walkSound1.set_volume(32)
        self.walkSound2.set_volume(32)
        self.walkSound3.set_volume(32)
        self.walkSound4.set_volume(32)
        self.dashSound.set_volume(32)
        self.getFairySound.set_volume(32)
        self.getCoinSound.set_volume(32)
        self.damagedSound.set_volume(32)
