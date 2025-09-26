from pico2d import clear_canvas, update_canvas

import SceneManager
import pico2d
from Time import Time
from ImageManager import ImageManager




class TitleScene:
    def __init__(self):
        print("[TitleScene] __init__()")
        self.backCloud, _, self.backCloud_width, self.backCloud_height = ImageManager.get_image("backCloud")
        self.frontCloud, _, self.frontCloud_width, self.frontCloud_height = ImageManager.get_image("frontCloud")
        self.backGround, _, self.backGround_width, self.backGround_height = ImageManager.get_image("titleBackground")
        self.mainLogo, _, self.mainLogo_width, self.mainLogo_height = ImageManager.get_image("mainlogo")

        #버튼
        self.play_On, _, self.play_On_width, self.play_On_height = ImageManager.get_image("play_on")
        self.play_Off, _, self.play_Off_width, self.play_Off_height = ImageManager.get_image("play_off")
        self.exit_On, _, self.exit_On_width, self.exit_On_height = ImageManager.get_image("exit_on")
        self.exit_Off, _, self.exit_Off_width, self.exit_Off_height = ImageManager.get_image("exit_off")

        self.screen_width = SceneManager.screen_width
        self.screen_height = SceneManager.screen_height
        self.backCloud_x = 0.0
        self.frontCloud_x = 0.0
        self.backCloud_speed = 80
        self.frontCloud_speed = 120

        #버튼 호버링 변수
        self.play_button_hover = False
        self.exit_button_hover = False


    def enter(self):
        print("[TitleScene] enter()")


    def exit(self):
        print("[TitleScene] exit()")
        self.backCloud = None
        self.frontCloud = None


    def update(self):
        dt = Time.DeltaTime()

        self.backCloud_x += self.backCloud_speed * dt
        self.frontCloud_x += self.frontCloud_speed * dt

        if self.backCloud_x >= self.screen_width:
            self.backCloud_x -= self.screen_width
        if self.frontCloud_x >= self.screen_width:
            self.frontCloud_x -= self.screen_width

        events = pico2d.get_events()
        for event in events:
            if event.type == pico2d.SDL_QUIT:
                pico2d.quit()
                exit()

            elif event.type == pico2d.SDL_MOUSEMOTION:
                mouse_x, mouse_y = event.x, self.screen_height - event.y

                # play button hover check
                if (self.screen_width // 2 - (self.play_On_width * 10.0) // 2 <= mouse_x <= self.screen_width // 2 + (self.play_On_width * 10.0) // 2 and
                    self.screen_height // 2 - 100 - (self.play_On_height * 10.0) // 2 <= mouse_y <= self.screen_height // 2 - 100 + (self.play_On_height * 10.0) // 2):
                    self.play_button_hover = True
                else:
                    self.play_button_hover = False

                # exit button hover check
                if (self.screen_width // 2 - (self.exit_On_width * 10.0) // 2 <= mouse_x <= self.screen_width // 2 + (self.exit_On_width * 10.0) // 2 and
                    self.screen_height // 2 - 300 - (self.exit_On_height * 10.0) // 2 <= mouse_y <= self.screen_height // 2 - 300 + (self.exit_On_height * 10.0) // 2):
                    self.exit_button_hover = True
                else:
                    self.exit_button_hover = False

            elif event.type == pico2d.SDL_MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.x, self.screen_height - event.y

                # play button click check
                if (self.screen_width // 2 - (self.play_On_width * 10.0) // 2 <= mouse_x <= self.screen_width // 2 + (self.play_On_width * 10.0) // 2 and
                    self.screen_height // 2 - 100 - (self.play_On_height * 10.0) // 2 <= mouse_y <= self.screen_height // 2 - 100 + (self.play_On_height * 10.0) // 2):
                    print("[TitleScene] Play 버튼 클릭, Stage1Scene으로 전환")
                    SceneManager.load_scene("Stage1Scene")

                # exit button click check
                if (self.screen_width // 2 - (self.exit_On_width * 10.0) // 2 <= mouse_x <= self.screen_width // 2 + (self.exit_On_width * 10.0) // 2 and
                    self.screen_height // 2 - 300 - (self.exit_On_height * 10.0) // 2 <= mouse_y <= self.screen_height // 2 - 300 + (self.exit_On_height * 10.0) // 2):
                    print("[TitleScene] Exit 버튼 클릭, 게임 종료")
                    pico2d.quit()
                    exit()



    def render(self):
        # background
        self.backGround.draw(self.screen_width // 2, self.screen_height // 2, self.screen_width, self.screen_height)

        # backCloud
        self.backCloud.draw(self.screen_width // 2 - self.backCloud_x, self.screen_height // 2, self.screen_width, self.screen_height)
        self.backCloud.draw(self.screen_width // 2 - self.backCloud_x + self.screen_width, self.screen_height // 2, self.screen_width, self.screen_height)
        # frontCloud
        self.frontCloud.draw(self.screen_width // 2 - self.frontCloud_x, self.screen_height // 2, self.screen_width, self.screen_height)
        self.frontCloud.draw(self.screen_width // 2 - self.frontCloud_x + self.screen_width, self.screen_height // 2, self.screen_width, self.screen_height)
        # mainLogo (중앙 상단)
        self.mainLogo.draw(self.screen_width // 2, self.screen_height - self.mainLogo_height // 2 - 300 , self.mainLogo_width * 5.0, self.mainLogo_height * 5.0)
        buttonScale = 10.0

        # play button (중앙 하단)
        if(self.play_button_hover):
            self.play_On.draw(self.screen_width // 2, self.screen_height // 2 - 100, self.play_On_width * buttonScale, self.play_On_height * buttonScale)
        else:
            self.play_Off.draw(self.screen_width // 2, self.screen_height // 2 - 100, self.play_Off_width * buttonScale, self.play_Off_height * buttonScale)

        # exit button (중앙 하단)
        if(self.exit_button_hover):
            self.exit_On.draw(self.screen_width // 2, self.screen_height // 2 - 300, self.exit_On_width * buttonScale, self.exit_On_height * buttonScale)
        else:
            self.exit_Off.draw(self.screen_width // 2, self.screen_height // 2 - 300, self.exit_Off_width * buttonScale, self.exit_Off_height * buttonScale)
