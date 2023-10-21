# Class to represent cars gearbox
import threading
import time

import pydirectinput


class Gearbox:
    def __init__(self, game_object):
        self.game_object = game_object
        self.gear = 0
        self.max_gears = 7
        self.mode = 0  # 0 = normal, 1 = sport, 2 = economy
        self.accelerator_pedal_position = 0
        self.brake_pedal_position = 0
        self.cornering = 0
        self.rpm = 0
        self.redline = 8000
        self.idle = 1000
        self.last_executed = 0
        self.full_throttle = 0

    def update_data(self):
        self.accelerator_pedal_position = self.game_object.own_vehicle.throttle
        if self.accelerator_pedal_position > 0.9:
            self.full_throttle = time.perf_counter()
        self.brake_pedal_position = self.game_object.own_vehicle.brake
        self.cornering = self.game_object.own_vehicle.steer_forces
        self.rpm = self.game_object.own_vehicle.rpm
        self.gear = self.game_object.own_vehicle.gear

    def send(self, keys):
        if time.perf_counter() - self.last_executed >= 1:
            self.last_executed = time.perf_counter()

            for key in keys:
                print("key: " + str(key))
                pydirectinput.press(key)

    def calculate_gear(self):
        self.update_data()
        shift_action = 0
        if self.mode == 0:
            corridor = (self.redline - self.idle) / 4
            if self.rpm > self.redline - 200:
                shift_action = 1
            elif self.rpm < self.idle + 1000:
                shift_action = -1
            elif self.redline * self.accelerator_pedal_position < self.rpm - corridor and not (
                    self.accelerator_pedal_position < 0.1 and self.rpm < self.redline - 2000) and not (
                self.full_throttle > time.perf_counter() - 1) and not (self.brake_pedal_position > 0):

                shift_action = 1
            elif self.redline * self.accelerator_pedal_position > self.rpm + corridor:
                shift_action = -1
            elif self.brake_pedal_position > 0.5 and self.rpm < self.redline - 1500:
                shift_action = -1
            elif self.brake_pedal_position > 0.2 and self.rpm < self.redline - 2500:
                shift_action = -1
        elif self.mode == 1:
            pass

        elif self.mode == 2:
            pass
        if self.gear == self.max_gears and shift_action == 1:
            shift_action = 0
        elif self.gear <= 2 and shift_action == -1:
            shift_action = 0
        if self.accelerator_pedal_position > 0.9 and not self.rpm > self.redline - 200 and shift_action == 1:
            shift_action = 0
        ign = self.game_object.settings.IGNITION_KEY
        up = self.game_object.settings.SHIFT_UP_KEY
        down = self.game_object.settings.SHIFT_DOWN_KEY

        if shift_action == 1:
            self.send([ign, up, ign])

        elif shift_action == -1:
            self.send([ign, down, ign])
