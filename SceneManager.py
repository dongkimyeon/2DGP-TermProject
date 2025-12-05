import pico2d
import playerSound
from Time import Time
screen_width = 1920
screen_height = 1080

from ResourceManager import ResourceManager
scenes = {}
active_scene = None

play_time = 0.0
play_timerOn = False

ps = None
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
    global ps
    ps = playerSound.PlayerSound()
    while active_scene:
        Time.update()
        events = pico2d.get_events()
        if play_timerOn:
            global play_time
            play_time += Time.DeltaTime()
        # 씬의 handle_events 메서드 호출 (씬 전환 처리 포함)
        if active_scene and hasattr(active_scene, 'handle_events'):
            scene_changed = active_scene.handle_events(events)
            if scene_changed:
                continue  # 씬이 변경되면 다음 루프로

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
