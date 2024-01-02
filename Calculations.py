import math
from shapely import Polygon


def calc_polygon_points(own_x, own_y, length, angle):
    return own_x + length * math.cos(math.radians(angle)), own_y + length * math.sin(math.radians(angle))


def create_rectangles_for_collision_warning(cars):
    rectangles = []
    conversion_factor = 65536
    offset_angle = 16384
    angle_divisor = 182.05
    distance = 2.3 * conversion_factor

    angles = [22, 158, 202, 338]

    for car in cars:
        car_heading = car[0].heading
        angle_of_car = abs((car_heading - offset_angle) / angle_divisor)

        car_x, car_y = car[0].x, car[0].y
        polygon_points = [
            calc_polygon_points(car_x, car_y, distance, angle_of_car + angle)
            for angle in angles
        ]

        rectangles.append((car, Polygon(polygon_points)))

    return rectangles


def polygon_intersect(p1, p2):
    return p1.intersects(p2)


def calculate_angle(x1, x2, y1, y2, own_heading):
    ang = (math.atan2((x2 / 65536 - x1 / 65536),
                      (y2 / 65536 - y1 / 65536)) * 180.0) / 3.1415926535897931
    if ang < 0.0:
        ang = 360.0 + ang
    consider_dir = ang + own_heading / 182
    if consider_dir > 360.0:
        consider_dir -= 360.0
    angle = consider_dir
    return angle


def get_distance(list_of_cars):
    return list_of_cars[0].distance


def calc_distance(x1, y1, x2, y2):
    # Vector length
    return math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))
