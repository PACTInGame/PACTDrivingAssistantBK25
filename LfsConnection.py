import time

import pyinsim
from OwnVehicle import OwnVehicle
from Setting import Setting
from Vehicle import Vehicle


# Button IDs
# 1-10 Head up Display
class LFSConnection:
    def __init__(self):
        self.insim = pyinsim.insim(b'127.0.0.1', 29999, Admin=b'', Prefix=b"$",
                                   Flags=pyinsim.ISF_MCI | pyinsim.ISF_LOCAL, Interval=200)

        self.players = {}
        self.cars_on_track = []
        self.cars_relevant = []
        self.own_vehicle = OwnVehicle()
        self.outgauge = None
        self.game_time = 0
        self.buttons_on_screen = [0] * 255
        self.valid_ids = {*range(1, 10)}
        self.collision_warning_intensity = 0
        self.settings = Setting()
        self.timers = []
        self.time_MCI = 0

    def outgauge_packet(self, outgauge, packet):
        # get_own_car_data
        self.game_time = packet.Time
        self.own_vehicle.fuel = packet.Fuel
        self.own_vehicle.speed = packet.Speed
        self.own_vehicle.rpm = packet.RPM
        self.own_vehicle.gear = packet.Gear
        self.own_vehicle.cname = packet.Car
        self.own_vehicle.player_id = packet.PLID
        self.own_vehicle.brake_pressure = packet.Brake
        self.own_vehicle.throttle = packet.Throttle
        self.own_vehicle.clutch = packet.Clutch
        self.own_vehicle.turbo = packet.Turbo
        if b"Batt" in packet.Display1:
            self.own_vehicle.eng_type = "electric"
        else:
            self.own_vehicle.eng_type = "combustion"
        self.own_vehicle.indicator_left = pyinsim.DL_SIGNAL_L & packet.ShowLights
        self.own_vehicle.indicator_right = pyinsim.DL_SIGNAL_R & packet.ShowLights
        self.own_vehicle.hazard_lights = self.own_vehicle.indicator_left and self.own_vehicle.indicator_right
        self.own_vehicle.full_beam_light = pyinsim.DL_FULLBEAM & packet.ShowLights > 0
        self.own_vehicle.tc_light = pyinsim.DL_TC & packet.ShowLights > 0
        self.own_vehicle.abs_light = pyinsim.DL_ABS & packet.ShowLights > 0
        self.own_vehicle.handbrake_light = pyinsim.DL_HANDBRAKE & packet.ShowLights > 0
        self.own_vehicle.battery_light = pyinsim.DL_BATTERY & packet.ShowLights > 0
        self.own_vehicle.oil_light = pyinsim.DL_OILWARN & packet.ShowLights > 0

        # Function calls
        self.head_up_display()

    def start_outgauge(self):
        print("outgauge_started")
        self.outgauge = pyinsim.outgauge('127.0.0.1', 30000, self.outgauge_packet, 30.0)

    def message_handling(self, insim, mso):
        pass

    def insim_state(self, insim, sta):
        pass

    def new_player(self, insim, npl):
        cars_already_known = [car.player_id for car in self.cars_on_track]

        if npl.PLID not in cars_already_known:
            self.cars_on_track.append(Vehicle(0, 0, 0, 0, 0, 0, 0, npl.PLID, 0, 0, npl.CName))
        for car in self.cars_on_track:
            if npl.PLID == car.player_id:
                if car.cname != npl.CName:
                    car.update_cname(npl.CName)
        print("new_player")

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
        pass

    def object_detection(self, insim, axm):
        pass

    def send_button(self, click_id, style, t, l, w, h, text):
        if self.buttons_on_screen[click_id] == 0 or click_id in self.valid_ids:
            self.buttons_on_screen[click_id] = 1
            self.insim.send(
                pyinsim.ISP_BTN,
                ReqI=255,
                ClickID=click_id,
                BStyle=style | 3,
                T=t,
                L=l,
                W=w,
                H=h,
                Text=text.encode())

    def del_button(self, click_id):
        if self.buttons_on_screen[click_id] == 1:
            self.insim.send(pyinsim.ISP_BFN,
                            ReqI=255,
                            ClickID=click_id
                            )
            self.buttons_on_screen[click_id] = 0

    def head_up_display(self):
        def send_speed_button(color_code, speed_unit, speed):
            speed = int(speed)
            self.send_button(1, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 119, 90, 13, 8,
                             f'{color_code}{speed} {speed_unit}')

        def send_rpm_button(color_code, rpm):
            self.send_button(2, pyinsim.ISB_DARK, 119, 103, 13, 8, f'{color_code}%.1f RPM' % (rpm / 1000))

        def send_warning_button(intensity):
            self.send_button(3, pyinsim.ISB_DARK + 10 * (intensity == 2), 119, 90, 13, 8, '^1<< ---')
            self.send_button(4, pyinsim.ISB_DARK + 10 * (intensity == 2), 119, 103, 13, 8, '^1--- >>')

        def send_gear_button(gear_mode):
            self.send_button(5, pyinsim.ISB_DARK, 123, 116, 4, 4, '^7' + gear_mode)

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
                send_speed_button('^7', 'km/h', self.own_vehicle.speed * 3.6)
                send_rpm_button('^7', self.own_vehicle.rpm)

    def timers_decr(self):
        for i in range(len(self.timers)):
            self.timers[i][0] = self.timers[i][0] - 1

            if self.timers[i][1] == "NPL" and self.timers[i][0] == 0:
                self.timers[i][0] = 20
                self.insim.send(pyinsim.ISP_TINY, ReqI=255, SubT=pyinsim.TINY_NPL)

    def get_car_data(self, insim, MCI):
        if time.time() - self.time_MCI > 0.1:
            self.timers_decr()
        # DATA RECEIVING ---------------
        updated_this_packet = []
        [car.update_data(data.X, data.Y, data.Z, data.Heading, data.Direction, data.AngVel, data.Speed / 91.02,
                         data.PLID)
         for data
         in MCI.Info for car in self.cars_on_track if car.player_id == data.PLID]
        [updated_this_packet.append(data.PLID) for data in MCI.Info]

    def run(self):
        self.insim.bind(pyinsim.ISP_MCI, self.get_car_data)
        self.insim.bind(pyinsim.ISP_MSO, self.message_handling)
        self.insim.bind(pyinsim.ISP_STA, self.insim_state)
        self.insim.bind(pyinsim.ISP_NPL, self.new_player)
        self.insim.bind(pyinsim.ISP_PLL, self.player_left)
        self.insim.bind(pyinsim.ISP_PLP, self.player_pits)
        self.insim.bind(pyinsim.ISP_BTC, self.on_click)
        self.insim.bind(pyinsim.ISP_AXM, self.object_detection)
        self.start_outgauge()
        self.insim.send(pyinsim.ISP_TINY, ReqI=255, SubT=pyinsim.TINY_NPL)
        self.timers.append([20, "NPL"])
        self.insim.send(pyinsim.ISP_TINY, ReqI=255, SubT=pyinsim.TINY_AXM)
        pyinsim.run()


if __name__ == '__main__':
    lfs_connection = LFSConnection()
    lfs_connection.run()
