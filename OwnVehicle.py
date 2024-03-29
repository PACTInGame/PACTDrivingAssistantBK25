import math


class OwnVehicle:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.heading = 0
        self.direction = 0
        self.steer_forces = 0
        self.speed = 0
        self.speed_mci = 0
        self.player_id = 0
        self.dynamic = 0
        self.collision_warning_multiplier = (0, 1)
        self.gear = 0
        self.rpm = 0
        self.brake = 0
        self.throttle = 0
        self.clutch = 0
        self.fuel = 0
        self.turbo = 0
        self.control_mode = 0  # 0 = Mouse, 1 = Keyboard, 2 = Joystick
        self.gearbox_mode = 0  # 0 = Auto, 1 = Shifter, 2 = Sequential
        # Database Data
        self.fuel_capacity = -1
        self.redline = -1
        self.max_gears = -1

        self.indicator_left = False
        self.indicator_right = False
        self.indicator_hazard = False
        self.auto_clutch = False
        self.battery_light = False
        self.oil_light = False
        self.abs_light = False
        self.handbrake_light = False
        self.tc_light = False
        self.full_beam_light = False
        self.engine_light = False
        self.low_beam_light = False

        self.player_name = ""
        self.cname = ""
        self.roleplay = "civil"
        self.eng_type = "combutstion"  # combustion, electric

        self.acc_active = False

        self.is_bus = False

    def update_dynamic(self, dynamic):
        self.dynamic = dynamic

    def update_distance(self, own_x, own_y, own_z):
        a = (own_x, own_y, own_z)
        b = (self.x, self.y, self.z)
        self.distance = (math.sqrt(
            (b[0] - a[0]) * (b[0] - a[0]) + (b[1] - a[1]) * (b[1] - a[1]) + (b[2] - a[2]) * (b[2] - a[2])) / 65536)

    def update_data(self, x, y, z, heading, direction, steer_forces, speed, player_id):
        self.x = x
        self.y = y
        self.z = z
        self.heading = heading
        self.direction = direction
        self.steer_forces = steer_forces
        self.speed_mci = speed
        self.player_id = player_id

    def update_cname(self, cn):
        self.cname = cn
