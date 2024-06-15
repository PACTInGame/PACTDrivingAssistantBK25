import pyinsim

try:
    from vjoy import vj, setJoy
except:
    print("ERROR LOADING VJOY. VJOY IS MANDATORY FOR AUTO-BRAKE WITH CONTROLLER.")


class WheelSupport:
    def __init__(self, game_obj):
        self.game_obj = game_obj
        self.accelerator = 1000
        self.brake = 1000
        self.steer = 0
        self.wanted_brake = -800
        try:
            vj.open()
            vj.close()
            self.vjoy_available = True
        except:
            self.vjoy_available = False

    def use(self):
        if self.vjoy_available:
            vj.open()

            # valueX(brake), valueY(throttle) between -1000 and 1000, 1000 = 0%, -1000 = 100%
            # scale between 0 and 16000

            scale = 16.39
            xPos = self.accelerator + 23
            yPos = self.brake + 23
            zPos = self.steer + 23
            setJoy(xPos, yPos, zPos, scale)
            vj.close()

    def use_wheel_collision_warning(self, game_obj):
        self.brake = 200*game_obj.collision_warning_brake_force + 1000
        self.accelerator = 1000
        self.use()
        game_obj.insim.send(pyinsim.ISP_MST,
                            Msg=b"/axis %.1i brake" % game_obj.settings.VJOY_AXIS1)
        game_obj.insim.send(pyinsim.ISP_MST,
                            Msg=b"/axis %.1i throttle" % game_obj.settings.VJOY_AXIS)

    def use_wheel_stop(self, game_obj):

        game_obj.insim.send(pyinsim.ISP_MST,
                            Msg=b"/axis %.1i brake" % game_obj.settings.BRAKE_AXIS)
        game_obj.insim.send(pyinsim.ISP_MST,
                            Msg=b"/axis %.1i throttle" % game_obj.settings.THROTTLE_AXIS)

    def use_wheel(self, game_obj, accel, brake):
        self.accelerator = accel
        self.brake = brake
        self.use()
        game_obj.insim.send(pyinsim.ISP_MST,
                            Msg=b"/axis %.1i brake" % game_obj.settings.VJOY_AXIS1)
        game_obj.insim.send(pyinsim.ISP_MST,
                            Msg=b"/axis %.1i throttle" % game_obj.settings.VJOY_AXIS)

    def use_wheel_psc(self, game_obj, accel, brake):
        self.brake = brake
        self.accelerator = accel
        self.use()
        game_obj.insim.send(pyinsim.ISP_MST,
                            Msg=b"/axis %.1i throttle" % game_obj.settings.VJOY_AXIS)
        game_obj.insim.send(pyinsim.ISP_MST,
                            Msg=b"/axis %.1i brake" % game_obj.settings.VJOY_AXIS1)
