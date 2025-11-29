import SceneManager
import os
from ResourceManager import ResourceManager



class RankingScene:
    def __init__(self):
        # 폰트 로드 및 레코드 읽기

        self.records = self.load_records()

    def enter(self):
        print("[RankingScene] enter")
        # 씬에 진입할 때 최신 기록 다시 로드
        self.records = self.load_records()

    def exit(self):
        print("[RankingScene] exit")

    def update(self):
        pass

    def load_records(self):
        # record.txt는 프로젝트 루트에 존재함
        path = os.path.join(os.path.dirname(__file__), 'record.txt')
        if not os.path.exists(path):
            return []
        records = []
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                s = line.strip()
                if not s:
                    continue
                # 각 줄은 초 단위 실수로 저장되어 있다고 가정
                try:
                    t = float(s)
                    records.append(t)
                except Exception:
                    # 예외적인 포맷(예: 이름,콤마 포함 등)은 무시
                    continue
        # 시간 빠른 순 (오름차순)
        records.sort()
        return records

    def render(self):
        # 배경 그리기
        image, frame_count, width, height = SceneManager.ResourceManager.get_image("ranking_background")
        if image:
            image.draw(SceneManager.screen_width // 2, SceneManager.screen_height // 2,
                       SceneManager.screen_width, SceneManager.screen_height)

        # 레코드 출력
        font = ResourceManager.get_font("RankingFont")
        start_x = SceneManager.screen_width // 2 - 200
        start_y = SceneManager.screen_height - 360
        line_height = 70
        max_show = 10
        for i, t in enumerate(self.records[:max_show]):
            minutes = int(t) // 60
            seconds = int(t) % 60
            millis = int((t - int(t)) * 1000)
            time_text = f"{i + 1:2}. {minutes:02}:{seconds:02}.{millis:01}"
            try:
                font.draw(start_x, start_y - i * line_height, time_text, (0, 0, 0))
            except TypeError:
                font.draw(start_x, start_y - i * line_height, time_text)


    def handle_events(self, events):
        for event in events:
            if event.type == SceneManager.pico2d.SDL_QUIT:
                SceneManager.active_scene = None
            elif event.type == SceneManager.pico2d.SDL_KEYDOWN:
                if event.key == SceneManager.pico2d.SDLK_SPACE:
                    SceneManager.load_scene("TitleScene")
                    return True
        return False