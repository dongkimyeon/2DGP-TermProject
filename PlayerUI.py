from ResourceManager import ResourceManager
import pico2d
from Player import player
import SceneManager

class PlayerUI:
    def __init__(self):
        self.player = player
        # UI 스케일 (각각 분리)
        self.hp_bar_scale = 5.0
        self.dash_bar_scale = 7.0

        # 좌상단 위치로 조정 (피코투디는 왼쪽 아래가 0,0이므로 화면 높이 기준으로 계산)
        self.hp_bar_x = 200
        self.hp_bar_y = SceneManager.screen_height- 50  # 화면 상단에서 20픽셀 아래
        self.dash_bar_x = 50
        self.dash_bar_y = SceneManager.screen_height - 125  # HP바 아래 50픽셀

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

        # 코인 개수 렌더링
        self.render_coin()
        # 플레이 타임 렌더링
        self.render_playtime()
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
            gauge_width = int(bar_width * hp_ratio)
            gauge_height = bar_height

            # 클리핑 영역을 이용한 부분 렌더링
            if gauge_width > 0:
                # 원본 이미지에서 체력 비율만큼만 잘라서 그리기
                life_bar.clip_draw(
                    0, 0,  # 원본 이미지의 시작 위치
                    gauge_width, gauge_height,  # 잘라낼 크기
                    self.hp_bar_x - int((bar_width - gauge_width) * self.hp_bar_scale / 2),  # 왼쪽 정렬을 위한 위치 조정
                    self.hp_bar_y,
                    int(gauge_width * self.hp_bar_scale),
                    int(gauge_height * self.hp_bar_scale)
                )

                # LifeWave 애니메이션 (체력바의 오른쪽 끝에 붙여서 렌더링)
                # 체력이 70 이하일 때만 표시
                if life_wave and frame_count > 0 and hp_ratio > 0 and self.player.hp <= 70:
                    # 프레임 루프 처리
                    current_frame = self.wave_frame % frame_count

                    # 체력바의 오른쪽 끝 위치 계산
                    wave_x = self.hp_bar_x - int((bar_width - gauge_width) * self.hp_bar_scale / 2) + int(gauge_width * self.hp_bar_scale / 2)

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
            hp_text = f"{int(self.player.hp)}  /  {int(self.player.max_hp)}"
            font.draw(
                self.hp_bar_x - int(9 * self.hp_bar_scale),
                self.hp_bar_y - int(0 * self.hp_bar_scale),
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
            left_x = self.dash_bar_x + 4
            dash_base0.draw(
                left_x,
                self.dash_bar_y,
                int(base0_width * self.dash_bar_scale),
                int(base0_height * self.dash_bar_scale)
            )

            # 첫 번째 대쉬 아이콘
            if dash_count_img and self.player.dash_count >= 1:
                dash_count_img.draw(
                    left_x,
                    self.dash_bar_y,
                    int(count_width * self.dash_bar_scale),
                    int(count_height * self.dash_bar_scale)
                )

        # 중앙 베이스 (base1)
        if dash_base1:
            center_x = self.dash_bar_x + int(base0_width * self.dash_bar_scale) + base_spacing-3
            dash_base1.draw(
                center_x,
                self.dash_bar_y,
                int(base1_width * self.dash_bar_scale),
                int(base1_height * self.dash_bar_scale)
            )

            # 두 번째 대쉬 아이콘
            if dash_count_img and self.player.dash_count >= 2:
                dash_count_img.draw(
                    center_x,
                    self.dash_bar_y,
                    int(count_width * self.dash_bar_scale),
                    int(count_height * self.dash_bar_scale)
                )

        # 오른쪽 베이스 (base2)
        if dash_base2:
            right_x = self.dash_bar_x + int((base0_width + base1_width) * self.dash_bar_scale) + base_spacing * 2
            dash_base2.draw(
                right_x,
                self.dash_bar_y,
                int(base2_width * self.dash_bar_scale),
                int(base2_height * self.dash_bar_scale)
            )

            # 세 번째 대쉬 아이콘
            if dash_count_img and self.player.dash_count >= 3:
                dash_count_img.draw(
                    right_x,
                    self.dash_bar_y,
                    int(count_width * self.dash_bar_scale),
                    int(count_height * self.dash_bar_scale)
                )

    def render_coin(self):
        """코인 개수 렌더링"""
        coin_img, _, coin_width, coin_height = ResourceManager.get_image("CoinIcon")
        font = ResourceManager.get_font("default")

        if coin_img:
            coin_x = 50
            coin_y = SceneManager.screen_height - 175

            # 코인 아이콘 렌더링
            coin_img.draw(
                coin_x,
                coin_y,
                int(coin_width * 2.0),
                int(coin_height * 2.0)
            )


            if font:
                coin_text = f"x {self.player.coin_count}"
                font.draw(
                    coin_x + 30,
                    coin_y ,
                    coin_text,
                    (255, 255, 255)
                )

    def render_playtime(self):
        """플레이 타임 렌더링"""
        font = ResourceManager.get_font("HpText")
        if font:
            minutes = int(SceneManager.play_time) // 60
            seconds = int(SceneManager.play_time) % 60
            time_text = f"Time: {minutes:02}:{seconds:02}"
            font.draw(
                SceneManager.screen_width - 250,
                SceneManager.screen_height - 50,
                time_text,
                (255, 255, 255)
            )


