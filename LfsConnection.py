import sys
import time
from threading import Thread

import Calculations
import CarDataBase
import ForwardCollisionWarning
import Menu
import Sounds
import pyinsim
from BusHQ import BusHQ
from BusSimulation import BusSimulation
from Language import Language
from OwnVehicle import OwnVehicle
from Setting import Setting
from Vehicle import Vehicle


# Button IDs
# 1-10 Head up Display and "Waiting for you to hit the road"
# 11-20 Bus Simulation
# 20-40 Settings (Menu)

class LFSConnection:
    def __init__(self):

        self.insim = pyinsim.insim(b'127.0.0.1', 29999, Admin=b'', Prefix=b"$",
                                   Flags=pyinsim.ISF_MCI | pyinsim.ISF_LOCAL, Interval=200)
        self.running = True
        self.players = {}
        self.cars_on_track = []
        self.cars_relevant = []

        self.own_vehicle = OwnVehicle()
        self.settings = Setting(self)
        self.bus_simulation = BusSimulation(self)
        self.language = Language(self)
        self.bus_hq = BusHQ(self)

        self.outgauge = None
        self.game_time = 0
        self.buttons_on_screen = [0] * 255
        self.valid_ids = {*range(1, 41)}
        self.collision_warning_intensity = 0
        self.timers = []
        self.time_MCI = 0
        self.is_connected = False

        # Game Infos
        self.text_entry = False
        self.on_track = False
        self.in_pits = False
        self.track = ""

        # for checking the previous state
        self.indicator_right_sound = False
        self.indicator_left_sound = False
        self.time_menu_open = 0
        self.cars_previous_speed = []
        self.cars_previous_speed_buffer = []
        self.collision_warning_sound_played = False

    def outgauge_packet(self, outgauge, packet):
        # get_own_car_data
        self.game_time = packet.Time
        self.own_vehicle.fuel = packet.Fuel
        self.own_vehicle.speed = packet.Speed * 3.6 if self.settings.unit == 0 else packet.Speed * 2.236
        self.own_vehicle.rpm = packet.RPM
        self.own_vehicle.gear = packet.Gear
        self.own_vehicle.player_id = packet.PLID
        self.own_vehicle.brake = packet.Brake
        self.own_vehicle.throttle = packet.Throttle
        self.own_vehicle.clutch = packet.Clutch
        self.own_vehicle.turbo = packet.Turbo

        self.own_vehicle.indicator_left = pyinsim.DL_SIGNAL_L & packet.ShowLights
        self.own_vehicle.indicator_right = pyinsim.DL_SIGNAL_R & packet.ShowLights
        self.own_vehicle.hazard_lights = self.own_vehicle.indicator_left and self.own_vehicle.indicator_right
        self.own_vehicle.full_beam_light = pyinsim.DL_FULLBEAM & packet.ShowLights > 0
        self.own_vehicle.tc_light = pyinsim.DL_TC & packet.ShowLights > 0
        self.own_vehicle.abs_light = pyinsim.DL_ABS & packet.ShowLights > 0
        self.own_vehicle.handbrake_light = pyinsim.DL_HANDBRAKE & packet.ShowLights > 0
        self.own_vehicle.battery_light = pyinsim.DL_BATTERY & packet.ShowLights > 0
        self.own_vehicle.oil_light = pyinsim.DL_OILWARN & packet.ShowLights > 0
        self.own_vehicle.eng_light = pyinsim.DL_SPARE & packet.ShowLights > 0

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

        # Function calls
        if self.on_track:
            self.head_up_display()
            self.sound_effects()

    def start_outgauge(self):
        try:
            self.outgauge = pyinsim.outgauge('127.0.0.1', 30000, self.outgauge_packet, 30.0)
        except:
            print("Failed to connect to OutGauge. Maybe it was still active.")

    def sound_effects(self):
        if self.own_vehicle.roleplay == "civil":
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
        pass

    def insim_state(self, insim, sta):
        def start_game_insim():
            self.on_track = True
            self.in_pits = False
            if time.time() - self.time_menu_open >= 30:
                self.start_outgauge()
            insim.bind(pyinsim.ISP_MCI, self.get_car_data)
            insim.send(pyinsim.ISP_TINY, ReqI=255, SubT=pyinsim.TINY_NPL)
            self.del_button(31)
            self.del_button(3)
            self.send_button(21, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 100, 0, 7, 5, "Menu")

        def start_menu_insim():
            self.time_menu_open = time.time()
            self.on_track = False
            self.in_pits = False
            insim.unbind(pyinsim.ISP_MCI, self.get_car_data)
            [self.del_button(i) for i in range(200)]
            self.send_button(3, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 180, 0, 25, 5,
                             "Waiting for you to hit the road.")

        flags = [int(i) for i in str("{0:b}".format(sta.Flags))]

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

    def new_player(self, insim, npl):
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
            flags = [int(i) for i in bin(npl.Flags)[2:]]

            if b"[COP]" in npl.PName:
                self.own_vehicle.roleplay = "cop"
            elif b"[MED]" in npl.PName or b"[RES]" in npl.PName:
                self.own_vehicle.roleplay = "res"
            elif b"[TOW]" in npl.PName:
                self.own_vehicle.roleplay = "tow"
            else:
                self.own_vehicle.roleplay = "civil"
                self.del_button(33)
                self.del_button(34)

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
        pass

    def player_pits(self, insim, plp):
        pass

    def on_click(self, insim, btc):
        click_actions = {
            15: self.bus_simulation.open_bus_doors,
            18: self.bus_simulation.accept_route,
            21: Menu.open_menu,
            24: Menu.open_bus_menu,
            25: self.settings.change_language,
            26: self.settings.activate_bus_offline,
            40: Menu.close_menu,

        }
        action = click_actions.get(btc.ClickID)
        if action:
            try:
                action()
            except:
                action(self)

    def object_detection(self, insim, axm):
        pass

    def send_button(self, click_id, style, t, l, w, h, text):
        if self.buttons_on_screen[click_id] == 0 or click_id in self.valid_ids:
            self.buttons_on_screen[click_id] = 1
            if type(text) == str:
                text = text.encode()
            self.insim.send(
                pyinsim.ISP_BTN,
                ReqI=255,
                ClickID=click_id,
                BStyle=style | 3,
                T=t,
                L=l,
                W=w,
                H=h,
                Text=text)

    def del_button(self, click_id):
        if self.buttons_on_screen[click_id] == 1:
            self.insim.send(pyinsim.ISP_BFN,
                            ReqI=255,
                            ClickID=click_id
                            )
            self.buttons_on_screen[click_id] = 0

    def head_up_display(self):
        x = self.settings.offset_w
        y = self.settings.offset_h

        def send_speed_button(color_code, speed_unit, speed):
            speed = int(speed)
            self.send_button(1, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 119 + x, 90 + y, 13, 8,
                             f'{color_code}{speed} {speed_unit}')

        def send_rpm_button(color_code, rpm):
            self.send_button(2, pyinsim.ISB_DARK, 119 + x, 103 + y, 13, 8, f'{color_code}%.1f RPM' % (rpm / 1000))

        def send_warning_button(intensity):
            self.send_button(1, 32 if intensity < 3 else 16, 119 + x, 90 + y, 13, 8, '^1<< ---')
            self.send_button(2, 32 if intensity < 3 else 16, 119 + x, 103 + y, 13, 8, '^1--- >>')

        def send_gear_button(gear_mode):
            self.send_button(5, pyinsim.ISB_DARK, 123 + x, 116 + y, 4, 4, '^7' + gear_mode)

        if self.settings.head_up_display:
            if self.own_vehicle.gear > 1:
                if self.own_vehicle.gearbox_mode > 0 and not self.settings.automatic_gearbox:
                    send_gear_button('%.i' % (self.own_vehicle.gear - 1))
                else:
                    send_gear_button('D%.i' % (self.own_vehicle.gear - 1))
            elif self.own_vehicle.gear == 1:
                send_gear_button('n')
            elif self.own_vehicle.gear == 0:
                send_gear_button('r')

            if self.collision_warning_intensity > 0:
                send_warning_button(self.collision_warning_intensity)
            else:
                send_speed_button('^7', 'km/h', self.own_vehicle.speed)
                send_rpm_button('^7', self.own_vehicle.rpm)

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
        self.get_relevant_cars()
        # Collision_Warning
        if 12 < self.own_vehicle.speed or (
                self.collision_warning_intensity > 0 and self.own_vehicle.speed > 0.5) and self.own_vehicle.gear > 1:
            ForwardCollisionWarning.forward_collision_warning(self)
        else:
            self.collision_warning_intensity = 0
        if self.collision_warning_intensity > 1 and not self.collision_warning_sound_played:
            Sounds.collision_warning_sound(self.settings.collision_warning_sound)
            self.collision_warning_sound_played = True
        if self.collision_warning_sound_played and self.collision_warning_intensity == 0:
            self.collision_warning_sound_played = False

        # Bus Simulation
        if self.bus_simulation.active:
            self.bus_simulation.check_bus_simulation()
        if self.settings.bus_offline_sim:
            self.bus_hq.check_bus_radio()
        if self.bus_simulation.new_route_offer != 0:
            self.bus_simulation.route_offer()

    def get_relevant_cars(self):
        relevant_cars = []

        for car in self.cars_on_track:
            if 0 < car.distance < 130:
                angle = Calculations.calculate_angle(self.own_vehicle.x, car.x, self.own_vehicle.y, car.y,
                                                     self.own_vehicle.heading)
                relevant_cars.append([car, angle])

        relevant_cars = sorted(relevant_cars, key=lambda x: Calculations.get_distance(x))

        many_cars = False
        while len(relevant_cars) > 8:
            del relevant_cars[-1]
            if self.own_vehicle.siren_active and not self.own_vehicle.siren_fast and self.settings.cop_aid_system:
                self.insim.send(pyinsim.ISP_MST, Msg=b"/siren fast")
            many_cars = True

        if self.own_vehicle.siren_active and not many_cars and self.own_vehicle.siren_fast and self.settings.cop_aid_system:
            self.insim.send(pyinsim.ISP_MST, Msg=b"/siren slow")

        self.cars_relevant = relevant_cars

    def get_car_data(self, insim, MCI):
        if not self.running:
            sys.exit()
        curr_time = time.time()

        if curr_time - self.time_MCI > 0.1:
            self.time_MCI = curr_time
            self.timers_decr()
            warnings_thread = Thread(target=self.start_assistants)
            warnings_thread.start()
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

            [car.update_distance(self.own_vehicle.x, self.own_vehicle.y, self.own_vehicle.z) for car in
             self.cars_on_track]
            [car.update_dynamic(speed[0] - car.speed) for speed in self.cars_previous_speed for car in
             self.cars_on_track if
             speed[1] == car.player_id and speed[0] - car.speed != 0.0]

        # DATA RECEIVING ---------------
        updated_this_packet = []
        [car.update_data(data.X, data.Y, data.Z, data.Heading, data.Direction, data.AngVel, data.Speed / 91.02,
                         data.PLID)
         for data
         in MCI.Info for car in self.cars_on_track if car.player_id == data.PLID]
        [updated_this_packet.append(data.PLID) for data in MCI.Info]

    def get_pings(self, insim, ping):
        self.is_connected = True

    def run(self):
        self.insim.bind(pyinsim.ISP_MCI, self.get_car_data)
        self.insim.bind(pyinsim.ISP_MSO, self.message_handling)
        self.insim.bind(pyinsim.ISP_STA, self.insim_state)
        self.insim.bind(pyinsim.ISP_NPL, self.new_player)
        self.insim.bind(pyinsim.ISP_PLL, self.player_left)
        self.insim.bind(pyinsim.ISP_PLP, self.player_pits)
        self.insim.bind(pyinsim.ISP_BTC, self.on_click)
        self.insim.bind(pyinsim.ISP_AXM, self.object_detection)
        self.insim.bind(pyinsim.TINY_PING, self.get_pings)
        self.start_outgauge()
        self.insim.send(pyinsim.ISP_TINY, ReqI=255, SubT=pyinsim.TINY_NPL)
        self.timers.append([20, "NPL"])  # Timer 1
        self.timers.append([20, "PING"])  # Timer 2
        self.insim.send(pyinsim.ISP_TINY, ReqI=255, SubT=pyinsim.TINY_AXM)
        self.insim.send(pyinsim.ISP_TINY, ReqI=255, SubT=pyinsim.ISP_STA)
        pyinsim.run()


if __name__ == '__main__':
    lfs_connection = LFSConnection()
    lfs_connection.run()
