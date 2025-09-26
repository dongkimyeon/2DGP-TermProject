import pico2d
from pico2d import load_image


class ImageManager:
    _instance = None

    def __init__(self):
        self.images = {}  # 이미지 객체를 저장하는 딕셔너리
        load_image("player_idle", 'resources/images/Characters/Player/Costume/Basic/player_idle.png')
        load_image("player_run", 'resources/images/Characters/Player/Costume/Basic/player_run.png')
        load_image("player_jump", 'resources/images/Characters/Player/Costume/Basic/player_jump.png')
        load_image("player_die", 'resources/images/Characters/Player/Costume/Basic/player_die.png')
    @staticmethod
    def instance():
        if ImageManager._instance is None:
            ImageManager._instance = ImageManager()
        return ImageManager._instance

    @staticmethod
    def load_image(name, path):
        inst = ImageManager.instance()
        if name not in inst.images:
            inst.images[name] = pico2d.load_image(path)
        return inst.images[name]

    @staticmethod
    def get_image(name):
        inst = ImageManager.instance()
        return inst.images.get(name, None)

    @staticmethod
    def unload_all():
        inst = ImageManager.instance()
        inst.images.clear()


