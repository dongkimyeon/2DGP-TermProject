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
        # Player 이미지 로드
        self.load_image("player_idle", 'resources/images/Characters/Player/Costume/Basic/player_idle.png', 5)
        self.load_image("player_run", 'resources/images/Characters/Player/Costume/Basic/player_run.png', 8)
        self.load_image("player_jump", 'resources/images/Characters/Player/Costume/Basic/player_jump.png', 1)
        self.load_image("player_die", 'resources/images/Characters/Player/Costume/Basic/player_die.png', 1)
        # TitleScene 이미지 로드
        self.load_image("backCloud", 'resources/images/TitleScene/BackCloud.png')
        self.load_image("frontCloud", 'resources/images/TitleScene/FrontCloud.png')
        self.load_image("titleBackground", 'resources/images/TitleScene/background.png')
        self.load_image("mainlogo", 'resources/images/TitleScene/MainLogo.png')
        self.load_image("exit_off", 'resources/images/TitleScene/ExitOff_Kor.png')
        self.load_image("exit_on", 'resources/images/TitleScene/ExitOn_Kor.png')
        self.load_image("play_off", 'resources/images/TitleScene/PlayOff_Kor.png')
        self.load_image("play_on", 'resources/images/TitleScene/PlayOn_Kor.png')
        # Stage1Scene 배경 이미지 로드
        self.load_image("forest_back_Layer_0", 'resources/images/Map/ForestBackLayer0.png')
        self.load_image("forest_back_Layer_1", 'resources/images/Map/ForestBackLayer1.png')
        self.load_image("forest_back_Layer_2", 'resources/images/Map/ForestBackLayer2.png')

        # Banshee 이미지 로드
        self.load_image("banshee_idle", 'resources/images/Enemy/Banshee/idle.png', 6)
        self.load_image("banshee_idle_shot", 'resources/images/Enemy/Banshee/idle_shot.png', 6)
        self.load_image("banshee_attack", 'resources/images/Enemy/Banshee/attack.png', 6)
        self.load_image("banshee_attack_shot", 'resources/images/Enemy/Banshee/attack_shot.png', 6)
        self.load_image("note", "resources/images/Enemy/Bullet/note.png",4)
        self.load_image("note_hit", "resources/images/Enemy/Bullet/note_FX.png",6)

        # Bat 이미지 로드
        self.load_image("bat_move", "resources/images/Enemy/Bat/Normal/move.png" ,6)
        self.load_image("bat_move_shot", "resources/images/Enemy/Bat/Normal/move_shot.png",6)
        self.load_image("bat_bullet", "resources/images/Enemy/Bullet/smallBullet.png",5)
        self.load_image("bat_bullet_hit", "resources/images/Enemy/Bullet/smallBullet_FX.png",7)

        # Ghost 이미지 로드
        self.load_image("ghost_move", "resources/images/Enemy/Ghost/move.png",6)
        self.load_image("ghost_attack", "resources/images/Enemy/Ghost/attack.png",3)
        self.load_image("ghost_move_shot", "resources/images/Enemy/Ghost/move_shot.png",6)
        self.load_image("ghost_attack_shot", "resources/images/Enemy/Ghost/attack_shot.png",3)

        # Skel 이미지 로드
        self.load_image("skel_idle", "resources/images/Enemy/Skel/Big_Normal/idle.png",5)
        self.load_image("skel_idle_shot", "resources/images/Enemy/Skel/Big_Normal/idle_shot.png",5)
        self.load_image("skel_move", "resources/images/Enemy/Skel/Big_Normal/move.png",6)
        self.load_image("skel_move_shot", "resources/images/Enemy/Skel/Big_Normal/move_shot.png",6)
        self.load_image("skel_attack", "resources/images/Enemy/Skel/Big_Normal/attack.png",12)
        self.load_image("skel_attack_shot", "resources/images/Enemy/Skel/Big_Normal/attack_shot.png",12)

        # Katana 관련 이미지 로드
        self.load_image("katana", 'resources/images/SwordWeapon/Katana.png')
        self.load_image("katana_effect", 'resources/images/SwordWeapon/Katana_Effect.png', 9)
        self.load_image("katana_effect_ex", 'resources/images/SwordWeapon/Kanata_Effect_Ex.png', 10)






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


