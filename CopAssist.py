import pyinsim


class CopAssist:
    def __init__(self, game_object):
        self.game_object = game_object
        self.siren = False
        self.siren_fast = False
        self.strobe = False

        self.strobe_cycle = 0

    def strobe_func(self):
        if self.strobe_cycle == 0:
            self.strobe_cycle = 1
            if self.game_object.settings.use_extra_light:
                self.game_object.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL,
                                            UVal=pyinsim.LCL_SET_EXTRA | pyinsim.LCL_Mask_Extra)
            if self.game_object.settings.use_indicators:
                self.game_object.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL,
                                            UVal=pyinsim.LCL_SET_SIGNALS | pyinsim.LCL_Mask_Left)
            if self.game_object.settings.use_light:
                self.game_object.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL, UVal=pyinsim.LCL_SET_LIGHTS)
        elif self.strobe_cycle == 1:
            self.strobe_cycle = 2
            if self.game_object.settings.use_indicators:
                self.game_object.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL,
                                            UVal=pyinsim.LCL_SET_SIGNALS | pyinsim.LCL_Mask_Right)
            if self.game_object.settings.use_fog_light:
                self.game_object.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL,
                                            UVal=pyinsim.LCL_SET_FOG_REAR | pyinsim.LCL_Mask_FogRear)
                self.game_object.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL,
                                            UVal=pyinsim.LCL_SET_FOG_FRONT)
        elif self.strobe_cycle == 2:
            self.strobe_cycle = 3
            if self.game_object.settings.use_extra_light:
                self.game_object.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL, UVal=pyinsim.LCL_SET_EXTRA)
            if self.game_object.settings.use_indicators:
                self.game_object.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL, UVal=pyinsim.LCL_SET_SIGNALS)
            if self.game_object.settings.use_light:
                self.game_object.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL,
                                            UVal=pyinsim.LCL_SET_LIGHTS | pyinsim.LCL_Mask_HighBeam)
        elif self.strobe_cycle == 3:
            self.strobe_cycle = 0
            if self.game_object.settings.use_light:
                self.game_object.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL, UVal=pyinsim.LCL_SET_LIGHTS)
            if self.game_object.settings.use_fog_light:
                self.game_object.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL,
                                            UVal=pyinsim.LCL_SET_FOG_REAR)
                self.game_object.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL,
                                            UVal=pyinsim.LCL_SET_FOG_FRONT | pyinsim.LCL_Mask_FogFront)

    def stop_strobe(self):
        self.strobe = False
        if self.game_object.settings.use_extra_light:
            self.game_object.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL, UVal=pyinsim.LCL_SET_EXTRA)
        if self.game_object.settings.use_indicators:
            self.game_object.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL, UVal=pyinsim.LCL_SET_SIGNALS)
        if self.game_object.settings.use_light:
            self.game_object.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL, UVal=pyinsim.LCL_SET_LIGHTS)
        if self.game_object.settings.use_fog_light:
            self.game_object.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL, UVal=pyinsim.LCL_SET_FOG_REAR)
            self.game_object.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL, UVal=pyinsim.LCL_SET_FOG_FRONT)

    def stop_siren(self):
        self.game_object.insim.send(pyinsim.ISP_MST, Msg=b"/siren off")

    def start_siren(self):
        self.game_object.insim.send(pyinsim.ISP_MST, Msg=b"/siren slow")

    def toggle_siren(self):
        self.siren = not self.siren
        if not self.siren:
            self.stop_siren()
        else:
            self.start_siren()
            self.strobe = True

    def toggle_strobe(self):
        self.strobe = not self.strobe
        if not self.strobe:
            self.stop_strobe()

    def run(self):
        # Example in Test.py
        if self.strobe:
            self.strobe_func()
