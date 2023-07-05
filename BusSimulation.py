import random
import time

import Sounds
import pyinsim


def get_routes_westhill():
    routes = {
        1: [
            {"name": "south_station", "next_stop": "weston_zoo", "coordinates": (733.44, -748.50)},
            {"name": "weston_zoo", "next_stop": "dustin", "coordinates": (333.44, -235.13)},
            {"name": "dustin", "next_stop": "paddock", "coordinates": (73.81, 205.25)},
            {"name": "paddock", "next_stop": "gas_station", "coordinates": (-124.44, 239.94)},
            {"name": "gas_station", "next_stop": "roundabout", "coordinates": (-134.00, 571.25)},
            {"name": "roundabout", "next_stop": "vip_tribune", "coordinates": (-306.63, 766.56)},
            {"name": "vip_tribune", "next_stop": "west_grill", "coordinates": (-298.75, 355.88)},
            {"name": "west_grill", "next_stop": "traffic_police", "coordinates": (-423.56, -78.88)},
            {"name": "traffic_police", "next_stop": "main_station", "coordinates": (-707.88, -184.56)}
        ],
        2: [
            {"name": "south_station", "next_stop": "weston_observatory", "coordinates": (733.44, -748.50)},
            {"name": "weston_observatory", "next_stop": "infield", "coordinates": (175.88, -545.50)},
            {"name": "infield", "next_stop": "speedway", "coordinates": (-239.25, -409.75)},
            {"name": "speedway", "next_stop": "green_mountain", "coordinates": (-342.69, -670.94)},
            {"name": "green_mountain", "next_stop": "vipers_valley", "coordinates": (84.44, -709.56)},
            {"name": "vipers_valley", "next_stop": "southampton_road", "coordinates": (247.19, -992.06)},
            {"name": "southampton_road", "next_stop": "south_station", "coordinates": (634.88, -1133.19)}
        ],
        # Add more routes here...
    }
    return routes


def get_routes_blackwood():
    routes = {
        1: [
            {"name": "main_station", "next_stop": "forest_hill", "coordinates": (-219.19, 215.00), "time": 0.5,
             "dn": "Main Station"},
            {"name": "forest_hill", "next_stop": "velocity_ave", "coordinates": (-347.81, 344.75), "time": 1.5,
             "dn": "Forest Hill"},
            {"name": "velocity_ave", "next_stop": "blackwood_heights", "coordinates": (-544.94, 401.56), "time": 2.5,
             "dn": "Velocity Ave."},
            {"name": "blackwood_heights", "next_stop": "narrow_passage", "coordinates": (-892.94, 401.38), "time": 3.5,
             "dn": "Blackwood Heights"},
            {"name": "narrow_passage", "next_stop": "forest", "coordinates": (-823.31, 729.75), "time": 4.5,
             "dn": "Narrow Passage"},
            {"name": "forest", "next_stop": "forest_hill", "coordinates": (-302.94, 698.06), "time": 5.5,
             "dn": "Forest"},
            {"name": "forest_hill", "next_stop": "main_station_a", "coordinates": (-310.38, 344.13), "time": 6.5,
             "dn": "Forest Hill"},
            {"name": "main_station_a", "next_stop": "none", "coordinates": (-219.19, 215.00), "time": 7.5,
             "dn": "Main Station"}
        ],
        2: [
            {"name": "main_station", "next_stop": "ellecsix_boulevard", "coordinates": (-211.63, 231.00)},
            {"name": "ellecsix_boulevard", "next_stop": "industry_lane", "coordinates": (-384.56, 169.38)},
            {"name": "industry_lane", "next_stop": "lyon_road", "coordinates": (-698.63, 204.00)},
            {"name": "lyon_road", "next_stop": "bourne_road", "coordinates": (-750.56, 430.19)},
            {"name": "bourne_road", "next_stop": "manor_way", "coordinates": (-594.19, 715.75)},
            {"name": "manor_way", "next_stop": "forest_hill", "coordinates": (-378.81, 534.06)},
            {"name": "forest_hill", "next_stop": "main_station_b", "coordinates": (-310.38, 344.13)}
        ],
        # Add more routes here...
    }
    return routes


