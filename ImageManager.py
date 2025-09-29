import pico2d

class ImageManager:
    _instance = None
    _initialized = False

    def __init__(self):
        self.images = {}

    @staticmethod
    def instance():
        if ImageManager._instance is None:
            ImageManager._instance = ImageManager()
            if not ImageManager._initialized:
                ImageManager._instance._init_images()
                ImageManager._initialized = True
        return ImageManager._instance

    def _init_images(self):
        self.load_image("player_idle", 'resources/images/Characters/Player/Costume/Basic/player_idle.png', 5)
        self.load_image("player_run", 'resources/images/Characters/Player/Costume/Basic/player_run.png', 8)
        self.load_image("player_jump", 'resources/images/Characters/Player/Costume/Basic/player_jump.png', 1)
        self.load_image("player_die", 'resources/images/Characters/Player/Costume/Basic/player_die.png', 1)
        self.load_image("backCloud", 'resources/images/TitleScene/BackCloud.png')
        self.load_image("frontCloud", 'resources/images/TitleScene/FrontCloud.png')
        self.load_image("titleBackground", 'resources/images/TitleScene/background.png')
        self.load_image("mainlogo", 'resources/images/TitleScene/MainLogo.png')
        self.load_image("exit_off", 'resources/images/TitleScene/ExitOff_Kor.png')
        self.load_image("exit_on", 'resources/images/TitleScene/ExitOn_Kor.png')
        self.load_image("play_off", 'resources/images/TitleScene/PlayOff_Kor.png')
        self.load_image("play_on", 'resources/images/TitleScene/PlayOn_Kor.png')
        self.load_image("forest_back_Layer_0", 'resources/images/Map/ForestBackLayer0.png')
        self.load_image("forest_back_Layer_1", 'resources/images/Map/ForestBackLayer1.png')
        self.load_image("forest_back_Layer_2", 'resources/images/Map/ForestBackLayer2.png')
        self.load_image("banshee_idle", 'resources/images/Enemy/Banshee/idle.png', 6)
        self.load_image("banshee_idle_attacked", 'resources/images/Enemy/Banshee/idle_shot.png', 6)
        self.load_image("banshee_attack", 'resources/images/Enemy/Banshee/attack.png', 6)
        self.load_image("banshee_attack_attacked", 'resources/images/Enemy/Banshee/attack_shot.png', 6)
        self.load_image("note", "resources/images/Enemy/Bullet/note.png",4)




    @staticmethod
    def load_image(name, path, frame_count=1):
        inst = ImageManager.instance()
        if name not in inst.images:
            img = pico2d.load_image(path)
            width = img.w if hasattr(img, 'w') else 0
            height = img.h if hasattr(img, 'h') else 0
            print(f"[ImageManager] Load: {name}, w={width}, h={height}")
            inst.images[name] = (img, frame_count, width, height)
        return inst.images[name]

    @staticmethod
    def get_image(name):
        inst = ImageManager.instance()
        return inst.images.get(name, (None, 0, 0, 0))

    @staticmethod
    def unload_all():
        inst = ImageManager.instance()
        inst.images.clear()

# 사용 예시:
# ImageManager.load_image("player_idle", "경로", 6)
# img, frame_count, width, height = ImageManager.get_image("player_idle")
# width, height는 자동으로 img.w, img.h 값이 들어감
