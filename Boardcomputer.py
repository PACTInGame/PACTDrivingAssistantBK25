class Boardcomputer:
    def __init__(self, game_object):
        self.game_obj = game_object
        self.distance_driven_meters = 0
        self.distance_since_reset = 0
        self.range_km = 0
        self.liters_per_100km = 0
        self.percent_fuel_burned_since_reset = 0
        self.percent_fuel_at_reset = 0

    def reset(self):
        self.distance_since_reset = 0
        self.percent_fuel_burned_since_reset = 0
        self.liters_per_100km = 0
        self.percent_fuel_at_reset = self.game_obj.own_vehicle.fuel

    def update(self):
        fuel = self.game_obj.own_vehicle.fuel
        add_distance = self.game_obj.own_vehicle.speed / 3.6 / 5
        self.distance_driven_meters += add_distance
        self.distance_since_reset += add_distance
        self.percent_fuel_burned_since_reset = abs(self.percent_fuel_at_reset - fuel)
        if self.distance_since_reset > 200:
            fuel_percent_per_km = self.percent_fuel_burned_since_reset / self.distance_since_reset * 1000
            self.range_km = fuel / fuel_percent_per_km

        if self.percent_fuel_at_reset < fuel or self.percent_fuel_at_reset == 0:
            self.reset()

        print(self.distance_since_reset)
        print("fuel burned", self.percent_fuel_burned_since_reset)
        print("Fuel at reset", self.percent_fuel_at_reset)
        print(self.range_km)

