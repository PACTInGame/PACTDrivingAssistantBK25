def get_max_gears(vehicle_model):
    vehicle_data = {
        b"FZ5": (6, 7800),
        b'\x98a\x10': (5, 2100),  # Carobus
        b'\xb6i\xbd': (7, 6300),  # Luxury Sedan
        b'K\xd2c': (6, 6700),  # UF Pickup Truck
        b'\xac\xb1\xb0': (6, 5150),  # Faik Topo
        b'*\x8f-': (6, 6700),
        b'>\x8c\x88': (5, 5600),
        b'Gb\xa7': (7, 2100),
        b'T\xe1\xec': (6, 2100)  # Bus Monoblonco
    }

    return vehicle_data.get(vehicle_model, (-1, -1))


def get_vehicle_length(own_car):
    vehicle_data = {
        b'XFG': (0, 1.1),
        b'LX4': (0, 0.9),
        b'LX6': (0, 0.9),
        b'FXO': (0, 0.9),
        b'UFR': (0, 0.85),
        b'XFR': (0, 0.85),
        b'FXR': (0, 0.8),
        b'XRR': (0, 0.8),
        b'FZR': (0, 0.8),
        b'BF1': (0, 0.7),
        b'\x98a\x10': (-5, 1.9),  # CAROBUS
        b'z\xf8p': (3, 1.3),  # LKW
        b'\xb67G': (3, 1.4),  # ONIBUS
        b'\xa4\xc2\xf3': (3, 1.3),  # Line Runner
        b'\xcf\xee\x83': (3, 1.2),  # BUS 2
        b'\xbc\xe5B': (4, 1.4),  # Reisebus
        b'x\x0b!': (0, 1.1),  # Lory GP5
        b'>\x8c\x88': (0, 1.1),  # Bumer 7
        b'=v{': (0, 1.1),  # CCF012
        b'\xac\xb1\xb0': (0, 0.95),  # FAIK TOPO
        b'K\xd2c': (1, 1),  # UF Pickup Truck
        b'*\x8f-': (1, 0.9),  # N.400s
        b'Gb\xa7': (2, 1.4)  # Town Bus
    }
    length_adjustment, brake = vehicle_data.get(own_car, (0, 1.0))
    length = 0 + length_adjustment

    return length, brake


def get_vehicle_redline(c):
    redline_dict = {
        b"UF1": 6000,
        b"XFG": 7000,
        b"XRG": 6000,
        b"LX4": 8000,
        b"LX6": 8000,
        b"RB4": 6500,
        b"FXO": 6500,
        b"XRT": 6500,
        b"RAC": 6000,
        b"FZ5": 7000,
        b'K\xd2c': 6000,  # UF Pick Up
        b'\xb4\xdf\xa6': 6000,  # Swirl
        b'\xedmj': 5100,  # TAZ09
        b'\x05\xad\xcf': 9000,  # Wessex
        b'\x81X\x95': 3200,  # SLX130
        b'\x98a\x10': 1900,  # CAROBUS
        b'z\xf8p': 3000,  # LKW
        b'\xb67G': 1900,  # ONIBUS
        b'\xa4\xc2\xf3': 3000,  # Line Runner
        b'\x0c\xb9\xfc': 5000,  # Bayern 540
        b'o\xa1%': 6000,  # EDM 540
        b'\xf6\x121': 3800,  # lemon adieu
        b']7\xd8': 6000,  # Panther
        b'\x13\x80^': 6000,  # Pinewood
        b'\xbc\xe5B': 3000,  # Reisebus
        b'*\x8f-': 6000,  # N.440S
        b'>\x8c\x88': 5000,  # Bumer 7
        b'\xbe\xa1e': 13000,
        b'?!?': 2000,  # TSV8
        b'\xcf\xee\x83': 3000,  # TSV8
        b'Gb\xa7': 2000,  # Town Bus
        b'T\xe1\xec': 2500  # Bus Monoblonco
    }

    return redline_dict.get(c, 7000)


