# BossUI.py
from ResourceManager import ResourceManager
import SceneManager
from Time import Time
import pico2d

class BossUI:
    def __init__(self, boss):
        # 보스 객체 참조
        self.boss = boss

        # 보스 UI 위치/스케일 (상단 중앙)
        self.hp_bar_scale = 5.0
        self.hp_bar_x = SceneManager.screen_width // 2
        self.hp_bar_y = SceneManager.screen_height - 50

        # LifeWave 애니메이션 변수 (PlayerUI와 유사하게 유지, 보스 체력 70% 이하 시 표시)
        self.wave_frame = 0
        self.wave_timer = 0.0
        self.wave_frame_duration = 0.1

    def update(self):
        # 애니메이션 타이머 업데이트
        dt = Time.DeltaTime()
        self.wave_timer += dt
        if self.wave_timer >= self.wave_frame_duration:
            self.wave_timer = 0.0
            self.wave_frame += 1

    def render(self):
        """체력바 렌더링"""
        # 체력 비율 계산
        hp_ratio = max(0, min(1, self.boss.health / self.boss.max_health))

        # 이미지 로드
        life_back, _, back_width, back_height = ResourceManager.get_image("BossLifeBaseBack")
        life_bar, _, bar_width, bar_height = ResourceManager.get_image("LifeBar")
        life_wave, frame_count, wave_width, wave_height = ResourceManager.get_image("LifeWave")
        life_base, _, base_width, base_height = ResourceManager.get_image("BossLifeBase")
        font = ResourceManager.get_font("HpText")

        # 체력바 배경 (뒤쪽)
        if life_back:
            life_back.draw(
                self.hp_bar_x,
                self.hp_bar_y,
                int(back_width * self.hp_bar_scale),
                int(back_height * self.hp_bar_scale)
            )

        # 체력 게이지
        if life_bar:
            # 체력 게이지 길이 계산 (비율에 따라)
            gauge_width = int(bar_width * hp_ratio) + 45
            gauge_height = bar_height

            # 클리핑 영역을 이용한 부분 렌더링
            if gauge_width > 0:
                # 원본 이미지에서 체력 비율만큼만 잘라서 그리기
                life_bar.clip_draw(
                    0, 0,  # 원본 이미지의 시작 위치
                    gauge_width, gauge_height,  # 잘라낼 크기
                    self.hp_bar_x - int((bar_width - gauge_width) * self.hp_bar_scale / 2) - 120,  # 왼쪽 정렬을 위한 위치 조정
                    self.hp_bar_y,
                    int(gauge_width * self.hp_bar_scale),
                    int(gauge_height * self.hp_bar_scale)
                )

                # LifeWave 애니메이션 (체력바의 오른쪽 끝에 붙여서 렌더링)
                # 체력이 70 이하일 때만 표시
                if life_wave and frame_count > 0 and hp_ratio > 0 :
                    # 프레임 루프 처리
                    current_frame = self.wave_frame % frame_count

                    # 체력바의 오른쪽 끝 위치 계산
                    wave_x = self.hp_bar_x - int((bar_width - gauge_width) * self.hp_bar_scale / 2)- 120 + int(
                        gauge_width * self.hp_bar_scale / 2)

                    # 프레임 단위로 잘라서 그리기
                    frame_width = wave_width // frame_count
                    life_wave.clip_draw(
                        current_frame * frame_width, 0,  # 현재 프레임 위치
                        frame_width, wave_height,  # 한 프레임의 크기
                        wave_x,
                        self.hp_bar_y,
                        int(frame_width * self.hp_bar_scale),
                        int(wave_height * self.hp_bar_scale)
                    )
        # 체력바 프레임 (앞쪽)
        if life_base:
            life_base.draw(
                self.hp_bar_x,
                self.hp_bar_y,
                int(base_width * self.hp_bar_scale),
                int(base_height * self.hp_bar_scale)
            )

        # HP 숫자 표시
        if font:
            hp_text = f"{int(self.boss.health)}  /  {int(self.boss.max_health)}"
            font.draw(
                self.hp_bar_x - int(9 * self.hp_bar_scale),
                self.hp_bar_y - int(0 * self.hp_bar_scale),
                hp_text,
                (255, 255, 255)
            )