import pico2d
from Time import Time
screen_width = 1920
screen_height = 1080

from ResourceManager import ResourceManager
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
        events = pico2d.get_events()

        # 씬의 handle_events 메서드 호출 (씬 전환 처리 포함)
        if active_scene and hasattr(active_scene, 'handle_events'):
            scene_changed = active_scene.handle_events(events)
            if scene_changed:
                continue  # 씬이 변경되면 다음 루프로

        update()
        render()


def change_scene(new_scene):
    """씬을 변경하는 함수"""
    global active_scene

    if active_scene and hasattr(active_scene, 'exit'):
        print(f"[SceneManager] exit: {type(active_scene).__name__}")
        active_scene.exit()

    active_scene = new_scene

    if active_scene and hasattr(active_scene, 'enter'):
        print(f"[SceneManager] enter: {type(active_scene).__name__}")
        active_scene.enter()

def update():
    if active_scene:
        active_scene.update()

def render():
    if active_scene:
        pico2d.clear_canvas()
        active_scene.render()
        pico2d.update_canvas()
