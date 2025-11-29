import SceneManager



class RankingScene:
    def __init__(self):
        pass

    def enter(self):
        print("[RankingScene] enter")

    def exit(self):
        print("[RankingScene] exit")

    def update(self):
        pass

    def render(self):
        image, frame_count, width, height = SceneManager.ResourceManager.get_image("ranking_background")
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