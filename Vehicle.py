import math
import time


class Vehicle:
    def __init__(self, x, y, z, heading, direction, steer_forces, speed, player_id, distance, dynamic, cname):
        self.x = x
        self.y = y
        self.z = z
        self.heading = heading
        self.direction = direction
        self.steer_forces = steer_forces
        self.speed = speed
        self.player_id = player_id
        self.distance = distance
        self.dynamic = dynamic
        self.last_speed = 0
        self.last_dynamic_change = time.perf_counter()
        self.cname = cname
        self.length = 0

    def update_dynamic(self, dynamic):
        self.dynamic = dynamic

    def update_distance(self, own_x, own_y, own_z):
        a = (own_x, own_y, own_z)
        b = (self.x, self.y, self.z)
        self.distance = (math.sqrt(
            (b[0] - a[0]) * (b[0] - a[0]) + (b[1] - a[1]) * (b[1] - a[1]) + (b[2] - a[2]) * (b[2] - a[2])) / 65536)

    def update_data(self, x, y, z, heading, direction, steer_forces, speed, player_id):
        self.x = x
        self.y = y
        self.z = z
        self.heading = heading
        self.direction = direction
        self.steer_forces = steer_forces
        self.speed = speed
        self.calculate_acceleration()
        self.player_id = player_id

    def update_cname(self, cn):
        self.cname = cn

    def calculate_acceleration(self):
        zeit = time.perf_counter() - self.last_dynamic_change
        if zeit == 0:
            raise ValueError("Die Zeitspanne darf nicht null sein.")
        speed = self.speed/3.6
        acceleration = (speed - self.last_speed) / zeit
        self.last_speed = speed
        self.last_dynamic_change = time.perf_counter()
        if acceleration == 0.0 and self.speed < 0.5 or acceleration != 0.0:
            self.dynamic = acceleration
        #print(f"Beschleunigung/Verzögerung Veh2: {self.dynamic:.2f} m/s^2")
