# Class to represent cars gearbox
from threading import Thread
import time

import pydirectinput
import keyboard as kb
import pyinsim


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
        self.car_supported = False
        self.make_selection = False
        self.gears_and_max_speed = {}
        self.filtered_percentages = []

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
        if time.perf_counter() - self.last_executed >= 2:
            self.last_executed = time.perf_counter()
            t = Thread(target=self.press, args=(keys,))
            t.start()

    def press(self, keys):
        shift = get_shift_buttons()
        if not shift:
            for key in keys:
                pydirectinput.press(key)

    def get_gearbox_data_from_file(self, cname):
        cname = str(cname)
        cname = cname[2:-1]
        print(cname)
        text_file = open("data/gearbox.txt", "r").read()
        # Parse the text file and store the data in a dictionary of dictionaries
        data_dict = {}
        current_key = ""
        for line in text_file.split("\n"):
            if "_" in line:  # This is a new key
                current_key = line.strip()
                data_dict[current_key] = []
            elif ":" in line and current_key:  # These are values under the current key
                value = line.strip()
                data_dict[current_key].append(value)

        # Filter the results based on the input string
        results = []
        for key, values in data_dict.items():
            if cname in key:
                # Extracting the prefix from the key
                prefix = key.rsplit("_")[0]
                postfix = key.rsplit("_")[1]
                postfix = postfix.split(":")[0]
                formatted_values = {int(v.split(":")[0]): int(v.split(":")[1]) for v in values}
                results.append([prefix, formatted_values, postfix])

        return results

    def get_gears_and_max_speed(self):
        gears_and_max_speed_list = self.get_gearbox_data_from_file(self.game_object.own_vehicle.cname)
        if len(gears_and_max_speed_list) > 0:
            self.car_supported = True
            if len(gears_and_max_speed_list) > 1:
                # TODO be able to select
                self.gears_and_max_speed = gears_and_max_speed_list
                self.make_selection = True
            else:
                self.make_selection = False
                self.gears_and_max_speed = gears_and_max_speed_list[0][1]
        else:
            self.car_supported = False

    def gearbox_select(self, number):
        self.gears_and_max_speed = self.gears_and_max_speed[number][1]
        self.make_selection = False
        for i in range(11):
            self.game_object.del_button(120 + i)

    def calculate_gear(self):
        # TODO only 10 settings per car saveable
        self.update_data()
        if self.make_selection:
            self.game_object.send_button(120, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 50, 87, 26, 5,
                                         "Select gearbox settings")
            for i in range(len(self.gears_and_max_speed)):
                if i > 10:  # TODO check if this is right
                    break
                self.game_object.send_button(121 + i, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 55 + 5 * i, 87, 26, 5,
                                             self.gears_and_max_speed[i][2])

        if self.car_supported and not self.make_selection:
            # As list comprehension
            percentage_gears = [self.speed / self.gears_and_max_speed[i] * 100 for i in
                                range(1, len(self.gears_and_max_speed) + 1)]
            wanted_percentage = self.accelerator_pedal_position * 100 + 10
            if wanted_percentage > 100:
                wanted_percentage = 100
            if self.brake_pedal_position > 0.1:
                wanted_percentage = self.brake_pedal_position * 100 - 10

                if wanted_percentage < 50:
                    wanted_percentage = 50
            fp = [p for p in percentage_gears if p <= 95.0]
            if len(self.filtered_percentages) < len(fp):
                fp = [p for p in percentage_gears if p <= 87.0]
            self.filtered_percentages = fp
            # Find the value closest to 'percent' in the filtered list
            if len(self.filtered_percentages) == 0:
                closest = percentage_gears[-1]
            else:
                closest = min(self.filtered_percentages, key=lambda x: abs(x - wanted_percentage))
            find_index = percentage_gears.index(closest) + 2
            if self.gear < find_index and self.accelerator_pedal_position > 0 and not self.brake_pedal_position > 0:
                shift_action = find_index - self.gear
            elif self.gear > find_index:
                shift_action = find_index - self.gear
            else:
                shift_action = 0
            if self.cornering > 500 or self.cornering < -500 or self.gear <= 1:
                shift_action = 0

            ign = self.game_object.settings.IGNITION_KEY
            up = self.game_object.settings.SHIFT_UP_KEY
            down = self.game_object.settings.SHIFT_DOWN_KEY

            if not self.game_object.text_entry:
                if shift_action >= 1:
                    self.send([ign, up, ign])

                elif shift_action == -1:
                    self.send([ign, down, ign])

                elif shift_action == -2:
                    self.send([ign, down, down, ign])

                elif shift_action <= -3:
                    self.send([ign, down, down, down, ign])


def get_shift_buttons():
    try:
        return kb.is_pressed("shift")
    except:
        return "Error detecting Keyboard inputs"
