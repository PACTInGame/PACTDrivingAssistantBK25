import sys

import pygame

from Button import Button
from LfsConnection import LFSConnection
from threading import Thread


class PACTDrivingAssistant2:

    def __init__(self):
        print("starting")
        pygame.init()  # initialize pygame
        pygame.mixer.init()
        pygame.display.set_caption('Pact Driving Assistant 2')

        self.width, self.height = 800, 600
        self.btn_width, self.btn_height = 130, 50
        self.btn_width_opt = 230
        # make screen resizable
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        # self.screen = pygame.display.set_mode((self.width, self.height))
        self.running = True
        self.icon = pygame.image.load('data\\images\\icon.png')
        pygame.display.set_icon(self.icon)
        self.clock = pygame.time.Clock()
        self.colors = {
            "WHITE": (255, 255, 255),
            "RED": (255, 204, 204),
            "BLUE": (180, 210, 228),
            "GREEN": (204, 255, 204),
            "ORANGE": (255, 204, 153),
            "DARK_ORANGE": (220, 160, 120),
            "GREY": (60, 60, 60),
            "PURPLE": (41, 14, 63),
            "PINK": (212, 92, 114),
        }
        # Settings
        self.collision_warning_distance = 0

        # Backgrounds
        self.background_start = pygame.image.load('data\\images\\background_3.png')
        self.background_settings = pygame.image.load('data\\images\\background.png')
        self.background_cross = pygame.image.load('data\\images\\background_2.png')
        self.collision_1 = pygame.image.load('data\\images\\col_1.png')
        self.collision_2 = pygame.image.load('data\\images\\col_2.png')
        self.collision_3 = pygame.image.load('data\\images\\col_3.png')
        self.animation1 = [pygame.image.load('data\\images\\Anim2\\Start' + str(x) + '.png') for x in range(0, 32)]
        self.animation2 = [pygame.image.load('data\\images\\Anim1\\cross' + str(x) + '.png') for x in range(0, 10)]
        self.animation_counter = 0
        self.animation_num = 0

        self.image_position = (-960 + self.width / 2, -540 + self.height / 2)
        self.mode = 0

        # Buttons
        self.start_button = Button(self.colors['GREEN'], self.width / 2, self.height / 2, self.btn_width,
                                   self.btn_height, 'Settings')
        self.close_button = Button(self.colors['RED'], self.width / 2, self.height / 2 + self.btn_height + 15,
                                   self.btn_width, self.btn_height, 'Quit')
        self.fwd_col_button = Button(self.colors['BLUE'], self.width / 2, self.height / 2, self.btn_width_opt,
                                     self.btn_height, 'Collision Warning')
        self.light_ass_button = Button(self.colors['BLUE'], self.width / 2,
                                       self.height / 2 + self.btn_height + 15,
                                       self.btn_width_opt, self.btn_height, 'Light Assist')

        self.buttons = [self.start_button, self.close_button, self.fwd_col_button, self.light_ass_button]

        # Last: LFSConnection
        self.lfs_connection = LFSConnection()

    def reset_anim(self):
        self.animation_counter = 0
        self.animation_num = 0

    def animation(self):
        if self.animation_num == 1:  # 0 = off, 1 = to settings, 2 = forward col
            self.screen.blit(self.animation1[self.animation_counter], self.image_position)
        elif self.animation_num == 2:
            if self.collision_warning_distance == 0:
                self.screen.blit(self.collision_1, self.image_position)
            elif self.collision_warning_distance == 1:
                self.screen.blit(self.collision_2, self.image_position)
            elif self.collision_warning_distance == 2:
                self.screen.blit(self.collision_3, self.image_position)
        self.animation_counter += 1

        if self.animation_counter > 31 and 1 <= self.animation_num <= 2:
            self.reset_anim()

    def reinit_buttons(self):
        self.start_button = Button(self.colors['GREEN'], self.width / 2, self.height / 2, self.btn_width,
                                   self.btn_height, 'Settings')
        self.close_button = Button(self.colors['RED'], self.width / 2, self.height / 2 + self.btn_height + 15,
                                   self.btn_width, self.btn_height, 'Quit')
        self.fwd_col_button = Button(self.colors['BLUE'], self.width / 2, self.height / 2, self.btn_width_opt,
                                     self.btn_height, 'Collision Warning')
        self.light_ass_button = Button(self.colors['BLUE'], self.width / 2,
                                       self.height / 2 + self.btn_height + 15,
                                       self.btn_width_opt, self.btn_height, 'Light Assist')

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.quit_game()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button.is_over(event.pos):
                    if self.mode == 0:
                        if button.text == 'Settings':
                            self.mode = 1
                            self.animation_num = 1
                            break
                        elif button.text == 'Quit':
                            self.quit_game()
                            break
                    elif self.mode == 1:
                        if button.text == 'Collision Warning':
                            self.animation_num = 2
                            self.animation_counter = 0
                            self.collision_warning_distance = self.collision_warning_distance + 1 if self.collision_warning_distance < 2 else 0
                            break
        elif event.type == pygame.KEYDOWN:
            pass

        elif event.type == pygame.VIDEORESIZE:
            if event.w < 800 or event.h < 600:
                self.width, self.height = 800, 600
                self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
            elif event.w > 1920 or event.h > 1080:
                self.width, self.height = 1920, 1080
                self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
            else:
                self.width, self.height = event.w, event.h
                self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
            self.image_position = (-960 + self.width / 2, -540 + self.height / 2)
            self.reinit_buttons()

    def draw_background(self):
        if self.mode == 0:
            self.screen.blit(self.background_start, self.image_position)
        elif self.mode == 1:
            self.screen.blit(self.background_settings, self.image_position)
        elif self.mode == 2:
            self.screen.blit(self.background_cross, self.image_position)

    def draw_buttons(self):
        if self.mode == 0:
            self.start_button.draw(self.screen)
            self.close_button.draw(self.screen)
        elif self.mode == 1:
            self.fwd_col_button.draw(self.screen)
            self.light_ass_button.draw(self.screen)
        elif self.mode == 2:
            pass

    def quit_game(self):
        self.running = False
        self.lfs_connection.running = False
        pygame.quit()
        sys.exit()

    def run(self):

        thread2 = Thread(target=self.lfs_connection.run)
        thread2.start()
        while self.running:
            self.screen.fill(self.colors['GREY'])
            self.clock.tick(30)
            self.draw_background()
            if self.animation_num != 0:
                self.animation()

            self.draw_buttons()
            for event in pygame.event.get():
                self.handle_event(event)
            pygame.display.update()


if __name__ == "__main__":
    pda = PACTDrivingAssistant2()
    pda.run()
