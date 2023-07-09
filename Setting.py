import time

import Menu


class Setting:
    def __init__(self, game_obj):
        self.game_obj = game_obj
        self.head_up_display = True
        self.forward_collision_warning = True
        self.blind_spot_warning = True
        self.cross_traffic_warning = True
        self.light_assist = True
        self.park_distance_control = True
        self.emergency_assist = True
        self.lane_assist = True
        self.cop_aid_system = True
        self.automatic_emergency_braking = True
        self.collision_warning_distance = 0
        self.automatic_gearbox = False
        self.lane_dep_intensity = 0
        self.image_hud = True
        self.PSC = True

        self.bus_simulation = True
        self.bus_door_sound = True
        self.bus_route_sound = True
        self.bus_announce_sound = True
        self.bus_sound_effects = True
        self.bus_offline_sim = False

        self.resolution = 1920, 1080
        self.collision_warning_sound = 1
        self.bc = 0
        self.unit = 0
        self.offset_h = 0
        self.offset_w = 0
        self.language = 'de'

    def change_language(self):
        languages = ['en', 'de', 'fr', 'es', 'it', 'tr']
        for i in range(len(languages)):
            print(i)
            if i == len(languages) - 1:
                self.language = languages[0]
                Menu.open_menu(self.game_obj)
                break
            if languages[i] == self.language:
                self.language = languages[i + 1]
                Menu.open_menu(self.game_obj)
                break

    def activate_bus_offline(self):
        self.bus_offline_sim = True
        self.game_obj.bus_hq.sim_started = time.time()
        Menu.open_bus_menu(self.game_obj)

