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
            self.mX = self.mTarget.x - (SceneManager.screen_width/2)  # 1280 / 2
            self.mY = self.mTarget.y - (SceneManager.screen_height/2)  # 720 / 2
            # Clamp to map bounds (2000x2000)
            if SceneManager.active_scene == 'BossStageScene':
                self.mX = max(0.0, min(self.mX, 0))
                self.mY = max(0.0, min(self.mY, 1600.0 - 720.0))
            else:
                self.mX = max(0.0, min(self.mX, 3200.0 - 1280.0))
                self.mY = max(0.0, min(self.mY, 1600.0 - 720.0))


    def set_target(self, target):
        self.mTarget = target

    def set_zoom(self, zoom):
        self.zoom = max(0.5, min(zoom, 3.0))  # 0.5~3.0배 제한
    def get_position(self):
        return self.mX, self.mY
    def get_zoom(self):
        return self.zoom
