import pico2d
from Time import Time
screen_width = 1280
screen_height = 720

scenes = {}
active_scene = None
mfont = None
def CreateScene(name, scene_class):
    print(f"[SceneManager] CreateScene: {name} 인스턴스 생성")
    scenes[name] = scene_class()

def load_scene(name):
    global active_scene

    if active_scene and hasattr(active_scene, 'exit'):
        print(f"[SceneManager] exit: {type(active_scene).__name__}")
        active_scene.exit()
    active_scene = scenes[name]
    if active_scene and hasattr(active_scene, 'enter'):
        print(f"[SceneManager] enter: {type(active_scene).__name__}")
        active_scene.enter()

def run():
    print("[SceneManager] run")
    global mfont
    mfont = pico2d.load_font('resources/font/alagard.ttf', 50)

    while active_scene:
        Time.update()
        update()
        render()


def update():
    if active_scene:
        active_scene.update()



def render():
    if active_scene:
        pico2d.clear_canvas()
        active_scene.render()
        pico2d.update_canvas()

