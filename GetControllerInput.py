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

    def check_controller_input(self):
        joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        counter = time.perf_counter()

        while self.game_obj.on_track:
            if time.perf_counter() - counter > 0.1:
                counter = time.perf_counter()

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


