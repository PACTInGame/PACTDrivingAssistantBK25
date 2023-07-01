import random
import sys
import time

import pygame

from Button import Button
from LfsConnection import LFSConnection
from threading import Thread


class PACTDrivingAssistant2:

    def __init__(self):
        pygame.init()  # initialize pygame
        pygame.mixer.init()
        pygame.display.set_caption('Pact Driving Assistant 2')

        self.width, self.height = 800, 600
        self.btn_width, self.btn_height = 100, 30
        self.btn_width_opt = 200
        # make screen resizable
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        # self.screen = pygame.display.set_mode((self.width, self.height))
        self.image_position = (-960 + self.width / 2, -540 + self.height / 2)

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
        # startup animation
        self.startup_animation = [pygame.image.load('data\\images\\Starting\\Start0' + str(x) + '.png') for x in
                                  range(1, 6)]
        for i in range(0, 5):
            self.screen.blit(self.startup_animation[i], self.image_position)
            time.sleep(random.uniform(0.1, 0.3))
            pygame.display.update()

        # Settings
        self.collision_warning_distance = 0
        self.light_assist = 0
        self.head_up_display = 0
        self.cross_warning_distance = 0
        self.lane_departure_warning = 0
        self.real_clutch = 0


        # Backgrounds
        self.background_start = pygame.image.load('data\\images\\background_start.png')
        self.background_settings = pygame.image.load('data\\images\\background.png')
        self.background_bus = pygame.image.load('data\\images\\background_bus.png')
        self.background_pdc = pygame.image.load('data\\images\\background_pdc.png')
        self.collision_0 = pygame.image.load('data\\images\\col_0.png')
        self.collision_1 = pygame.image.load('data\\images\\col_1.png')
        self.collision_2 = pygame.image.load('data\\images\\col_2.png')
        self.collision_3 = pygame.image.load('data\\images\\col_3.png')
        self.cross_0 = pygame.image.load('data\\images\\cross_0.png')
        self.cross_1 = pygame.image.load('data\\images\\cross_1.png')
        self.cross_2 = pygame.image.load('data\\images\\cross_2.png')
        self.cross_3 = pygame.image.load('data\\images\\cross_3.png')
        self.head_up_on = pygame.image.load('data\\images\\hud_1.png')
        self.head_up_off = pygame.image.load('data\\images\\hud_0.png')
        self.animation1 = [pygame.image.load('data\\images\\Anim1\\settings' + str(x) + '.png') for x in range(0, 26)]
        self.animation2 = [pygame.image.load('data\\images\\Anim2\\bus' + str(x) + '.png') for x in range(0, 26)]
        self.animation3 = [pygame.image.load('data\\images\\Anim3\\pdc' + str(x) + '.png') for x in range(0, 30)]
        self.animation_counter = 0
        self.animation_num = 0

        self.mode = 0

        # Buttons
        self.start_button = None
        self.close_button = None
        self.fwd_col_button = None
        self.light_ass_button = None
        self.hud_button = None
        self.clutch_button = None
        self.pdc_button = None
        self.lane_departure_button = None
        self.cross_traffic_button = None
        self.bus_button = None
        self.back_button = None
        self.reinit_buttons()
        self.buttons = [self.start_button, self.close_button, self.fwd_col_button, self.light_ass_button,
                        self.hud_button, self.clutch_button, self.pdc_button, self.lane_departure_button,
                        self.cross_traffic_button, self.bus_button, self.back_button]

        # Last: LFSConnection
        self.lfs_connection = LFSConnection()
        self.font = pygame.font.SysFont('Arial', 30)
        self.connection_text = self.font.render("Connection to LFS", True, self.colors["WHITE"])

    def reset_anim(self):
        self.animation_counter = 0
        self.animation_num = 0

    def animation(self):
        # 0 = off, 1 = to settings, 2 = forward col, 3 = to bus, 4 = to pdc, 6 = from bus, 7 = from pdc
        if self.animation_num == 1:
            self.screen.blit(self.animation1[self.animation_counter], self.image_position)

        elif self.animation_num == 2:
            if self.collision_warning_distance == 0:
                self.screen.blit(self.collision_0, self.image_position)
            elif self.collision_warning_distance == 1:
                self.screen.blit(self.collision_1, self.image_position)
            elif self.collision_warning_distance == 2:
                self.screen.blit(self.collision_2, self.image_position)
            elif self.collision_warning_distance == 3:
                self.screen.blit(self.collision_3, self.image_position)
        elif self.animation_num == 3:
            self.screen.blit(self.animation2[self.animation_counter], self.image_position)

        elif self.animation_num == 4:
            self.screen.blit(self.animation3[self.animation_counter], self.image_position)
        elif self.animation_num == 5:
            self.screen.blit(self.animation1[self.animation_counter], self.image_position)
        elif self.animation_num == 6:
            self.screen.blit(self.animation2[self.animation_counter], self.image_position)
        elif self.animation_num == 7:
            self.screen.blit(self.animation3[self.animation_counter], self.image_position)

        elif self.animation_num == -1:
            if self.head_up_display == 1:
                self.screen.blit(self.head_up_on, self.image_position)

            elif self.head_up_display == 0:
                self.screen.blit(self.head_up_off, self.image_position)

        elif self.animation_num == -2:

            if self.cross_warning_distance == 0:
                self.screen.blit(self.cross_0, self.image_position)
            elif self.cross_warning_distance == 1:
                self.screen.blit(self.cross_1, self.image_position)
            elif self.cross_warning_distance == 2:
                self.screen.blit(self.cross_2, self.image_position)
            elif self.cross_warning_distance == 3:
                self.screen.blit(self.cross_3, self.image_position)

        if self.animation_num > 4:
            self.animation_counter -= 1
        else:
            self.animation_counter += 1

        if self.animation_counter > 25 and -2 <= self.animation_num <= 3:
            self.reset_anim()
        elif self.animation_counter > 29 and self.animation_num == 4:
            self.reset_anim()
        elif self.animation_counter == 0 and 5 <= self.animation_num <= 7:
            self.reset_anim()

    def reinit_buttons(self):
        x_opt = self.width / 2 - 375
        y_opt = self.height / 2 - self.btn_height - 15
        gap = 10
        self.start_button = Button(self.colors['GREEN'], self.width / 2 + 200, self.height / 2, self.btn_width,
                                   self.btn_height, 'Settings')
        self.close_button = Button(self.colors['RED'], self.width / 2 + 200, self.height / 2 + self.btn_height + 15,
                                   self.btn_width, self.btn_height, 'Quit')
        self.hud_button = Button(self.colors['GREEN' if self.head_up_display else 'RED'], x_opt, y_opt, self.btn_width_opt,
                                 self.btn_height, 'Head Up Display')
        self.fwd_col_button = Button(self.colors['GREEN' if self.collision_warning_distance > 0 else 'RED'], x_opt,
                                     y_opt + self.btn_height + gap,
                                     self.btn_width_opt, self.btn_height, 'Collision Warning')
        self.cross_traffic_button = Button(self.colors['GREEN' if self.cross_warning_distance > 0 else 'RED'], x_opt,
                                           y_opt + self.btn_height * 2 + gap * 2,
                                           self.btn_width_opt, self.btn_height, 'Cross Traffic Warning')
        self.lane_departure_button = Button(self.colors['GREEN' if self.lane_departure_warning > 0 else 'RED'], x_opt,
                                            y_opt + self.btn_height * 3 + gap * 3,
                                            self.btn_width_opt, self.btn_height, 'Lane Dep. Warning')
        self.clutch_button = Button(self.colors['GREEN' if self.real_clutch == 1 else 'RED'], x_opt,
                                    y_opt + self.btn_height * 4 + gap * 4,
                                    self.btn_width_opt, self.btn_height, 'Realistic Clutch')
        self.light_ass_button = Button(self.colors['GREEN' if self.light_assist == 1 else 'RED'], x_opt,
                                       y_opt + self.btn_height * 5 + gap * 5,
                                       self.btn_width_opt, self.btn_height, 'Light Assist')
        self.bus_button = Button(self.colors['BLUE'], x_opt,
                                 y_opt + self.btn_height * 6 + gap * 6,
                                 self.btn_width_opt, self.btn_height, 'Bus Simulation ->')
        self.pdc_button = Button(self.colors['BLUE'], x_opt + self.btn_width_opt + 15,
                                 y_opt + self.btn_height * 6 + gap * 6,
                                 self.btn_width_opt, self.btn_height, 'Parking Aid ->')
        self.back_button = Button(self.colors['RED'], x_opt,
                                  y_opt + self.btn_height * 7 + gap * 7,
                                  self.btn_width_opt, self.btn_height, 'Back')

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
                            self.collision_warning_distance = self.collision_warning_distance + 1 if self.collision_warning_distance < 3 else 0
                            break

                        elif button.text == 'Head Up Display':
                            if self.head_up_display == 0:
                                self.head_up_display = 1
                                self.animation_num = -1
                                self.animation_counter = 0
                            else:
                                self.animation_num = -1
                                self.head_up_display = 0
                                self.animation_counter = 0
                            break

                        elif button.text == 'Cross Traffic Warning':
                            self.animation_num = -2
                            self.cross_warning_distance = self.cross_warning_distance + 1 if self.cross_warning_distance < 3 else 0
                            self.animation_counter = 0
                            break

                        elif button.text == 'Light Assist':
                            self.light_assist = 0 if self.light_assist else 1
                            break

                        elif button.text == 'Realistic Clutch':
                            self.real_clutch = 0 if self.real_clutch else 1
                            break

                        elif button.text == 'Bus Simulation ->':
                            self.animation_num = 3
                            self.animation_counter = 0
                            self.mode = 2
                            break

                        elif button.text == 'Parking Aid ->':
                            self.animation_num = 4
                            self.animation_counter = 0
                            self.mode = 3
                            break

                        elif button.text == 'Back':
                            self.animation_num = 5
                            self.animation_counter = 25
                            self.mode = 0
                            break

                    elif self.mode == 2:
                        if button.text == 'Back':
                            self.animation_num = 6
                            self.animation_counter = 25
                            self.mode = 1
                            break

                    elif self.mode == 3:
                        if button.text == 'Back':
                            self.animation_num = 7
                            self.animation_counter = 29
                            self.mode = 1
                            break
            self.reinit_buttons()
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
            self.screen.blit(self.background_bus, self.image_position)
        elif self.mode == 3:
            self.screen.blit(self.background_pdc, self.image_position)

    def draw_buttons(self):
        if self.mode == 0:
            self.start_button.draw(self.screen)
            self.close_button.draw(self.screen)
        elif self.mode == 1:
            self.fwd_col_button.draw(self.screen)
            self.light_ass_button.draw(self.screen)
            self.hud_button.draw(self.screen)
            self.pdc_button.draw(self.screen)
            self.clutch_button.draw(self.screen)
            self.lane_departure_button.draw(self.screen)
            self.bus_button.draw(self.screen)
            self.cross_traffic_button.draw(self.screen)
            self.back_button.draw(self.screen)
        elif self.mode == 2:
            self.back_button.draw(self.screen)
        elif self.mode == 3:
            self.back_button.draw(self.screen)

        # Draw if connected
        self.screen.blit(self.connection_text, (
            self.width - self.connection_text.get_width() - 50, self.height - self.connection_text.get_height() - 15))
        if self.lfs_connection.is_connected:
            pygame.draw.rect(self.screen, (0, 255, 0), (
                self.width - 40, self.height - self.connection_text.get_height() - 15, 30,
                self.connection_text.get_height()))
        else:
            pygame.draw.rect(self.screen, (255, 0, 0), (
                self.width - 40, self.height - self.connection_text.get_height() - 15, 30,
                self.connection_text.get_height()))

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
