import pico2d
import SceneManager
from BossStage_scene import BossStageScene
from Title_scene import TitleScene
from Stage1_scene import Stage1Scene
from Stage2_scene import Stage2Scene
from RankingScene import RankingScene
from DeadScene import DeadScene

pico2d.open_canvas(SceneManager.screen_width, SceneManager.screen_height)

SceneManager.CreateScene("TitleScene", TitleScene)
SceneManager.CreateScene("Stage1Scene", Stage1Scene)
SceneManager.CreateScene("Stage2Scene", Stage2Scene)
SceneManager.CreateScene("BossStageScene", BossStageScene)
SceneManager.CreateScene("RankingScene", RankingScene)
SceneManager.CreateScene("DeadScene", DeadScene)


SceneManager.load_scene("BossStageScene")

SceneManager.run()


pico2d.close_canvas()