class BusSimulation:
    def __init__(self, game_obj):
        self.active = False
        self.route_index = 0
        self.route = None
        self.current_stop = ""
        self.next_stop = ""
        self.passengers = 0
        self.passengers_max = 0
        self.doors_open = False
        self.online = False
        self.start_time = 0
        self.next_stop_countdown = 0
        self.stop_index = 0
        self.at_stop = False
        self.stationary_at_stop = False
        self.passengers_added_at_stop = 0

        self.next_stop_sound_played = False
        self.game_obj = game_obj

    def start_route(self, route):
        self.active = True
        self.route = get_routes_blackwood()[route]
        self.stop_index = 0
        self.current_stop = self.route[0]["name"]
        self.next_stop = self.route[0]["next_stop"]
        self.passengers = 0
        self.passengers_max = 50
        self.doors_open = False
        self.next_stop_sound_played = False
        self.start_time = time.time()

    def check_bus_simulation(self):
        x = self.game_obj.own_vehicle.x / 65536
        y = self.game_obj.own_vehicle.y / 65536
        speed = self.game_obj.own_vehicle.speed

        # Check_Timetable
        self.next_stop_countdown = (time.time() - self.start_time) - self.route[self.stop_index]["time"] * 60
        print(self.next_stop_countdown)

        # Check at stop
        self.at_stop = x - 5 <= self.route[self.stop_index]["coordinates"][0] <= x + 5 and y - 5 <= \
                       self.route[self.stop_index]["coordinates"][1] <= y + 5

        # Check stationary at stop
        self.stationary_at_stop = self.at_stop and speed < 0.1

        # update if stationary at stop
        if self.stationary_at_stop:
            self.stop_index = self.stop_index + 1
            self.current_stop = self.route[self.stop_index]["name"]
            self.next_stop = self.route[self.stop_index]["next_stop"]

            if self.doors_open:
                # Check if its last stop on route
                if self.stop_index == len(self.route) - 1:
                    self.passengers = self.passengers - 1 if self.passengers > 0 else 0
                    self.active = False if self.passengers == 0 else True
                elif self.passengers_added_at_stop < random.randint(1, 10):
                    # Randomly add or decrease passengers
                    self.passengers = self.passengers + random.randint(-1, 1)
                    self.passengers_added_at_stop += 1
                    if self.passengers < 0:
                        self.passengers = 0
                    if self.passengers > self.passengers_max:
                        self.passengers = self.passengers_max

        # update buttons
        self.update_buttons()

    def update_buttons(self):
        if not self.online and self.active:
            route_string = f'Destination: {self.route[-1]["dn"]}'
            next_stop_string = f'Next Stop: {self.route[self.stop_index]["dn"]}'
            time_string = f'^1Time: {self.next_stop_countdown:.0f}' if self.next_stop_countdown > 0 else f'^2Time: {self.next_stop_countdown:.0f}'
            passengers_string = f'Passengers: {self.passengers}/{self.passengers_max}'

            self.game_obj.send_button(11, pyinsim.ISB_DARK, 100, 175, 20, 5, route_string)
            self.game_obj.send_button(12, pyinsim.ISB_DARK, 105, 175, 20, 5, next_stop_string)
            self.game_obj.send_button(13, pyinsim.ISB_DARK, 110, 175, 20, 5, time_string)
            self.game_obj.send_button(14, pyinsim.ISB_DARK, 115, 175, 20, 5, passengers_string)
            if self.stationary_at_stop and not self.doors_open:
                self.game_obj.send_button(15, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 120, 175, 20, 5, "Open Doors")
            else:
                self.game_obj.send_button(15, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 120, 175, 20, 5, "Close Doors")
        else:
            self.game_obj.del_button(11)
            self.game_obj.del_button(12)
            self.game_obj.del_button(13)
            self.game_obj.del_button(14)

    def open_bus_doors(self):
        self.doors_open = True if not self.doors_open else False
        if self.doors_open:
            Sounds.(self.settings.collision_warning_sound)
