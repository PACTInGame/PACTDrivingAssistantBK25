import pyinsim
from OwnVehicle import OwnVehicle


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
        print(self.own_vehicle.full_beam_light)
    def start_outgauge(self):
        print("outgauge_started")
        self.outgauge = pyinsim.outgauge('127.0.0.1', 30000, self.outgauge_packet, 30.0)

    def message_handling(self, insim, mso):
        pass

    def insim_state(self, insim, sta):
        pass

    def new_player(self, insim, npl):
        pass

    def player_left(self, insim, pll):
        pass

    def player_pits(self, insim, plp):
        pass

    def on_click(self, insim, btc):
        pass

    def object_detection(self, insim, axm):
        pass

    def run(self):
        self.insim.bind(pyinsim.ISP_MSO, self.message_handling)
        self.insim.bind(pyinsim.ISP_STA, self.insim_state)
        self.insim.bind(pyinsim.ISP_NPL, self.new_player)
        self.insim.bind(pyinsim.ISP_PLL, self.player_left)
        self.insim.bind(pyinsim.ISP_PLP, self.player_pits)
        self.insim.bind(pyinsim.ISP_BTC, self.on_click)
        self.insim.bind(pyinsim.ISP_AXM, self.object_detection)
        self.start_outgauge()
        pyinsim.run()


if __name__ == '__main__':
    lfs_connection = LFSConnection()
    lfs_connection.run()
