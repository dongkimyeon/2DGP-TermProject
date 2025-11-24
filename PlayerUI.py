from ResourceManager import ResourceManager
import pico2d
from Player import player
import SceneManager

class PlayerUI:
    def __init__(self):
        self.player = player
        # UI 스케일 (전체 UI 크기 조정)
        self.ui_scale = 3.0

        # 좌상단 위치로 조정 (피코투디는 왼쪽 아래가 0,0이므로 화면 높이 기준으로 계산)
        self.hp_bar_x = 100
        self.hp_bar_y = SceneManager.screen_height - 20  # 화면 상단에서 20픽셀 아래
        self.dash_bar_x = 30
        self.dash_bar_y = SceneManager.screen_height - 70  # HP바 아래 50픽셀

        # LifeWave 애니메이션 프레임
        self.wave_frame = 0
        self.wave_timer = 0.0
        self.wave_frame_duration = 0.1

    def update(self):
        """LifeWave 애니메이션 업데이트"""
        from Time import Time
        dt = Time.DeltaTime()
        self.wave_timer += dt
        if self.wave_timer >= self.wave_frame_duration:
            self.wave_timer = 0.0
            self.wave_frame += 1

    def render(self):
        # HP 바 렌더링
        self.render_hp_bar()
        
        # 대쉬 게이지 렌더링
        self.render_dash_bar()
    
    def render_hp_bar(self):
        """체력바 렌더링"""
        # 체력 비율 계산
        hp_ratio = max(0, min(1, self.player.hp / self.player.max_hp))
        
        # 이미지 로드
        life_back, _, back_width, back_height = ResourceManager.get_image("PlayerLifeBaseBack")
        life_bar, _, bar_width, bar_height = ResourceManager.get_image("LifeBar")
        life_wave, frame_count, wave_width, wave_height = ResourceManager.get_image("LifeWave")
        life_base, _, base_width, base_height = ResourceManager.get_image("PlayerLifeBase")
        font = ResourceManager.get_font("default")

        # 체력바 배경 (뒤쪽)
        if life_back:
            life_back.draw(
                self.hp_bar_x,
                self.hp_bar_y,
                int(back_width * self.ui_scale),
                int(back_height * self.ui_scale)
            )

        # 체력 게이지 (LifeBar) - HP 비율에 따라 가로로 늘어남
        if life_bar and hp_ratio > 0:
            # LifeBar의 시작 위치 (왼쪽 끝)
            bar_left_x = self.hp_bar_x - int(bar_width * self.ui_scale // 2)

            # 체력 비율만큼의 너비 계산
            actual_bar_width = int(bar_width * hp_ratio)
            scaled_bar_width = int(actual_bar_width * self.ui_scale)

            # LifeBar를 왼쪽에서 오른쪽으로 늘어나게 렌더링
            life_bar.clip_draw(
                0, 0, actual_bar_width, bar_height,
                bar_left_x + scaled_bar_width // 2,  # 중심점이 이동하도록
                self.hp_bar_y,
                scaled_bar_width,
                int(bar_height * self.ui_scale)
            )

            # LifeBar의 오른쪽 끝 위치 계산
            bar_right_x = bar_left_x + scaled_bar_width
        else:
            bar_right_x = self.hp_bar_x - int(bar_width * self.ui_scale // 2)

        # 체력바 웨이브 효과 (애니메이션) - LifeBar 오른쪽 끝에서 나옴
        if life_wave and hp_ratio > 0 and frame_count > 0:
            # 애니메이션 프레임 순환
            current_frame = self.wave_frame % frame_count
            frame_width = wave_width // frame_count

            # LifeWave를 LifeBar의 오른쪽 끝에서 렌더링
            life_wave.clip_draw(
                current_frame * frame_width, 0, frame_width, wave_height,
                bar_right_x + int(frame_width * self.ui_scale // 2),  # LifeBar 오른쪽 끝에 붙음
                self.hp_bar_y,
                int(frame_width * self.ui_scale),
                int(wave_height * self.ui_scale)
            )

        # 체력바 프레임 (앞쪽)
        if life_base:
            life_base.draw(
                self.hp_bar_x,
                self.hp_bar_y,
                int(base_width * self.ui_scale),
                int(base_height * self.ui_scale)
            )

        # HP 숫자 표시
        if font:
            hp_text = f"{int(self.player.hp)}/{int(self.player.max_hp)}"
            font.draw(
                self.hp_bar_x - int(30 * self.ui_scale),
                self.hp_bar_y - int(5 * self.ui_scale),
                hp_text,
                (255, 255, 255)
            )

    def render_dash_bar(self):
        """대쉬 게이지 렌더링"""
        # 대쉬 카운트 이미지
        dash_count_img, _, count_width, count_height = ResourceManager.get_image("DashCount")

        # 대쉬 베이스 이미지들
        dash_base0, _, base0_width, base0_height = ResourceManager.get_image("DashCountBase1")
        dash_base1, _, base1_width, base1_height = ResourceManager.get_image("DashCountBase0")
        dash_base2, _, base2_width, base2_height = ResourceManager.get_image("DashCountBase2")

        # 3개의 베이스를 가로로 나란히 배치 (왼쪽부터 base0, base1, base2)
        base_spacing = 0  # 베이스 간격

        # 왼쪽 베이스 (base0)
        if dash_base0:
            left_x = self.dash_bar_x
            dash_base0.draw(
                left_x,
                self.dash_bar_y,
                int(base0_width * self.ui_scale),
                int(base0_height * self.ui_scale)
            )

            # 첫 번째 대쉬 아이콘
            if dash_count_img and self.player.dash_count >= 1:
                dash_count_img.draw(
                    left_x,
                    self.dash_bar_y,
                    int(count_width * self.ui_scale),
                    int(count_height * self.ui_scale)
                )

        # 중앙 베이스 (base1)
        if dash_base1:
            center_x = self.dash_bar_x + int(base0_width * self.ui_scale) + base_spacing-3
            dash_base1.draw(
                center_x,
                self.dash_bar_y,
                int(base1_width * self.ui_scale),
                int(base1_height * self.ui_scale)
            )

            # 두 번째 대쉬 아이콘
            if dash_count_img and self.player.dash_count >= 2:
                dash_count_img.draw(
                    center_x,
                    self.dash_bar_y,
                    int(count_width * self.ui_scale),
                    int(count_height * self.ui_scale)
                )

        # 오른쪽 베이스 (base2)
        if dash_base2:
            right_x = self.dash_bar_x + int((base0_width + base1_width) * self.ui_scale) + base_spacing * 2
            dash_base2.draw(
                right_x,
                self.dash_bar_y,
                int(base2_width * self.ui_scale),
                int(base2_height * self.ui_scale)
            )

            # 세 번째 대쉬 아이콘
            if dash_count_img and self.player.dash_count >= 3:
                dash_count_img.draw(
                    right_x,
                    self.dash_bar_y,
                    int(count_width * self.ui_scale),
                    int(count_height * self.ui_scale)
                )

        # 대쉬 카운트 숫자 표시
        font = ResourceManager.get_font("default")
        if font:
            dash_text = f"Dash: {self.player.dash_count}/3"
            font.draw(
                self.dash_bar_x + int(5 * self.ui_scale),
                self.dash_bar_y - int(35 * self.ui_scale),
                dash_text,
                (255, 255, 255)
            )
