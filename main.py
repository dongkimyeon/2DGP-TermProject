import pico2d
import SceneManager
from Title_scene import TitleScene
from Stage1_scene import Stage1Scene

pico2d.open_canvas(SceneManager.screen_width, SceneManager.screen_height)

SceneManager.CreateScene("TitleScene", TitleScene)
SceneManager.CreateScene("Stage1Scene", Stage1Scene)

SceneManager.load_scene("TitleScene")

SceneManager.run()


pico2d.close_canvas()