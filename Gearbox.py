# Class to represent cars gearbox
from threading import Thread
import time

import pydirectinput


class Gearbox:
    def __init__(self, game_object):
        self.game_object = game_object
        self.gear = 2
        self.speed = 0
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
        self.speed = self.game_object.own_vehicle.speed

    def send(self, keys):
        if time.perf_counter() - self.last_executed >= 1:
            self.last_executed = time.perf_counter()
            t = Thread(target=self.press, args=(keys,))
            t.start()

    def press(self, keys):
        for key in keys:
            pydirectinput.press(key)

    def calculate_gear(self):
        # TODO this should work for all cars and be stored in files or smth
        # TODO And add support for different setups per car
        self.update_data()
        gears_and_max_speed = {
            0: 0,
            1: 65,
            2: 105,
            3: 141,
            4: 190,
            5: 246,
            6: 275,
        }
        '''
        FZ5
        gears_and_max_speed = {
            0: 0,
            1: 86,
            2: 123,
            3: 154,
            4: 189,
            5: 223,
            6: 257,
        }
        '''
        # As list comprehension
        percentage_gears = [self.speed / gears_and_max_speed[i] * 100 for i in range(1, len(gears_and_max_speed))]

        wanted_percentage = self.accelerator_pedal_position * 100 + 10
        if wanted_percentage > 100:
            wanted_percentage = 100
        if self.brake_pedal_position > 0.1:
            wanted_percentage = self.brake_pedal_position * 100 - 10

            if wanted_percentage < 50:
                wanted_percentage = 50
        filtered_percentages = [p for p in percentage_gears if p <= 95.0]

        # Find the value closest to 'percent' in the filtered listxi
        closest = min(filtered_percentages, key=lambda x: abs(x - wanted_percentage))
        find_index = percentage_gears.index(closest) + 2
        if self.gear < find_index and self.accelerator_pedal_position > 0 and not self.brake_pedal_position > 0:
            shift_action = 1
        elif self.gear > find_index:
            shift_action = -1
        else:
            shift_action = 0
        '''
        current_max_speed = gears_and_max_speed[self.gear - 1]
        max_corridor = gears_and_max_speed[1]
        low_speed = gears_and_max_speed[self.gear - 1] - (1-self.accelerator_pedal_position) * max_corridor
        high_speed = gears_and_max_speed[self.gear - 1] - (1-self.accelerator_pedal_position) * (max_corridor / 2)
        print("low speed: " + str(low_speed))
        print("high speed: " + str(high_speed))
        if self.speed > current_max_speed - 7:
            shift_action = 1
'''
        '''
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
        '''
        ign = self.game_object.settings.IGNITION_KEY
        up = self.game_object.settings.SHIFT_UP_KEY
        down = self.game_object.settings.SHIFT_DOWN_KEY

        if not self.game_object.text_entry:
            if shift_action == 1:

                self.send([ign, up, ign])

            elif shift_action == -1:
                self.send([ign, down, ign])
