class Camera:
    def __init__(self):
        self.mX = 0.0
        self.mY = 0.0
        self.mTarget = None
        self.zoom = 1.5  # 확대/축소 비율


    def update(self):
        if self.mTarget:
            # Center camera on player (viewport 1280x720)
            self.mX = self.mTarget.x - 640.0  # 1280 / 2
            self.mY = self.mTarget.y - 360.0  # 720 / 2
            # Clamp to map bounds (2000x2000)
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