def get_fuel_capa(car):
    fuel_capacity_map = {
        b'UF1': 35,
        b'XFG': 45,
        b'XRG': 65,
        b'LX4': 40,
        b'LX6': 40,
        b'RB4': 75,
        b'FXO': 75,
        b'XRT': 75,
        b'RAC': 42,
        b'FZ5': 90,
        b'_\x1d*': 90,
        b'\xeb\xce9': 90,
        b'4\x96\xde': 90,  # FZ5 Lightbar, Safetycar, FZ5 Turbo
        b'UFR': 60,
        b'XFR': 70,
        b'FXR': 100,
        b'XRR': 100,
        b'FZR': 100,
        b'\x98a\x10': 240,  # CAROBUS
        b'\xb6i\xbd': 66,
        b'\xa5\x90\xc6': 66,  # Luxury Sedan, SV
        b'K\xd2c': 137,  # UF Pickup Truck
        b'\xac\xb1\xb0': 50,  # Faik Topo
        b'*\x8f-': 71,  # N.440S
        b'>\x8c\x88': 95,  # Bumer 7
        b'\xbe\xa1e': 48,  # XFG E
        b'\n\xe8\x9e': 78.7,
        b'\xaah\x1a': 78.7,  # FEND BR
        b'\x85\xc4\xa4': 30,  # Chorus Attendanze
        b'\xfa\xae\xe2': 75,  # ETK - K series
        b'\xb7\x83K': 38,  # UF Electric (Note: Duplicate key '\xb7\x83K' removed)
        b'6=j': 50,  # Tiny Cupe
        b'\xce\xd9v': 65,
        b'\x13>\xcb': 65,  # GT V-34, God foot
        b'H1`': 75,
        b'J\x08\xc8': 75,  # Bimmy M46, BZG SUV
        b'\xfa5\xe7': 50,  # XFG YARIS
        b'Z\x1f\x80': 300,  # MUN Firetruck
        b'\xcd\x87U': 73,  # Adda Ar-Eight
        b'\xd6\x11n': 70,  # Frerri F90
        b'R\xea/': 53,  # XR E-GT
        b'?!?': 381.9,  # TSV8
        b'\xcf\xee\x83': 200,  # RTS 6-71
        b'z\xf8p': 100,  # LCT 300
        b'\x89)\xfa': 57,  # E-Challenger
        b'\xdc\xb8\xb7': 40,  # Formula XR-E
        b'BF1': 95,
        b'\xf1\xf13': 59,  # Bavaria A20
        b'Gb\xa7': 295.9,  # Town Bus
        b'T\xe1\xec': 300  # Bus Monoblonco
    }

    return fuel_capacity_map.get(car, -1)

def get_size(cn):
    size_map = {
        b'\x98a\x10': (11.2, 2.75),  # Karobus
        b'\xb6i\xbd': (5.1, 2),  # Luxury sedan
        b'UF1': (3.1, 1.6),
        b'XFG': (3.7, 1.7),
        b'XRG': (4.5, 1.8),
        b'LX4': (4.5, 1.8),
        b'LX6': (4.5, 1.9),
        b'RB4': (4.5, 1.9),
        b'FXO': (4.5, 1.9),
        b'XRT': (4.5, 1.9),
        b'RAC': (5.0, 1.9),
        b'FZ5': (5.0, 1.9),
        b'UFR': (3.7, 1.8),
        b'XFR': (4.2, 1.9),
        b'FXR': (5.0, 1.9),
        b'XRR': (5.0, 1.9),
        b'FZR': (5.0, 1.9),
        b'>\x8c\x88': (5.2, 1.9),  # bumer 7
        b'K\xd2c': (5.2, 2.2),  # Uf Pickup
        b'\xa4\xc2\xf3': (7.6, 2.3),  # Line Runner
        b'\xe3\x94\xf4': (13.5, 2.5),  # SCAMA K460
    }

    return size_map.get(cn, (4.8, 2))