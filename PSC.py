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

    def calculate_max_steering(self, speed):
        y = 0.2412138 + (1158948 - 0.2412138) / (1 + (speed / 0.08339507) ** 2.472554)
        return y

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
        gear = self.game_object.own_vehicle.gear
        override = False
        understeer = False
        oversteer = False
        max_throttle = -1000
        min_braking = 1000
        own_throttle = self.game_object.controller_inputs.accelerator * -2000 + 1000
        if own_throttle < -1000:
            own_throttle = -1000
        own_braking = self.game_object.controller_inputs.brake * -2000 + 1000
        if 30 < self.speed < 110 and gear > 0:
            max_steering = self.calculate_max_steering(self.speed)
            steer_diff = abs(self.game_object.controller_inputs.steer) - max_steering
            if steer_diff > 0:
                min_braking = steer_diff * -3000 + 1000
                understeer = True
        if abs(ang_of_car) > self.oversteer_threshold and self.speed > 10 and gear > 0:
            max_throttle = -1000 + (abs(ang_of_car) - self.oversteer_threshold) * self.sensitivity
            if max_throttle > 1000:
                max_throttle = 1000
        if own_throttle < max_throttle:
            oversteer = True
        if understeer or oversteer:
            self.sent_slip = True
            # TODO display slip only in cockpit view
            if self.game_object.settings.head_up_display:
                self.game_object.send_button(41, pyinsim.ISB_DARK, 113 + x, 103 + y, 13, 6, "^3SLIP")

        elif self.sent_slip:
            self.sent_slip = False
            self.game_object.wheel_support.use_wheel_stop(self.game_object)
            self.game_object.del_button(41)

        if oversteer or own_braking > min_braking:
            override = True
            if own_throttle > max_throttle:
                max_throttle = own_throttle
            if own_braking < min_braking:
                min_braking = own_braking
        if override and not self.game_object.collision_warning_intensity > 2:
            self.overridden = True
            self.game_object.wheel_support.use_wheel_psc(self.game_object, max_throttle, min_braking)


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
