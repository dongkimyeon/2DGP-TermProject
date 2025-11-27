#카메라 수정
import SceneManager
class Camera:
    def __init__(self):
        self.mX = 0.0
        self.mY = 0.0
        self.mTarget = None
        self.zoom = 1.5  # 확대/축소 비율


    def update(self):
        if self.mTarget:
            # Center camera on player
            self.mX = self.mTarget.x - 640.0  # 1280 / 2
            self.mY = self.mTarget.y - 360.0  # 720 / 2
            # 보스 스테이지 판별
            active = SceneManager.active_scene
            is_boss = False
            try:
                is_boss = (hasattr(active, '__class__') and
                           active.__class__.__name__ == 'BossStageScene')
            except Exception:
                is_boss = False
            if is_boss:
                self.mX = max(0.0, min(self.mX, 16))
                self.mY = max(0.0, min(self.mY, 100))
                #self.zoom = 1.0
            else:
                self.mX = max(0.0, min(self.mX, 3200.0 - 1280.0))
                self.mY = max(0.0, min(self.mY, 1600-720))


    def set_target(self, target):
        self.mTarget = target

    def set_zoom(self, zoom):
        self.zoom = max(0.5, min(zoom, 3.0))  # 0.5~3.0배 제한
    def get_position(self):
        return self.mX, self.mY
    def get_zoom(self):
        return self.zoom
