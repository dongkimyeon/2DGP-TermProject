from ResourceManager import ResourceManager

class Portal:
    def __init__(self, x,y):
        self.x = x
        self.y = y
        self.width = 27
        self.height = 31
        self.scale = 2.0


    def get_bb(self):
        half_width = self.width // 2
        half_height = self.height // 2
        return (self.x - half_width * self.scale, self.y - half_height * self.scale + 10, self.x + half_width * self.scale, self.y + half_height * self.scale + 10)

    def update(self):
        pass


    def render(self, camera_x=0, camera_y=0, zoom=1.0):
        image, frame_count, width, height = ResourceManager.get_image(f"gate")
        draw_x = int((self.x - camera_x) * zoom)
        draw_y = int((self.y - camera_y) * zoom) + int(height // 2 * zoom)

        image.draw(draw_x, draw_y, self.width * self.scale * zoom, self.height * self.scale * zoom)



