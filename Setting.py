import time

import Menu
import PersistentSettings
import get_settings


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

        set_def = get_settings.get_settings_from_file()
        self.persistentSettings = PersistentSettings.PersistentSettings(set_def[0], set_def[1], set_def[2], set_def[3], set_def[4],
                                                         set_def[5], set_def[6], set_def[7], set_def[8], set_def[9],
                                                         set_def[10], set_def[11], set_def[12], set_def[13],
                                                         set_def[14], set_def[15], set_def[16], set_def[17],
                                                         set_def[18], set_def[19], set_def[20])
        cont_def = get_settings.get_controls_from_file()
        self.SHIFT_UP_KEY = cont_def[0]
        self.SHIFT_DOWN_KEY = cont_def[1]
        self.IGNITION_KEY = cont_def[2]
        self.THROTTLE_AXIS = int(cont_def[3])
        self.BRAKE_AXIS = int(cont_def[4])
        self.STEER_AXIS = int(cont_def[5])
        self.VJOY_AXIS = int(cont_def[6])
        self.VJOY_AXIS1 = int(self.VJOY_AXIS) + 1
        self.VJOY_AXIS2 = int(self.VJOY_AXIS) + 2
        self.BRAKE_KEY = cont_def[7]
        self.ACC_KEY = cont_def[8]
        self.HANDBRAKE_KEY = cont_def[9]
        self.controller_throttle, self.controller_brake, self.num_joystick = get_settings.get_acc_settings_from_file()

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
        self.bus_offline_sim = not self.bus_offline_sim
        self.game_obj.bus_hq.sim_started = time.time()
        Menu.open_bus_menu(self.game_obj)
        if not self.bus_offline_sim:
            self.game_obj.bus_hq.sim_started = 0
            self.game_obj.bus_hq.route_active = False
            self.game_obj.bus_simulation.new_route_offer = 0
            self.game_obj.bus_simulation.active = False
