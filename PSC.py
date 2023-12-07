import pyinsim


class PSC:
    def __init__(self, game_object):
        self.game_object = game_object
        self.heading = 0
        self.direction = 0
        self.speed = 0
        self.ang_vel = 0
        self.acceleration = 0
        self.braking = 0
        self.oversteer_threshold = 500
        self.sensitivity = 1
        self.sent_slip = False
        self.overridden = False

    def update_data(self):
        self.heading = self.game_object.own_vehicle.heading
        self.direction = self.game_object.own_vehicle.direction
        self.speed = self.game_object.own_vehicle.speed
        self.ang_vel = self.game_object.own_vehicle.steer_forces
        self.acceleration = self.game_object.own_vehicle.throttle
        self.braking = self.game_object.own_vehicle.brake

    def calculate_psc(self):
        self.update_data()
        ang_of_car = self.circular_difference(self.heading, self.direction)

        x = self.game_object.settings.offset_w
        y = self.game_object.settings.offset_h
        override = False
        if abs(ang_of_car) > self.oversteer_threshold and self.speed > 10 and self.game_object.own_vehicle.gear > 0:
            self.sent_slip = True
            if self.game_object.settings.head_up_display:
                self.game_object.send_button(41, pyinsim.ISB_DARK, 113 + x, 103 + y, 13, 6, "^3SLIP")
            max_throttle = -1000 + (abs(ang_of_car) - self.oversteer_threshold) * self.sensitivity
            own_throttle = self.game_object.own_vehicle.throttle * -2000 + 1000
            if own_throttle < max_throttle:
                override = True
            if override and not self.game_object.collision_warning_intensity > 2:
                self.overridden = True
                self.game_object.wheel_support.use_wheel_psc(self.game_object, max_throttle)
            elif self.overridden:
                self.game_object.wheel_support.use_wheel_stop(self.game_object)
        elif self.sent_slip:
            self.sent_slip = False
            self.game_object.del_button(41)

    def circular_difference(self, a, b, max_value=65536):
        """
        Calculate the difference between two values on a circle.

        :param a: First value.
        :param b: Second value.
        :param max_value: Maximum value on the circle (exclusive). Default is 65536.
        :return: Circular difference between a and b.
        """
        diff = (a - b) % max_value
        if diff > max_value / 2:
            diff -= max_value
        return diff
