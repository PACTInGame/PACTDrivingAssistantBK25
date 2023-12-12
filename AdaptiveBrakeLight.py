import pyinsim


class AdaptiveBrakeLight:
    def __init__(self, game_obj):
        self.game_obj = game_obj
        self.braking = False
        self.stopped = False
        self.cycle = 0
        self.setting = self.game_obj.settings.adaptive_brake_light_style
        self.speed = self.game_obj.own_vehicle.speed
        self.brake = self.game_obj.own_vehicle.brake

    def update(self):
        self.setting = self.game_obj.settings.adaptive_brake_light_style
        self.speed = self.game_obj.own_vehicle.speed
        self.brake = self.game_obj.own_vehicle.brake
        if self.brake > 0.9 and self.speed > 10:
            self.braking = True
        elif self.brake < 0.9 and self.speed > 10:
            self.braking = False
            self.stopped = False
            self.game_obj.insim.send(pyinsim.ISP_MST, Msg=b"/press 0")
        elif self.braking and self.speed < 10:
            self.stopped = True
            self.braking = False
            self.game_obj.insim.send(pyinsim.ISP_MST, Msg=b"/press 9")
        elif self.stopped and self.speed > 10:
            self.stopped = False
            self.game_obj.insim.send(pyinsim.ISP_MST, Msg=b"/press 0")

        if self.braking:
            self.flash()

    def flash(self):
        if self.setting:
            if self.cycle == 0:
                self.cycle = 1
                self.game_obj.insim.send(pyinsim.ISP_MST, Msg=b"/press 9")
            else:
                self.cycle = 0
                self.game_obj.insim.send(pyinsim.ISP_MST, Msg=b"/press 0")
        else:
            self.game_obj.insim.send(pyinsim.ISP_MST, Msg=b"/press 3")
