# SceneManager를 통해서만 씬을 관리하도록 변경
import SceneManager

screen_width = SceneManager.screen_width
screen_height = SceneManager.screen_height

# game_framework에서는 SceneManager의 함수만 래핑
CreateScene = SceneManager.CreateScene
load_scene = SceneManager.load_scene
run = SceneManager.run
update = SceneManager.update
render = SceneManager.render
