class Boardcomputer:
    def __init__(self, game_object):
        self.game_obj = game_object
        self.distance_driven_meters = 0
        self.distance_since_reset = 0
        self.range_km = -1
        self.liters_per_100km = 0
        self.percent_fuel_burned_since_reset = 0
        self.percent_fuel_at_reset = 0
        self.notified_low_fuel = False
        self.notified_critical_fuel = False
        self.last_fuel = 0

    def reset(self):
        print("reset")
        self.distance_since_reset = 0
        self.percent_fuel_burned_since_reset = 0
        self.liters_per_100km = 0
        self.percent_fuel_at_reset = self.game_obj.own_vehicle.fuel
        self.notified_low_fuel = False
        self.notified_critical_fuel = False
        self.range_km = -1

    def update(self):
        fuel = self.game_obj.own_vehicle.fuel
        add_distance = self.game_obj.own_vehicle.speed / 3.6 / 5
        self.distance_driven_meters += add_distance
        self.distance_since_reset += add_distance
        self.percent_fuel_burned_since_reset = abs(self.percent_fuel_at_reset - fuel)
        if self.distance_since_reset > 200:  # TODO increase to 1000 for release
            fuel_percent_per_km = self.percent_fuel_burned_since_reset / self.distance_since_reset * 1000
            self.range_km = fuel / fuel_percent_per_km if fuel_percent_per_km > 0 else -1
        fuel_diff = abs(self.last_fuel - fuel)
        if fuel_diff > 0.001 or self.percent_fuel_at_reset == 0:
            self.reset()
        if self.range_km < 20 and not self.notified_low_fuel and not self.range_km == -1:
            self.game_obj.notifications.append(["^3Refuel soon. Range.", 5])
            self.notified_low_fuel = True
        if self.range_km < 5 and not self.notified_critical_fuel and not self.range_km == -1:
            self.game_obj.notifications.append(["^1Refuel immediately. Range.", 5])
            self.notified_critical_fuel = True
        self.last_fuel = fuel



