import time

import Menu
import PersistentSettings
import get_settings


class Setting:
    def __init__(self, game_obj):
        self.game_obj = game_obj

        self.bus_simulation = True
        self.bus_door_sound = True
        self.bus_route_sound = True
        self.bus_announce_sound = True
        self.bus_sound_effects = True
        self.bus_offline_sim = False

        set_def = get_settings.get_settings_from_file()

        self.head_up_display = set_def[0]
        self.forward_collision_warning = set_def[1]
        self.blind_spot_warning = set_def[2]
        self.cross_traffic_warning = set_def[3]
        self.light_assist = set_def[4]
        self.park_distance_control = set_def[5]
        self.emergency_assist = set_def[6]
        self.lane_assist = set_def[7]
        self.cop_aid_system = set_def[8]
        self.automatic_emergency_braking = set_def[9]
        self.collision_warning_distance = int(set_def[10])
        self.automatic_gearbox = set_def[11]
        self.lane_dep_intensity = set_def[12]
        self.image_hud = set_def[13]
        self.PSC = set_def[14]
        self.resolution = set_def[15]
        self.collision_warning_sound = set_def[16]
        self.bc = set_def[17]
        self.unit = set_def[18]
        self.offset_h = set_def[19]
        self.offset_w = set_def[20]
        self.automatic_indicator_turnoff = set_def[21]
        self.park_emergency_brake = set_def[22]
        self.language = set_def[23]
        self.audible_parking_aid = set_def[24]
        self.visual_parking_aid = set_def[25]
        self.side_collision_prevention = set_def[26]
        self.indicator_sound = set_def[27]
        self.adaptive_brake_light = set_def[28]
        self.adaptive_brake_light_style = set_def[29]
        self.pact_mode = set_def[30]  # 0 = all on, 1 = all off, 2 = cop, 3 = race
        self.stall_protection = set_def[31]
        self.realistic_clutch = set_def[32]

        # TODO MAKE MORE SETTINGS PERSISTENT
        self.automatic_siren = True
        self.use_indicators = True
        self.use_light = True
        self.use_extra_light = True
        self.use_fog_light = True
        self.suspect_tracker = True

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
        self.SPARE_KEY_1 = cont_def[10]
        self.SPARE_KEY_2 = cont_def[11]
        self.CLUTCH_AXIS = int(cont_def[12])
        self.TGROTTLE_KEY = "mousel"
        self.controller_throttle, self.controller_brake, self.controller_steer, self.num_joystick = get_settings.get_acc_settings_from_file()

    def change_language(self):
        languages = ['en', 'de', 'fr', 'es', 'it', 'tr']
        for i in range(len(languages)):
            if i == len(languages) - 1:
                self.language = languages[0]
                Menu.open_menu(self.game_obj)
                break
            if languages[i] == self.language:
                self.language = languages[i + 1]
                Menu.open_menu(self.game_obj)
                break
        self.game_obj.lang = self.language

    def activate_bus_offline(self):
        self.bus_offline_sim = not self.bus_offline_sim
        self.game_obj.bus_hq.sim_started = time.time()
        Menu.open_bus_menu(self.game_obj)
        if not self.bus_offline_sim:
            self.game_obj.bus_hq.sim_started = 0
            self.game_obj.bus_hq.route_active = False
            self.game_obj.bus_simulation.new_route_offer = 0
            self.game_obj.bus_simulation.active = False

    def change(self, var):
        var = not var

    def save_controls(self):
        print(self.SHIFT_UP_KEY)
        file_string = ("Important: Only change inside LFS!\n"
                       "{}  <-change you Shift Up key here.      ------------------ ALL USERS\n"
                       "{}  <-change you Shift Down key here. ------------------ ALL USERS\n"
                       "{}  <-change you Ignition key here.       ------------------ ALL USERS\n"
                       "{}  <-specify your throttle axis (OPTIONS -> CONTROLS -> AXES/FF), if you have a controller\n"
                       "{}  <-specify your brake axis, if you have a controller\n"
                       "{}  <-specify your steering axis, if you have a controller\n"
                       "{} <-specify the first vjoy axis, if you have a controller\n"
                       "{}  <-specify the brake key, if you use keyboard or mouse (can also be mousel, mouser)\n"
                       "{} <-specify the accelerator key, if you use keyboard\n"
                       "{} <-specify the handbrake key           ------------------ ALL USERS\n"
                       "C:\\Program Files\\vJoy\\x64\\vJoyInterface.dll <-change Path to vJoy folder here, depends on where you've installed it.\n"
                       "{} <-a spare key without any function\n"
                       "{} <-a spare key without any function\n"
                       "{} <- specify your clutch axis, if you have a controller)\n".format(str(self.SHIFT_UP_KEY),
                                                                                            str(self.SHIFT_DOWN_KEY),
                                                                                            str(self.IGNITION_KEY),
                                                                                            str(self.THROTTLE_AXIS),
                                                                                            str(self.BRAKE_AXIS),
                                                                                            str(self.STEER_AXIS),
                                                                                            str(self.VJOY_AXIS),
                                                                                            str(self.BRAKE_KEY),
                                                                                            str(self.ACC_KEY),
                                                                                            str(self.HANDBRAKE_KEY),
                                                                                            str(self.SPARE_KEY_1),
                                                                                            str(self.SPARE_KEY_2),
                                                                                            str(self.CLUTCH_AXIS)))
        try:
            with open('controls.txt', 'w') as file:
                file.write(file_string)
            print("Controls saved successfully")
        except:
            print("An Error has occurred during saving. Make sure controls.txt exists.")
