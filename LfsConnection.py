class LFSConnection:
    def __init__(self):
        self.insim = pyinsim.insim(b'127.0.0.1', 29999, Admin=b'', Prefix=b"$",
                      Flags=pyinsim.ISF_MCI | pyinsim.ISF_LOCAL, Interval=200)