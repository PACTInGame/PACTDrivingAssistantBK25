import time

import pygame


class ControllerInput:
    def __init__(self, game_obj):
        self.game_obj = game_obj
        self.accelerator = 0
        self.brake = 0
        self.steer = 0
        pygame.init()
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

    def check_controller_input(self):
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                if event.joy == self.game_obj.settings.num_joystick:
                    if event.axis == self.game_obj.settings.controller_throttle:
                        throttle = event.value
                        self.accelerator = (throttle - 1) / -2
                    elif event.axis == self.game_obj.settings.controller_brake:
                        brake = event.value
                        self.brake = (brake - 1) / -2
                    elif event.axis == self.game_obj.settings.controller_steer:
                        steer = event.value
                        self.steer = steer
