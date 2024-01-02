import time

import Calculations


class RaceAssist:
    def __init__(self, game_object):
        self.game_object = game_object

        self.laps_on_fuel = 0
        self.fuel_at_start_of_lap = 0

        self.laps_race = 0
        self.laps_left = 0
        self.laps_driven = 0
        self.total_time_in_race = [0, time.perf_counter()]

        self.pit_this_lap = False
        self.live_delta_next_car = 0
        self.live_delta_previous_car = 0
        self.live_delta_previous_lap = 0
        self.predicted_fuel_needed = 0

        self.tire_temp_high = [False, False, False, False]  # TODO: Sollte iwie über OutSim zu bekommen sein
        self.coordinates_and_timestamps_last_lap = []
        self.coordinates_and_timestamps_best_lap = []
        self.coordinates_and_timestamps_this_lap = []
        self.lap_times = []
        self.start_time_this_lap = 0
        self.radio = False

        self.best_first_split = 5940000  # = 99 min
        self.best_second_split = 5940000
        self.best_third_split = 5940000

    def update_lap_time(self, lap_time):
        self.lap_times.append(lap_time)
        print("update_laptime")
        self.coordinates_and_timestamps_last_lap = self.coordinates_and_timestamps_this_lap
        self.coordinates_and_timestamps_this_lap = []
        if min(self.lap_times) == lap_time:
            self.coordinates_and_timestamps_best_lap = self.coordinates_and_timestamps_last_lap

    def update_total_time(self, total_time):
        self.total_time_in_race = [total_time, time.perf_counter()]

    def update_split_times(self, split, split_time):
        if split == 1:
            if split_time < self.best_first_split:
                self.best_first_split = split_time
        elif split == 2:
            if split_time < self.best_second_split:
                self.best_second_split = split_time
        elif split == 3:
            if split_time < self.best_third_split:
                self.best_third_split = split_time

    def update_laps_done(self, laps):
        self.start_time_this_lap = time.perf_counter()
        self.laps_driven = laps

    def update_coordinates_and_timestamp(self):
        time_lap_split = time.perf_counter() - self.start_time_this_lap
        veh = self.game_object.own_vehicle
        self.coordinates_and_timestamps_this_lap.append([veh.x, veh.y, time_lap_split])

    def check_live_delta_previous_lap(self):
        min_dist = 131072000  # 2km
        time_next_point = 5940000
        if len(self.coordinates_and_timestamps_last_lap) > 0:
            veh = self.game_object.own_vehicle
            time_now = time.perf_counter() - self.start_time_this_lap
            for coordinates in self.coordinates_and_timestamps_last_lap:
                x, y, timestamp = coordinates
                dist = Calculations.calc_distance(veh.x, veh.y, x, y)
                if dist < min_dist:
                    min_dist = dist
                    time_next_point = timestamp
            print((time_now - time_next_point))
