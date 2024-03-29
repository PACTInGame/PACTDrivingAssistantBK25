import sys
import time
from threading import Thread

import ACC_Setup
import Boardcomputer
import Calculations
import CarDataBase
import CrossTrafficWarning
import ExeRunningChecker
import ForwardCollisionWarning
import Gearbox
import GetControllerInput
import KeyboardMouseEmulator
import Menu
import ParkDistanceControl
import Sounds
import Tips
import Version
import messagehandling
import pyinsim
import wheel
from AdaptiveBrakeLight import AdaptiveBrakeLight
from BlindSpotWarning import check_blindspots_ref
from BusHQ import BusHQ
from BusSimulation import BusSimulation
from CopAssist import CopAssist
from Language import Language
from OwnVehicle import OwnVehicle
from PSC import PSC
from RaceAssist import RaceAssist
from Setting import Setting
from Vehicle import Vehicle


# Button IDs
# 1-10 Head up Display and "Waiting for you to hit the road"
# 6 = Board-computer
# (7,8,9) = Notifications
# 11-20 Bus Simulation
# 20-40 Settings (Menu)
# 41-43 PSC
# 44-47 Blind Spot Warning
# 48-54 PDC
# 100-102 update available
# 103 Mode change (All on, All off, Cop, Race)
# 110 - 120 RaceAssist
# 121 - 130 Gearbox selection
# 131 - 138 CopAssist Menu
# 139 - 141 CopAssist HUD
# 142 - 151 Gearbox Setup
# 152, 153 Controller Setup
class LFSConnection:
    def __init__(self):
        """
        The LFSConnection class is the main class of the program. It contains all the objects for the different
        functionalities of the program. It also connects to the LFS insim port.
        """
        while not ExeRunningChecker.is_lfs_running():
            print("Waiting for LFS to start.")
            time.sleep(3)

        self.version = "0.0.2"
        self.update_available = Version.get_current_version(self.version)
        self.INTERVAL = 200  # TODO doesnt make sense bc Interval will not be updated if changed here
        self.insim = pyinsim.insim(b'127.0.0.1', 29999, Admin=b'', Prefix=b"$",
                                   Flags=pyinsim.ISF_MCI | pyinsim.ISF_LOCAL, Interval=self.INTERVAL)
        self.running = True
        self.notifications = []
        self.players = {}
        self.cars_on_track = []
        self.cars_relevant = []
        self.current_menu = 0  # 0 = None, 1 = Main Menu, 2 = Driving Menu, 3 = Parking Menu, 4 = Bus Menu, 5 = General Menu, 6 = Keys Menu, 7 = Cop Menu

        self.own_vehicle = OwnVehicle()
        self.settings = Setting(self)
        self.bus_simulation = BusSimulation(self)
        self.language = Language(self)
        self.bus_hq = BusHQ(self)
        self.wheel_support = wheel.WheelSupport(self)
        self.gearbox = Gearbox.Gearbox(self)
        self.PSC = PSC(self)
        self.boardcomputer = Boardcomputer.Boardcomputer(self)
        self.boardcomputer.reset()
        self.keyboard_support = KeyboardMouseEmulator
        self.controller_inputs = GetControllerInput.ControllerInput(self)
        self.AdaptiveBrakeLight = AdaptiveBrakeLight(self)
        self.RaceAssist = RaceAssist(self)
        self.CopAssist = CopAssist(self)

        self.outgauge = None
        self.outsim = None
        self.game_time = 0
        self.buttons_on_screen = [0] * 255
        self.valid_ids = {*range(1, 41), *range(48, 55), 101, 103, 112, 113, *range(132, 154)}
        self.collision_warning_intensity = 0
        # two separate variables for cross traffic warning
        # as braking is not directly connected to warning logic
        self.cross_traffic_braking = False
        self.cross_warning_intensity = 0, 0
        self.timers = []
        self.time_MCI = 0
        self.is_connected = False

        # Game Infos
        self.text_entry = False
        self.on_track = False
        self.track = ""
        self.in_game_cam = 0  # 0 = Follow, 1 = Heli, 2 = TV, 3 = Driver, 4 = Custom, 255 = Another
        self.in_game_interface = 0  # 0 = Game, 1 = Options, 2 = Host_Options, 3 = Garage, 4 = Car_select, 5 = Track_select,  6 = ShiftU
        self.submode_interface = 0

        # for checking the previous state
        self.indicator_right_sound = False
        self.indicator_left_sound = False
        self.time_menu_open = 0
        self.cars_previous_speed = []
        self.cars_previous_speed_buffer = []
        self.collision_warning_sound_played = False
        self.cross_traffic_warning_sound_played = False
        self.side_collision_warning_sound_played = time.perf_counter()
        self.obtain_PLID = True
        self.anti_stall_timer = 0

        self.holding_brake = False
        self.lang = self.settings.language
        self.brake_intervention_was_active = True
        # TODO Reset all axis on restart
        self.blindspot_l = False
        self.blindspot_r = False
        self.sidecollision_r = False
        self.sidecollision_l = False
        self.rect_obj = []  # TODO get layout data
        self.front_beep = 0
        self.rear_beep = 0
        self.beep_thread_started = False

        self.last_tip_time = time.perf_counter()
        self.manual_mode_change = False

    def outgauge_packet(self, outgauge, packet):
        """
        The outgauge_packet function is called every time a new outgauge packet is received, which is quite often.
        The packet contains all the information about the car, which is then saved in the own_vehicle object.
        All functions that depend on a very high refresh rate are called such as the head up display.
        """
        # get_own_car_data
        self.game_time = packet.Time
        self.own_vehicle.fuel = packet.Fuel
        self.own_vehicle.speed = packet.Speed * 3.6
        self.own_vehicle.rpm = packet.RPM
        self.own_vehicle.gear = packet.Gear
        if self.obtain_PLID and self.on_track:
            self.own_vehicle.player_id = packet.PLID
            self.obtain_PLID = False
        self.own_vehicle.brake = packet.Brake
        self.own_vehicle.throttle = packet.Throttle
        self.own_vehicle.clutch = packet.Clutch
        self.own_vehicle.turbo = packet.Turbo

        self.own_vehicle.indicator_left = pyinsim.DL_SIGNAL_L & packet.ShowLights
        self.own_vehicle.indicator_right = pyinsim.DL_SIGNAL_R & packet.ShowLights
        self.own_vehicle.hazard_lights = self.own_vehicle.indicator_left and self.own_vehicle.indicator_right
        self.own_vehicle.full_beam_light = pyinsim.DL_FULLBEAM & packet.ShowLights > 0
        self.own_vehicle.low_beam_light = pyinsim.DL_DIPPED & packet.ShowLights > 0
        self.own_vehicle.tc_light = pyinsim.DL_TC & packet.ShowLights > 0
        self.own_vehicle.abs_light = pyinsim.DL_ABS & packet.ShowLights > 0
        self.own_vehicle.handbrake_light = pyinsim.DL_HANDBRAKE & packet.ShowLights > 0
        self.own_vehicle.battery_light = pyinsim.DL_BATTERY & packet.ShowLights > 0
        self.own_vehicle.oil_light = pyinsim.DL_OILWARN & packet.ShowLights > 0
        self.own_vehicle.eng_light = pyinsim.DL_ENGINE & packet.ShowLights > 0

        if self.own_vehicle.cname != packet.Car:
            self.own_vehicle.cname = packet.Car
            if b"Batt" in packet.Display1:
                self.own_vehicle.eng_type = "electric"
            else:
                self.own_vehicle.eng_type = "combustion"

            self.own_vehicle.fuel_capacity = CarDataBase.get_fuel_capa(self.own_vehicle.cname)
            self.own_vehicle.redline = CarDataBase.get_vehicle_redline(self.own_vehicle.cname)
            self.own_vehicle.collision_warning_multiplier = CarDataBase.get_vehicle_length(self.own_vehicle.cname)
            self.own_vehicle.max_gears = CarDataBase.get_max_gears(self.own_vehicle.cname)
            self.gearbox.get_gears_and_max_speed()
        # Function calls
        if self.on_track:
            self.head_up_display()
            self.sound_effects()

    def outsim_packet(self, outsim, packet):
        """
        The outsim_packet function is called every time a new outsim packet is received. The packet contains mainly
        information for sim rigs like motion. We can use it for getting the users steering input.
        """
        # not yet used
        pass

    def start_outgauge(self):
        """
        start_outgauge tries to connect to the outgauge port. For example, when the user was in the menu for more than
        30 seconds. The outgauge connection differs from the insim connection.
        """
        try:
            self.outgauge = pyinsim.outgauge('127.0.0.1', 30000, self.outgauge_packet, 30.0)
        except:
            print("Failed to connect to OutGauge. Maybe it was still active.")

    def start_outsim(self):
        """
        start_outsim tries to connect to the outsim port. For example, when the user was in the menu for more than
        30 seconds. The outsim connection differs from the insim connection.
        """
        try:
            self.outsim = pyinsim.outsim('127.0.0.1', 29998, self.outsim_packet, 30.0)
        except:
            print("Failed to connect to OutSim. Maybe it was still active.")

    def sound_effects(self):
        if self.own_vehicle.roleplay == "civil" and self.settings.pact_mode == 0:
            if self.settings.indicator_sound and not self.AdaptiveBrakeLight.braking:
                if self.own_vehicle.indicator_right != self.indicator_right_sound:
                    self.indicator_right_sound = self.own_vehicle.indicator_right
                    if self.own_vehicle.indicator_right:
                        Sounds.playsound_indicator_on()
                    else:
                        Sounds.playsound_indicator_off()
                elif self.own_vehicle.indicator_left != self.indicator_left_sound:
                    self.indicator_left_sound = self.own_vehicle.indicator_left
                    if self.own_vehicle.indicator_left:
                        Sounds.playsound_indicator_on()
                    else:
                        Sounds.playsound_indicator_off()

    def message_handling(self, insim, mso):
        try:
            message = mso.Msg.decode()
            messagehandling.handle_commands(message, self)
        except:
            pass

    # TODO implement realistic clutch

    def insim_state(self, insim, sta):
        """
        this method receives the is_sta packet from LFS. It contains information about the game state, that will
        be read and saved inside "flags" variable.
        """

        def start_game_insim():
            print("Game started")
            self.on_track = True
            # p = Process(target=self.controller_inputs.check_controller_input)
            # p.start()
            # get_inputs_thread = Thread(target=self.controller_inputs.check_controller_input)
            # get_inputs_thread.start()
            self.insim.send(pyinsim.ISP_MST,
                            Msg=b"/axis %.1i steer" % self.settings.STEER_AXIS)
            self.insim.send(pyinsim.ISP_MST,
                            Msg=b"/axis %.1i brake" % self.settings.BRAKE_AXIS)
            self.insim.send(pyinsim.ISP_MST,
                            Msg=b"/axis %.1i throttle" % self.settings.THROTTLE_AXIS)
            if time.time() - self.time_menu_open >= 30:
                self.start_outgauge()
            insim.bind(pyinsim.ISP_MCI, self.get_car_data)
            insim.send(pyinsim.ISP_TINY, ReqI=255, SubT=pyinsim.TINY_NPL)
            self.del_button(31)
            self.del_button(3)

            if self.update_available:
                self.send_button(100, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 95, 0, 12, 5,
                                 self.language.translation(self.lang, "Update"))

            self.send_button(21, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 100, 0, 12, 5,
                             self.language.translation(self.lang, "Menu"))
            Menu.send_mode(self)

        def start_menu_insim():
            self.time_menu_open = time.time()
            self.on_track = False
            insim.unbind(pyinsim.ISP_MCI, self.get_car_data)
            [self.del_button(i) for i in range(143)]
            [self.del_button(i) for i in range(152, 200)]
            self.send_button(3, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 180, 0, 25, 5,
                             "Waiting for you to hit the road.")

        flags = [int(i) for i in str("{0:b}".format(sta.Flags))]
        self.in_game_cam = sta.InGameCam
        if len(flags) >= 15:
            game = flags[-1] == 1 and flags[-15] == 1

            if not self.on_track and game:
                start_game_insim()

            elif self.on_track and not game:
                start_menu_insim()

        elif self.on_track:
            start_menu_insim()

        self.text_entry = len(flags) >= 16 and flags[-16] == 1
        self.track = sta.Track

    # Player Handling starts here -------------------------------------------------------
    def new_player(self, insim, npl):
        # TODO check all players and remove those that are in list but not in packets
        def remove_control_chars(player_name):
            for i in range(10):
                player_name = player_name.replace(bytes(f"^{i}", 'utf-8'), b"")
            return player_name

        def get_control_mode(flags):
            if len(flags) >= 11 and flags[-11] == 1:
                return 0  # mouse
            elif (len(flags) >= 12 and flags[-12] == 1) or (len(flags) >= 13 and flags[-13] == 1):
                return 1  # keyboard
            else:
                return 2  # wheel

        cars_already_known = [car.player_id for car in self.cars_on_track]

        if npl.PLID not in cars_already_known:
            self.cars_on_track.append(Vehicle(0, 0, 0, 0, 0, 0, 0, npl.PLID, 0, 0, npl.CName))

        for car in self.cars_on_track:
            if npl.PLID == car.player_id:
                if car.cname != npl.CName:
                    car.update_cname(npl.CName)

        if npl.PLID == self.own_vehicle.player_id:
            self.obtain_PLID = True
            flags = [int(i) for i in bin(npl.Flags)[2:]]

            if b"[COP]" in npl.PName:
                self.own_vehicle.roleplay = "cop"
                if not self.manual_mode_change:
                    self.settings.pact_mode = 2
            elif b"[MED]" in npl.PName or b"[RES]" in npl.PName:
                self.own_vehicle.roleplay = "res"
                if not self.manual_mode_change:
                    self.settings.pact_mode = 2
            elif b"[TOW]" in npl.PName:
                self.own_vehicle.roleplay = "tow"
                if not self.manual_mode_change:
                    self.settings.pact_mode = 2
            else:
                self.own_vehicle.roleplay = "civil"
                if not self.manual_mode_change:
                    self.settings.pact_mode = 0
            Menu.send_mode(self)

            if len(flags) >= 4 and flags[-4] == 1:
                self.own_vehicle.gearbox_mode = 0  # automatic
            elif len(flags) >= 5 and flags[-5] == 1:
                self.own_vehicle.gearbox_mode = 1  # shifter
            else:
                self.own_vehicle.gearbox_mode = 2  # sequential

            self.own_vehicle.auto_clutch = len(flags) >= 10 and flags[-10] == 1
            self.own_vehicle.control_mode = get_control_mode(flags)
            self.own_vehicle.player_name = remove_control_chars(npl.PName)

    def player_left(self, insim, pll):
        for car in self.cars_on_track:
            if car.player_id == pll.PLID:
                self.cars_on_track.remove(car)

    def player_pits(self, insim, plp):

        for car in self.cars_on_track:
            if car.player_id == plp.PLID:
                self.cars_on_track.remove(car)

    # Player Handling ends here -------------------------------------------------------

    def on_click(self, insim, btc):
        """
        This recieves the is_btc packet from lfs if a clickable button is pressed, and it handles which menus
        will be opened or closed. Doesn't look that nice yet...
        """
        click_action = False
        click_actions = {}
        if 21 <= btc.ClickID <= 40:  # Menu-Buttons
            if self.current_menu == 0:  # None
                click_action = True

                click_actions = {
                    21: Menu.open_menu,
                }
            elif self.current_menu == 1:  # Main Menu
                click_action = True

                click_actions = {
                    15: self.bus_simulation.open_bus_doors,
                    18: self.bus_simulation.accept_route,
                    21: Menu.open_menu,
                    22: Menu.open_drive_menu,
                    23: Menu.open_park_menu,
                    24: Menu.open_bus_menu,
                    25: self.settings.change_language,
                    26: Menu.open_general_menu,
                    27: Menu.open_keys_menu,
                    28: ACC_Setup.set_up,
                    40: Menu.close_menu,
                }

            elif self.current_menu == 2:  # Driving Menu

                if btc.ClickID == 22:
                    self.settings.forward_collision_warning = not self.settings.forward_collision_warning
                elif btc.ClickID == 23:
                    self.settings.blind_spot_warning = not self.settings.blind_spot_warning
                elif btc.ClickID == 24:
                    self.settings.side_collision_prevention = not self.settings.side_collision_prevention
                elif btc.ClickID == 25:
                    self.settings.cross_traffic_warning = not self.settings.cross_traffic_warning
                elif btc.ClickID == 26:
                    self.settings.PSC = not self.settings.PSC
                elif btc.ClickID == 27:
                    self.settings.light_assist = not self.settings.light_assist
                elif btc.ClickID == 28:
                    self.settings.automatic_indicator_turnoff = not self.settings.automatic_indicator_turnoff
                elif btc.ClickID == 29:
                    self.settings.collision_warning_distance = (self.settings.collision_warning_distance + 1) % 3
                elif btc.ClickID == 30:
                    self.settings.automatic_gearbox = not self.settings.automatic_gearbox
                elif btc.ClickID == 31:
                    self.settings.automatic_emergency_braking = not self.settings.automatic_emergency_braking
                elif btc.ClickID == 33:
                    self.settings.adaptive_brake_light = not self.settings.adaptive_brake_light
                elif btc.ClickID == 34:
                    self.settings.adaptive_brake_light_style = not self.settings.adaptive_brake_light_style
                elif btc.ClickID == 35:
                    self.settings.stall_protection = not self.settings.stall_protection
                elif btc.ClickID == 40:
                    Menu.close_menu(self)
                if not btc.ClickID == 40:
                    Menu.open_drive_menu(self)

            elif self.current_menu == 3:  # Parking Menu
                if btc.ClickID == 22:
                    self.settings.park_distance_control = not self.settings.park_distance_control
                    if not self.settings.park_distance_control:
                        self.settings.visual_parking_aid = False
                        self.settings.audible_parking_aid = False
                    else:
                        self.settings.visual_parking_aid = True
                        self.settings.audible_parking_aid = True
                elif btc.ClickID == 23:
                    self.settings.park_emergency_brake = not self.settings.park_emergency_brake
                elif btc.ClickID == 24:
                    self.settings.visual_parking_aid = not self.settings.visual_parking_aid
                elif btc.ClickID == 25:
                    self.settings.audible_parking_aid = not self.settings.audible_parking_aid
                elif btc.ClickID == 40:
                    Menu.close_menu(self)
                if not btc.ClickID == 40:
                    Menu.open_park_menu(self)

            elif self.current_menu == 4:  # Bus Menu
                if btc.ClickID == 22:
                    self.settings.bus_door_sound = not self.settings.bus_door_sound
                elif btc.ClickID == 23:
                    self.settings.bus_route_sound = not self.settings.bus_route_sound
                elif btc.ClickID == 24:
                    self.settings.bus_announce_sound = not self.settings.bus_announce_sound
                elif btc.ClickID == 25:
                    self.settings.bus_sound_effects = not self.settings.bus_sound_effects
                elif btc.ClickID == 26:
                    self.settings.bus_offline_sim = not self.settings.bus_offline_sim
                elif btc.ClickID == 40:
                    Menu.close_menu(self)
                if not btc.ClickID == 40:
                    Menu.open_bus_menu(self)

            elif self.current_menu == 5:  # General Menu
                if btc.ClickID == 22:
                    self.settings.unit = "metric" if self.settings.unit == "imperial" else "imperial"
                elif btc.ClickID == 24:
                    self.settings.head_up_display = not self.settings.head_up_display
                elif btc.ClickID == 25:
                    self.settings.bc = "range" if self.settings.bc == "off" else "distance" if self.settings.bc == "range" else "off"
                elif btc.ClickID == 27:
                    self.settings.offset_w -= 1
                elif btc.ClickID == 28:
                    self.settings.offset_w += 1
                elif btc.ClickID == 29:
                    self.settings.offset_h -= 1
                elif btc.ClickID == 30:
                    self.settings.offset_h += 1
                elif btc.ClickID == 31:
                    self.settings.indicator_sound = not self.settings.indicator_sound
                elif btc.ClickID == 40:
                    Menu.close_menu(self)
                if not btc.ClickID == 40:
                    Menu.open_general_menu(self)

            elif self.current_menu == 6:  # Keys Menu
                if btc.ClickID == 22:
                    Menu.listen_for_key(self, "shift_up")
                elif btc.ClickID == 24:
                    Menu.listen_for_key(self, "shift_down")
                elif btc.ClickID == 26:
                    Menu.listen_for_key(self, "ignition")
                elif btc.ClickID == 28:
                    Menu.listen_for_key(self, "handbrake")
                if self.own_vehicle.control_mode == 2:
                    if btc.ClickID == 30:
                        Menu.listen_for_key(self, "throttle_axis")
                    elif btc.ClickID == 32:
                        Menu.listen_for_key(self, "brake_axis")
                    elif btc.ClickID == 34:
                        Menu.listen_for_key(self, "steer_axis")
                    elif btc.ClickID == 36:
                        Menu.listen_for_key(self, "clutch_axis")
                    elif btc.ClickID == 38:
                        ACC_Setup.set_up(self)
                else:
                    if btc.ClickID == 30:
                        Menu.listen_for_key(self, "throttle_key")
                    elif btc.ClickID == 32:
                        Menu.listen_for_key(self, "brake_key")
                    elif btc.ClickID == 34:
                        Menu.listen_for_key(self, "spare_key1")
                    elif btc.ClickID == 36:
                        Menu.listen_for_key(self, "spare_key2")
                if btc.ClickID == 40:
                    Menu.close_menu(self)
        elif self.current_menu == 7:  # Cop Menu
            if btc.ClickID == 132:
                self.settings.automatic_siren = not self.settings.automatic_siren
            elif btc.ClickID == 133:
                self.settings.use_indicators = not self.settings.use_indicators
            elif btc.ClickID == 134:
                self.settings.use_light = not self.settings.use_light
            elif btc.ClickID == 135:
                self.settings.use_extra_light = not self.settings.use_extra_light
            elif btc.ClickID == 136:
                self.settings.use_fog_light = not self.settings.use_fog_light
            elif btc.ClickID == 137:
                self.settings.suspect_tracker = not self.settings.suspect_tracker
            elif btc.ClickID == 138:
                Menu.close_cop_menu(self)
            if not btc.ClickID == 138:
                Menu.open_cop_menu(self)
        elif 143 <= btc.ClickID <= 150:  # Gearbox Setup
            self.gearbox.set_up_gear(btc.ClickID - 143)
        elif btc.ClickID == 151:
            self.gearbox.stop_key_listener()

        else:
            click_actions = {
                100: Menu.ask,
                101: Menu.open_google_drive,
                102: Menu.close_ask,
                6: self.boardcomputer.reset,
                103: Menu.change_mode,
                121: self.gearbox.gearbox_select,
                122: self.gearbox.gearbox_select,
                123: self.gearbox.gearbox_select,
                124: self.gearbox.gearbox_select,
                125: self.gearbox.gearbox_select,
                126: self.gearbox.gearbox_select,
                127: self.gearbox.gearbox_select,
                128: self.gearbox.gearbox_select,
                129: self.gearbox.gearbox_select,
                130: self.gearbox.gearbox_select,
                131: Menu.open_cop_menu,
                139: self.CopAssist.toggle_siren,
                140: self.CopAssist.toggle_strobe,

            }
            click_action = True
        if click_action:
            action = click_actions.get(btc.ClickID)
            if 121 <= btc.ClickID <= 130:
                action(btc.ClickID - 121)
            elif action:
                try:
                    action()
                except:
                    action(self)

    def object_detection(self, insim, axm):
        """
        This method is used to get autcross layout objects from LFS. For example for the park distance control to work
        also with layout objects.
        """
        pass

    def send_button(self, click_id, style, t, l, w, h, text, inst=0, typeIn=0):
        """
        This method checks if a button is already on the screen and if not, it sends a new button to LFS.
        It makes sending buttons easier than always sending the entire thing to lfs.
        """
        if self.buttons_on_screen[click_id] == 0 or click_id in self.valid_ids:
            self.buttons_on_screen[click_id] = 1
            if type(text) == str:
                text = text.encode()
            self.insim.send(
                pyinsim.ISP_BTN,
                ReqI=255,
                ClickID=click_id,
                BStyle=style | 3,
                Inst=inst,
                T=t,
                L=l,
                W=w,
                H=h,
                Text=text,
                TypeIn=typeIn)

    def del_button(self, click_id):
        if self.buttons_on_screen[click_id] == 1:
            self.insim.send(pyinsim.ISP_BFN,
                            ReqI=255,
                            ClickID=click_id
                            )
            self.buttons_on_screen[click_id] = 0

    def head_up_display(self):
        """
        This method is responsible for everything displayed on the head up display. This should be very efficient
        as it is called at minimum every 10ms.
        """
        x = self.settings.offset_w
        y = self.settings.offset_h

        def send_speed_button(color_code, speed_unit, speed):
            speed = int(speed)
            self.send_button(1, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 119 + x, 90 + y, 13, 8,
                             f'{color_code}{speed} {speed_unit}')

        def send_rpm_button(color_code, rpm):
            self.send_button(2, pyinsim.ISB_DARK, 119 + x, 103 + y, 13, 8, f'{color_code}%.1f RPM' % (rpm / 1000))

        def send_extra_info_button():
            unit = "km" if self.settings.unit == "metric" else "mi"

            if self.settings.bc == "range":
                range_k = self.boardcomputer.range_km
                color = "^7" if range_k > 20 else "^3" if range_k > 5 else "^1"
                if unit == "mi":
                    range_k = range_k * 0.621371
                self.send_button(6, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 113 + x, 90 + y, 13, 6,
                                 f"{color}{round(range_k) if range_k > 0 else '---'} {unit}")
            elif self.settings.bc == "distance":
                distance = self.boardcomputer.distance_driven_meters / 1000
                if unit == "mi":
                    distance = distance * 0.621371
                self.send_button(6, pyinsim.ISB_DARK, 113 + x, 90 + y, 13, 6,
                                 f"^7{round(distance) if distance > 0 else '0'} {unit}")
            else:
                self.del_button(6)

        def send_warning_button(intensity):
            self.send_button(1, 32 if intensity < 3 else 16, 119 + x, 90 + y, 13, 8, '^1<< ---')
            self.send_button(2, 32 if intensity < 3 else 16, 119 + x, 103 + y, 13, 8, '^1--- >>')

        def send_notifications():
            num_notifications = 0
            for notification in self.notifications:
                if num_notifications < 3:
                    self.send_button(7 + num_notifications, pyinsim.ISB_DARK, 127 + x + num_notifications * 6, 90 + y,
                                     26, 6, notification[0])
                    num_notifications += 1

        # TODO SEND FEEDBACK BUTTON
        def send_cross_button(intensity):
            if intensity[0] == 1:
                if intensity[1] > 180:
                    self.send_button(1, pyinsim.ISB_LIGHT, 119 + x, 90 + y, 13, 8, b'^3^L^H\xa1n\xa1n')
                    self.send_button(2, pyinsim.ISB_LIGHT, 119 + x, 103 + y, 13, 8, b'^3^L^H\xa1n\xa1n')
                else:
                    self.send_button(1, pyinsim.ISB_LIGHT, 119 + x, 90 + y, 13, 8, b'^3^L^H\xa1m\xa1m')
                    self.send_button(2, pyinsim.ISB_LIGHT, 119 + x, 103 + y, 13, 8, b'^3^L^H\xa1m\xa1m')
            else:
                if intensity[1] > 180:
                    self.send_button(1, pyinsim.ISB_LIGHT, 119 + x, 90 + y, 13, 8, b'^1^L^H\xa1n\xa1n')
                    self.send_button(2, pyinsim.ISB_LIGHT, 119 + x, 103 + y, 13, 8, b'^1^L^H\xa1n\xa1n')
                else:
                    self.send_button(1, pyinsim.ISB_LIGHT, 119 + x, 90 + y, 13, 8, b'^1^L^H\xa1m\xa1m')
                    self.send_button(2, pyinsim.ISB_LIGHT, 119 + x, 103 + y, 13, 8, b'^1^L^H\xa1m\xa1m')

        def send_gear_button(gear_mode):
            self.send_button(5, pyinsim.ISB_DARK, 123 + x, 116 + y, 4, 4, '^7' + gear_mode)

        def send_siren_button():
            self.send_button(139, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 119 + x, 84 + y, 6, 4,
                             ('^7' if not self.CopAssist.siren else '^4') + self.language.translation(self.lang,
                                                                                                      'Siren'))
            self.send_button(140, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 123 + x, 84 + y, 6, 4,
                             ('^7' if not self.CopAssist.strobe else '^4') + self.language.translation(self.lang,
                                                                                                       'Strobe'))

        def send_outside_hud():
            if self.settings.pact_mode == 2 and self.current_menu == 0:
                self.send_button(139, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 119, 0, 6, 4,
                                 ('^7' if not self.CopAssist.siren else '^4') + self.language.translation(self.lang,
                                                                                                          'Siren'))
                self.send_button(140, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 123, 0, 6, 4,
                                 ('^7' if not self.CopAssist.strobe else '^4') + self.language.translation(self.lang,
                                                                                                           'Strobe'))
            else:
                self.del_button(139)
                self.del_button(140)
            # TODO create more options for outside hud
            for i in range(1, 10):
                self.del_button(i)

        if self.settings.head_up_display:
            if self.in_game_cam == 3:  # Drivers View
                if self.own_vehicle.gear > 1:
                    if self.own_vehicle.gearbox_mode == 0 or (
                            self.settings.automatic_gearbox and self.own_vehicle.gearbox_mode == 2 and self.gearbox.car_supported):
                        send_gear_button('D%.i' % (self.own_vehicle.gear - 1))
                    else:
                        send_gear_button('%.i' % (self.own_vehicle.gear - 1))

                elif self.own_vehicle.gear == 1:
                    send_gear_button('n')
                elif self.own_vehicle.gear == 0:
                    send_gear_button('r')

                if self.collision_warning_intensity > 0:
                    send_warning_button(self.collision_warning_intensity)
                elif self.cross_warning_intensity[0] > 0:
                    send_cross_button(self.cross_warning_intensity)
                else:
                    if self.settings.unit == "metric":
                        send_speed_button('^7', 'km/h', self.own_vehicle.speed)
                    else:
                        send_speed_button('^7', 'mph', self.own_vehicle.speed * 0.621371)
                    send_rpm_button('^7', self.own_vehicle.rpm)

                if self.settings.pact_mode == 2:
                    send_siren_button()
                else:
                    self.del_button(139)
                    self.del_button(140)
                if self.settings.pact_mode != 1:
                    send_extra_info_button()
                    send_notifications()
            elif self.in_game_cam in [0, 1, 2, 4]:
                send_outside_hud()
            else:
                for i in range(1, 10):
                    self.del_button(i)
                for i in range(139, 142):
                    self.del_button(i)
        else:
            for i in range(1, 10):
                self.del_button(i)
            for i in range(139, 142):
                self.del_button(i)

    def timers_decr(self):
        for i in range(len(self.timers)):
            self.timers[i][0] = self.timers[i][0] - 1

            if self.timers[i][1] == "NPL" and self.timers[i][0] == 0:
                self.timers[i][0] = 20
                self.insim.send(pyinsim.ISP_TINY, ReqI=255, SubT=pyinsim.TINY_NPL)

            elif self.timers[i][1] == "PING" and self.timers[i][0] == 0:
                self.timers[i][0] = 20
                self.insim.send(pyinsim.ISP_TINY, ReqI=255, SubT=pyinsim.TINY_PING)

    def start_assistants(self):
        """
        This method is called every 200ms to start all driver assistance functions.
        """
        self.get_relevant_cars()


        def anti_stall():
            if self.own_vehicle.eng_type == "combustion" and self.own_vehicle.rpm < 200 and self.controller_inputs.accelerator > 0.1:
                if self.own_vehicle.battery_light:
                    self.gearbox.send([self.settings.IGNITION_KEY, self.settings.IGNITION_KEY])
                else:
                    self.gearbox.send([self.settings.IGNITION_KEY])
                send = True
                for notes in self.notifications:
                    if notes[0] == "^3Anti-Stall":
                        send = False
                if send:
                    self.notifications.append(["^3Anti-Stall", 2])

        def brake_emergency():
            self.brake_intervention_was_active = True
            if self.settings.automatic_emergency_braking and ALL_ON:
                if self.own_vehicle.control_mode == 2:
                    self.wheel_support.use_wheel_collision_warning(self)
                elif self.own_vehicle.control_mode == 1 or self.own_vehicle.control_mode == 0:
                    self.keyboard_support.use_keyboard_collision_warning(self)

        def release_brake():
            if self.brake_intervention_was_active:
                if self.own_vehicle.control_mode == 2:
                    self.wheel_support.use_wheel_stop(self)
                elif self.own_vehicle.control_mode == 1 or self.own_vehicle.control_mode == 0:
                    self.keyboard_support.release_brake(self)
                self.brake_intervention_was_active = False

        def start_collision_warning():
            if 12 < self.own_vehicle.speed or (
                    self.collision_warning_intensity > 0 and self.own_vehicle.speed > 0.5) and self.own_vehicle.gear > 1:
                ForwardCollisionWarning.forward_collision_warning(self)
            else:
                self.collision_warning_intensity = 0
            if self.collision_warning_intensity > 2:
                brake_emergency()
            else:
                if not self.cross_traffic_braking:
                    release_brake()
            if self.collision_warning_intensity > 1 and not self.collision_warning_sound_played:
                Sounds.collision_warning_sound(self.settings.collision_warning_sound)
                self.collision_warning_sound_played = True
            if self.collision_warning_sound_played and self.collision_warning_intensity == 0:
                self.collision_warning_sound_played = False

        def start_cross_traffic_warning():
            self.cross_traffic_braking = CrossTrafficWarning.cross_traffic(self)
            if self.cross_traffic_braking:
                brake_emergency()
            elif self.collision_warning_intensity < 3:
                release_brake()
            if self.cross_warning_intensity[0] > 1 and not self.cross_traffic_warning_sound_played:
                Sounds.collision_warning_sound(self.settings.collision_warning_sound)
                self.cross_traffic_warning_sound_played = True
            if self.cross_traffic_warning_sound_played and self.cross_warning_intensity[0] == 0:
                self.cross_traffic_warning_sound_played = False

        def start_bus_sim():
            if self.bus_simulation.active:
                self.bus_simulation.check_bus_simulation()
            if self.settings.bus_offline_sim:
                self.bus_hq.check_bus_radio()
            if self.bus_simulation.new_route_offer != 0:
                self.bus_simulation.route_offer()
            else:
                self.del_button(18)
            if not self.bus_simulation.active:
                for i in range(11, 18):
                    self.del_button(i)
                self.bus_simulation.route = None

        def start_blindspot():
            self.blindspot_r, self.blindspot_l, self.sidecollision_r, self.sidecollision_l = check_blindspots_ref(self)
            if self.blindspot_l:
                self.send_button(44, pyinsim.ISB_DARK, 110, 10, 5, 10, '^3!')
            else:
                self.del_button(44)

            if self.blindspot_r:
                self.send_button(45, pyinsim.ISB_DARK, 110, 190, 5, 10, '^3!')
            else:
                self.del_button(45)

        def start_side_collision_prevention():
            time_now = time.perf_counter()
            if self.sidecollision_l:
                self.send_button(46, pyinsim.ISB_DARK, 110, 15, 10, 15, '^1!')
                if time_now > self.side_collision_warning_sound_played + 2:
                    self.side_collision_warning_sound_played = time.perf_counter()
                    Sounds.collision_warning_sound(self.settings.collision_warning_sound)
            else:
                self.del_button(46)

            if self.sidecollision_r:
                self.send_button(47, pyinsim.ISB_DARK, 110, 180, 10, 15, '^1!')
                if time_now > self.side_collision_warning_sound_played + 2:
                    self.side_collision_warning_sound_played = time.perf_counter()
                    Sounds.collision_warning_sound(self.settings.collision_warning_sound)
            else:
                self.del_button(47)

        def start_park_assistance():
            sensors = ParkDistanceControl.sensors(self)
            ParkDistanceControl.draw_pdc_buttons(self, sensors)

            if self.settings.audible_parking_aid:
                if not self.beep_thread_started and (self.front_beep > 0 or self.rear_beep > 0):
                    self.beep_thread_started = True
                    park_beep_thread = Thread(target=ParkDistanceControl.beep(self))
                    park_beep_thread.start()
                if self.front_beep == 0 and self.rear_beep == 0:
                    self.beep_thread_started = False

        def start_boardcomputer():
            if self.own_vehicle.fuel > self.boardcomputer.percent_fuel_at_reset:
                self.boardcomputer.reset()
            self.boardcomputer.update()

        def check_notifications():
            if self.notifications:
                self.notifications[0][1] -= 0.2
                if self.notifications[0][1] <= 0:
                    self.del_button(7)
                    self.del_button(8)
                    self.del_button(9)
                    del self.notifications[0]

        ALL_ON = self.settings.pact_mode == 0
        ALL_OFF = self.settings.pact_mode == 1
        COP = self.settings.pact_mode == 2
        RACE = self.settings.pact_mode == 3

        if not ALL_OFF and not RACE:
            if self.settings.forward_collision_warning:
                start_collision_warning()

            if self.settings.automatic_gearbox:
                if self.own_vehicle.gearbox_mode == 2:
                    self.gearbox.calculate_gear()
                else:
                    self.gearbox.notify_user_sequential()

            if self.settings.PSC and not COP:
                self.controller_inputs.check_controller_input()
                self.PSC.calculate_psc()

            if self.settings.blind_spot_warning:
                start_blindspot()

            if self.settings.cross_traffic_warning and not COP:
                start_cross_traffic_warning()

            if self.settings.side_collision_prevention and not COP:
                start_side_collision_prevention()

            if self.settings.park_distance_control and self.own_vehicle.speed < 10:
                start_park_assistance()
            else:
                self.rear_beep = 0
                self.front_beep = 0
                self.beep_thread_started = False
                ParkDistanceControl.del_pdc_buttons(self)

            if self.settings.bc != "none":
                start_boardcomputer()

            if self.settings.adaptive_brake_light:
                self.AdaptiveBrakeLight.update()

            if ALL_ON:
                bus_thread = Thread(target=start_bus_sim)
                bus_thread.start()

            if self.notifications:
                check_notifications()

            if self.last_tip_time < time.perf_counter() - 120 and self.settings.pact_mode == 0:
                self.last_tip_time = time.perf_counter()
                tip = Tips.get_tip(self.settings.language)
                self.insim.send(pyinsim.ISP_MSL, Msg=tip.encode())

            if COP:
                self.CopAssist.run()
            else:
                if self.settings.light_assist:
                    if not self.own_vehicle.low_beam_light and not self.AdaptiveBrakeLight.braking:
                        self.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL,
                                        UVal=pyinsim.LCL_SET_LIGHTS | pyinsim.LCL_Mask_LowBeam)
            if self.settings.stall_protection:
                anti_stall()
        if RACE:
            self.RaceAssist.update_coordinates_and_timestamp()
            self.RaceAssist.check_live_delta_previous_lap()
            self.RaceAssist.check_live_delta_best_lap()

    def get_relevant_cars(self):
        """
        This function decides if a car is relevant for the driver assistance functions or not. Therefore, the workload
        is reduced and the program runs faster.
        """
        relevant_cars = []

        for car in self.cars_on_track:
            if 0 < car.distance < 130:
                angle = Calculations.calculate_angle(self.own_vehicle.x, car.x, self.own_vehicle.y, car.y,
                                                     self.own_vehicle.heading)
                relevant_cars.append([car, angle])

        relevant_cars = sorted(relevant_cars, key=lambda x: Calculations.get_distance(x))

        many_cars = False
        while len(relevant_cars) > 6:
            del relevant_cars[-1]
            if self.CopAssist.siren and not self.CopAssist.siren_fast and self.settings.automatic_siren:
                self.CopAssist.siren_fast = True
                self.insim.send(pyinsim.ISP_MST, Msg=b"/siren fast")
            many_cars = True

        if self.CopAssist.siren and not many_cars and self.CopAssist.siren_fast and self.settings.automatic_siren:
            self.CopAssist.siren_fast = False
            self.insim.send(pyinsim.ISP_MST, Msg=b"/siren slow")

        self.cars_relevant = relevant_cars

    def get_car_data(self, insim, MCI):
        """
        This method is called every time a new MCI packet is received. It stores all information about the cars on track.
        However, since there might be multiple MCI packets, as one packet can only contain up to 8 cars, some of the
        functionaltiy will only be called every 200 ms to reduce the workload, such as the driver assistance functions.
        """
        if not self.running:
            sys.exit()
        curr_time = time.time()

        if curr_time - self.time_MCI > 0.1:
            self.time_MCI = curr_time
            self.timers_decr()
            warnings_thread = Thread(target=self.start_assistants)
            warnings_thread.start()

        # DATA RECEIVING ---------------
        updated_this_packet = []
        [car.update_data(data.X, data.Y, data.Z, data.Heading, data.Direction, data.AngVel, data.Speed / 91.02,
                         data.PLID)
         for data
         in MCI.Info for car in self.cars_on_track if car.player_id == data.PLID]
        [updated_this_packet.append(data.PLID) for data in MCI.Info]

        self.cars_previous_speed = self.cars_previous_speed_buffer
        self.cars_previous_speed_buffer = []

        for i, j in enumerate(self.cars_on_track):
            if j.player_id == self.own_vehicle.player_id:
                self.own_vehicle.speed_mci = j.speed
                self.own_vehicle.x = j.x
                self.own_vehicle.y = j.y
                self.own_vehicle.z = j.z
                self.own_vehicle.heading = j.heading
                self.own_vehicle.direction = j.direction
                self.own_vehicle.steer_forces = j.steer_forces
            self.cars_previous_speed_buffer.append((j.speed, j.player_id))

        [car.update_dynamic(speed[0] - car.speed) for speed in self.cars_previous_speed for car in
         self.cars_on_track if
         speed[1] == car.player_id and speed[0] - car.speed != 0.0]

        [car.update_distance(self.own_vehicle.x, self.own_vehicle.y, self.own_vehicle.z) for car in
         self.cars_on_track]

    def get_pings(self, insim, ping):
        if not self.is_connected:
            self.is_connected = True
            print("connection to LFS successful")
            self.insim.send(pyinsim.ISP_TINY, ReqI=255, SubT=pyinsim.TINY_SST)

    def get_laptimes(self, insim, lap):
        if self.own_vehicle.player_id == lap.PLID:
            self.RaceAssist.update_lap_time(lap.LTime)
            self.RaceAssist.update_total_time(lap.ETime)
            self.RaceAssist.update_laps_done(lap.LapsDone)

    def get_split_times(self, insim, spx):
        if self.own_vehicle.player_id == spx.PLID:
            self.RaceAssist.update_split_times(spx.Split, spx.STime)
            self.RaceAssist.update_total_time(spx.ETime)

    def get_interface_mode(self, insim, cim):
        self.in_game_interface = cim.Mode
        self.submode_interface = cim.SubMode
        print(self.in_game_interface, self.submode_interface)
        if self.in_game_interface == 3 and self.submode_interface == pyinsim.GRG_DRIVE:
            self.gearbox.set_up_screen()
        else:
            self.gearbox.delete_gearbox_builder()

    def run(self):
        self.insim.bind(pyinsim.ISP_CIM, self.get_interface_mode)
        self.insim.bind(pyinsim.ISP_MCI, self.get_car_data)
        self.insim.bind(pyinsim.ISP_MSO, self.message_handling)
        self.insim.bind(pyinsim.ISP_STA, self.insim_state)
        self.insim.bind(pyinsim.ISP_NPL, self.new_player)
        self.insim.bind(pyinsim.ISP_PLL, self.player_left)
        self.insim.bind(pyinsim.ISP_PLP, self.player_pits)
        self.insim.bind(pyinsim.ISP_BTC, self.on_click)
        self.insim.bind(pyinsim.ISP_AXM, self.object_detection)
        self.insim.bind(pyinsim.TINY_PING, self.get_pings)
        self.insim.bind(pyinsim.ISP_LAP, self.get_laptimes)
        self.insim.bind(pyinsim.ISP_SPX, self.get_split_times)
        self.start_outgauge()
        self.insim.send(pyinsim.ISP_TINY, ReqI=255, SubT=pyinsim.TINY_NPL)
        self.timers.append([20, "NPL"])  # Timer 1
        self.timers.append([20, "PING"])  # Timer 2
        self.insim.send(pyinsim.ISP_TINY, ReqI=255, SubT=pyinsim.TINY_AXM)
        self.insim.send(pyinsim.ISP_TINY, ReqI=255, SubT=pyinsim.TINY_SST)
        pyinsim.run()


if __name__ == '__main__':
    lfs_connection = LFSConnection()
    lfs_connection.run()
