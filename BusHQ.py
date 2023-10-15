import random
import time

import Sounds


class BusHQ:
    def __init__(self, game_obj):
        self.game_obj = game_obj
        self.route_active = False
        self.sim_started = 0
        self.last_radio = 0

    def start_sim(self):
        self.sim_started = time.time()

    def check_bus_radio(self):
        time_now = time.time()
        print(time_now - self.sim_started)
        print(self.route_active)
        print(time_now-self.last_radio)
        if time_now - self.sim_started > 7 and not self.route_active and time_now - self.last_radio > 30 and self.game_obj.settings.bus_offline_sim:
            self.last_radio = time.time()
            Sounds.new_route()
            if b"BL" in self.game_obj.track:
                print("BL")
                self.game_obj.bus_simulation.new_route_offer = random.randint(1, 1)
        if not self.route_active and self.game_obj.bus_simulation.route is not None:
            self.start_sim()
        self.route_active = self.game_obj.bus_simulation.route is not None

