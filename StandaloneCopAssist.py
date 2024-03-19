import pyinsim


class CopAssist:
    def __init__(self):
        self.started = False
        self.siren = False
        self.siren_fast = False
        self.strobe = False

        self.use_extra_light = True
        self.use_indicators = True
        self.use_light = True
        self.use_fog_light = True

        self.strobe_cycle = 0
        self.insim = pyinsim.insim(b'127.0.0.1', 29999, Admin=b'', Flags=pyinsim.ISF_MCI, Interval=200)

    def strobe_func(self):
        if self.strobe_cycle == 0:
            self.strobe_cycle = 1
            if self.use_extra_light:
                self.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL,
                                UVal=pyinsim.LCL_SET_EXTRA | pyinsim.LCL_Mask_Extra)
            if self.use_indicators:
                self.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL,
                                UVal=pyinsim.LCL_SET_SIGNALS | pyinsim.LCL_Mask_Left)
            if self.use_light:
                self.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL, UVal=pyinsim.LCL_SET_LIGHTS)
        elif self.strobe_cycle == 1:
            self.strobe_cycle = 2
            if self.use_indicators:
                self.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL,
                                UVal=pyinsim.LCL_SET_SIGNALS | pyinsim.LCL_Mask_Right)
            if self.use_fog_light:
                self.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL,
                                UVal=pyinsim.LCL_SET_FOG_REAR | pyinsim.LCL_Mask_FogRear)
                self.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL,
                                UVal=pyinsim.LCL_SET_FOG_FRONT)
        elif self.strobe_cycle == 2:
            self.strobe_cycle = 3
            if self.use_extra_light:
                self.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL, UVal=pyinsim.LCL_SET_EXTRA)
            if self.use_indicators:
                self.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL, UVal=pyinsim.LCL_SET_SIGNALS)
            if self.use_light:
                self.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL,
                                UVal=pyinsim.LCL_SET_LIGHTS | pyinsim.LCL_Mask_HighBeam)
        elif self.strobe_cycle == 3:
            self.strobe_cycle = 0
            if self.use_light:
                self.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL, UVal=pyinsim.LCL_SET_LIGHTS)
            if self.use_fog_light:
                self.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL,
                                UVal=pyinsim.LCL_SET_FOG_REAR)
                self.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL,
                                UVal=pyinsim.LCL_SET_FOG_FRONT | pyinsim.LCL_Mask_FogFront)

    def stop_strobe(self):
        self.strobe = False
        if self.use_extra_light:
            self.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL, UVal=pyinsim.LCL_SET_EXTRA)
        if self.use_indicators:
            self.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL, UVal=pyinsim.LCL_SET_SIGNALS)
        if self.use_light:
            self.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL, UVal=pyinsim.LCL_SET_LIGHTS)
        if self.use_fog_light:
            self.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL, UVal=pyinsim.LCL_SET_FOG_REAR)
            self.insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL, UVal=pyinsim.LCL_SET_FOG_FRONT)

    def stop_siren(self):
        self.insim.send(pyinsim.ISP_MST, Msg=b"/siren off")

    def start_siren(self):
        self.insim.send(pyinsim.ISP_MST, Msg=b"/siren slow")

    def toggle_siren(self):
        self.siren = not self.siren
        if not self.siren:
            self.stop_siren()
        else:
            self.start_siren()
            self.strobe = True
        self.send_buttons()

    def toggle_strobe(self):
        self.strobe = not self.strobe
        if not self.strobe:
            self.stop_strobe()
            self.siren = False
            self.stop_siren()
        self.send_buttons()

    def send_buttons(self):
        self.send_button(1, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 100, 0, 12, 5,
                         "^4Strobe" if self.strobe else "Strobe")
        self.send_button(2, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 105, 0, 12, 5,
                         "^4Siren" if self.siren else "Siren")
    def get_car_data(self, insim, mci):
        if not self.started:
            self.started = True
            self.send_buttons()
            self.insim.send(pyinsim.ISP_MSL, Msg=b"Type '/o siren' or '/o strobe' to toggle siren or strobe.")

        if self.strobe:
            self.strobe_func()

    def button_click(self, insim, btc):
        if btc.ClickID == 1:
            self.toggle_strobe()
        elif btc.ClickID == 2:
            self.toggle_siren()

    def send_button(self, click_id, style, t, l, w, h, text, inst=0, typeIn=0):
        """
        This method checks if a button is already on the screen and if not, it sends a new button to LFS.
        It makes sending buttons easier than always sending the entire thing to lfs.
        """
        if type(text) == str:
            text = text.encode()
        self.insim.send(
            pyinsim.ISP_BTN,
            ReqI=255,
            ClickID=click_id,
            BStyle=style | 3,
            Inst=inst,
            T=t,
            L=l,
            W=w,
            H=h,
            Text=text,
            TypeIn=typeIn)

    def message_handling(self, insim, mso):
        if mso.Msg == b'siren':
            self.toggle_siren()
        elif mso.Msg == b'strobe':
            self.toggle_strobe()

    def run(self):
        self.insim.bind(pyinsim.ISP_MCI, self.get_car_data)
        self.insim.bind(pyinsim.ISP_BTC, self.button_click)
        self.insim.bind(pyinsim.ISP_MSO, self.message_handling)

        pyinsim.run()
        # Example in Test.py


if __name__ == "__main__":
    Strobe = CopAssist()
    Strobe.run()
