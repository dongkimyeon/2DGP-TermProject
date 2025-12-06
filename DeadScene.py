import SceneManager
import pico2d
from Player import player


class DeadScene:
    def __init__(self):
        self.bgm = pico2d.load_music('resources/sound/Character/dead.wav')
        self.bgm.set_volume(32)

    def enter(self):
        print("[DeadScene] enter")
        self.bgm.play()
        player.coin_count = 0

    def exit(self):
        print("[DeadScene] exit")
        self.bgm.stop()

    def update(self):
        pass

    def render(self):
        image, frame_count, width, height = SceneManager.ResourceManager.get_image("Dead_background")
        if image:
            image.draw(SceneManager.screen_width // 2, SceneManager.screen_height // 2,
                       SceneManager.screen_width, SceneManager.screen_height)
        pass

    def handle_events(self, events):
        for event in events:
            if event.type == SceneManager.pico2d.SDL_QUIT:
                SceneManager.active_scene = None
            elif event.type == SceneManager.pico2d.SDL_KEYDOWN:
                if event.key == SceneManager.pico2d.SDLK_SPACE:
                    SceneManager.load_scene("TitleScene")
                    return True
        return False