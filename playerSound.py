import pico2d


class PlayerSound:
    def __init__(self):
        self.dash = pico2d.load_wav('resources/sound/Character/dash.wav')
        self.Get_Fairy = pico2d.load_wav('resources/sound/Character/Get_Fairy.wav')
        self.gold_collect = pico2d.load_wav('resources/sound/Character/gold_collect.wav')
        self.Hit_Player = pico2d.load_wav('resources/sound/Character/Hit_Player.wav')
        self.jump = pico2d.load_wav('resources/sound/Character/jump.wav')
        self.katana = pico2d.load_wav('resources/sound/Character/katana.wav')
        self.RifleFire = pico2d.load_wav('resources/sound/Character/RifleFire.wav')
        self.step_lth1 = pico2d.load_wav('resources/sound/Character/step_lth1.wav')
        self.step_lth2 = pico2d.load_wav('resources/sound/Character/step_lth2.wav')
        self.step_lth3 = pico2d.load_wav('resources/sound/Character/step_lth3.wav')
        self.step_lth4 = pico2d.load_wav('resources/sound/Character/step_lth4.wav')
        self.swap = pico2d.load_wav('resources/sound/Character/swap.wav')

        self.dash.set_volume(32)
        self.Get_Fairy.set_volume(32)
        self.gold_collect.set_volume(32)
        self.Hit_Player.set_volume(32)
        self.jump.set_volume(32)
        self.katana.set_volume(32)
        self.RifleFire.set_volume(32)
        self.step_lth1.set_volume(32)
        self.step_lth2.set_volume(32)
        self.step_lth3.set_volume(32)
        self.step_lth4.set_volume(32)
        self.swap.set_volume(32)





