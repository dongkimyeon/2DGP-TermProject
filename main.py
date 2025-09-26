import pico2d
import SceneManager
from Title_scene import TitleScene
from Stage1_scene import Stage1Scene

print("[main.py] Canvas open 시작")
pico2d.open_canvas(SceneManager.screen_width, SceneManager.screen_height)

print("[main.py] TitleScene, Stage1Scene 등록")
SceneManager.CreateScene("TitleScene", TitleScene)
SceneManager.CreateScene("Stage1Scene", Stage1Scene)

print("[main.py] TitleScene 로드")
SceneManager.load_scene("TitleScene")

print("[main.py] 게임 루프 시작")
SceneManager.run()

print("[main.py] Canvas close")
pico2d.close_canvas()