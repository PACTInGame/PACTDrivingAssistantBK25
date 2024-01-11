import pyinsim


class CopAssist:
    def __init__(self, game_object):
        self.game_object = game_object
        self.siren = False
        self.strobe = True

        self.use_indicators = True
        self.use_light = True
        self.use_extra_light = True
        self.use_fog_light = True

        self.strobe_cycle = 0

    def strobe_func(self):
        if self.strobe_cycle == 0:
            self.strobe_cycle = 1
            if self.use_extra_light:
                self.game_object.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL,
                                            UVal=pyinsim.LCL_SET_EXTRA | pyinsim.LCL_Mask_Extra)
            if self.use_indicators:
                self.game_object.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL,
                                            UVal=pyinsim.LCL_SET_SIGNALS | pyinsim.LCL_Mask_Left)
            if self.use_light:
                self.game_object.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL, UVal=pyinsim.LCL_SET_LIGHTS)
        elif self.strobe_cycle == 1:
            self.strobe_cycle = 2
            if self.use_indicators:
                self.game_object.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL,
                                            UVal=pyinsim.LCL_SET_SIGNALS | pyinsim.LCL_Mask_Right)
            if self.use_fog_light:
                self.game_object.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL,
                                            UVal=pyinsim.LCL_SET_FOG_REAR | pyinsim.LCL_Mask_FogRear)
                self.game_object.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL,
                                            UVal=pyinsim.LCL_SET_FOG_FRONT)
        elif self.strobe_cycle == 2:
            self.strobe_cycle = 3
            if self.use_extra_light:
                self.game_object.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL, UVal=pyinsim.LCL_SET_EXTRA)
            if self.use_indicators:
                self.game_object.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL, UVal=pyinsim.LCL_SET_SIGNALS)
            if self.use_light:
                self.game_object.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL,
                                            UVal=pyinsim.LCL_SET_LIGHTS | pyinsim.LCL_Mask_HighBeam)
        elif self.strobe_cycle == 3:
            self.strobe_cycle = 0
            if self.use_light:
                self.game_object.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL, UVal=pyinsim.LCL_SET_LIGHTS)
            if self.use_fog_light:
                self.game_object.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL,
                                            UVal=pyinsim.LCL_SET_FOG_REAR)
                self.game_object.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL,
                                            UVal=pyinsim.LCL_SET_FOG_FRONT | pyinsim.LCL_Mask_FogFront)

    def stop_strobe(self):
        self.strobe = False
        if self.use_extra_light:
            self.game_object.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL, UVal=pyinsim.LCL_SET_EXTRA)
        if self.use_indicators:
            self.game_object.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL, UVal=pyinsim.LCL_SET_SIGNALS)
        if self.use_light:
            self.game_object.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL, UVal=pyinsim.LCL_SET_LIGHTS)
        if self.use_fog_light:
            self.game_object.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL, UVal=pyinsim.LCL_SET_FOG_REAR)
            self.game_object.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL, UVal=pyinsim.LCL_SET_FOG_FRONT)

    def run(self):
        # Example in Test.py
        if self.strobe:
            self.strobe_func()
