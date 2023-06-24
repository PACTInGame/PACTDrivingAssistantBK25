import pyinsim


class LFSConnection:
    def __init__(self):
        self.insim = pyinsim.insim(b'127.0.0.1', 29999, Admin=b'', Prefix=b"$",
                      Flags=pyinsim.ISF_MCI | pyinsim.ISF_LOCAL, Interval=200)
        self.outgauge = pyinsim.outgauge('127.0.0.1', 30000, outgauge_packet, 30.0)
        self.players = {}
        self.cars_on_track = []
        self.cars_relevant = []