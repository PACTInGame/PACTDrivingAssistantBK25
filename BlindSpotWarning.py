from shapely import Polygon

import SideCollisionPrevention
from Calculations import calc_polygon_points, polygon_intersect


def create_rectangles_for_blindspot_warning(cars):
    rectangles = []
    factor = 2.3 * 65536
    heading_offset = 16384
    heading_divisor = 182.05
    angle_offsets = [22, 158, 202, 338]

    for car in cars:
        x, y, heading = car[0].x, car[0].y, car[0].heading
        angle_of_car = abs((heading - heading_offset) / heading_divisor)
        polygon_points = [calc_polygon_points(x, y, factor, angle_of_car + offset) for offset in angle_offsets]
        rectangles.append((car[0].speed, car[0].distance, Polygon(polygon_points), heading))

    return rectangles


def check_blindspots(game_object):
    cars = game_object.cars_relevant
    own_x = game_object.own_vehicle.x
    own_y = game_object.own_vehicle.y
    own_heading = game_object.own_vehicle.heading
    own_speed = game_object.own_vehicle.speed

    blindspot_r = False
    blindspot_l = False
    angle_of_car = (own_heading + 16384) / 182.05
    if angle_of_car < 0:
        angle_of_car *= -1
    ang1 = angle_of_car + 270
    ang2 = angle_of_car + 182
    ang3 = angle_of_car + 183
    ang4 = angle_of_car + 270
    ang5 = angle_of_car + 90
    ang6 = angle_of_car + 178
    ang7 = angle_of_car + 177
    ang8 = angle_of_car + 90
    # blind spot right checker
    (x1, y1) = calc_polygon_points(own_x, own_y, 4 * 65536, ang1)  # front left
    (x2, y2) = calc_polygon_points(own_x, own_y, 85 * 65536, ang2)  # rear left
    (x3, y3) = calc_polygon_points(own_x, own_y, 85 * 65536, ang3)  # rear right
    (x4, y4) = calc_polygon_points(own_x, own_y, 1 * 65536, ang4)  # front right
    (x5, y5) = calc_polygon_points(own_x, own_y, 4 * 65536, ang5)  # front left
    (x6, y6) = calc_polygon_points(own_x, own_y, 85 * 65536, ang6)  # rear left
    (x7, y7) = calc_polygon_points(own_x, own_y, 85 * 65536, ang7)  # rear right
    (x8, y8) = calc_polygon_points(own_x, own_y, 1 * 65536, ang8)  # front right

    rectangle_right = Polygon([(x1, y1), (x2, y2), (x3, y3), (x4, y4)])
    rectangle_left = Polygon([(x5, y5), (x6, y6), (x7, y7), (x8, y8)])
    rectangles_others = create_rectangles_for_blindspot_warning(cars)

    for i, rectangle in enumerate(rectangles_others):
        ok = False
        edge = False
        if rectangle[3] + 5000 > 65536:
            heading_car_two_big = rectangle[3] - 65536 + 5000
            edge = True
        else:
            heading_car_two_big = rectangle[3] + 5000

        if rectangle[3] - 5000 < 0:
            heading_car_two_small = rectangle[3] + 65536 - 5000
            edge = True
        else:
            heading_car_two_small = rectangle[3] - 5000

        if edge:
            if own_heading > heading_car_two_small or own_heading < heading_car_two_big:
                ok = True
        else:
            if heading_car_two_small < own_heading < heading_car_two_big:
                ok = True
        speed_diff = rectangle[0] - own_speed
        if rectangle[1] < speed_diff * 1.2 and ok:
            if polygon_intersect(rectangle[2], rectangle_left):
                blindspot_l = True
            if polygon_intersect(rectangle[2], rectangle_right):
                blindspot_r = True

    return blindspot_r, blindspot_l


def check_blindspots_ref(game_object):
    cars = game_object.cars_relevant
    own_vehicle = game_object.own_vehicle

    blindspot_r, blindspot_l = False, False
    angle_of_car = normalize_angle((own_vehicle.heading + 16384) / 182.05)

    # Rectangles for right and left blind spots
    rectangle_right = create_blindspot_rectangle(own_vehicle, angle_of_car, [270, 182, 183, 270])
    rectangle_left = create_blindspot_rectangle(own_vehicle, angle_of_car, [90, 178, 177, 90])

    rectangles_others = create_rectangles_for_blindspot_warning(cars)

    for rectangle in rectangles_others:
        if is_within_threshold(own_vehicle.heading, rectangle[3]) and rectangle[1] < (
                rectangle[0] - own_vehicle.speed + (5 if own_vehicle.speed > 15 else 0)) * 1.2:
            if polygon_intersect(rectangle[2], rectangle_left):
                blindspot_l = True
            if polygon_intersect(rectangle[2], rectangle_right):
                blindspot_r = True
    sidecollision_r, sidecollision_l = SideCollisionPrevention.calculate_warning(blindspot_l, blindspot_r, game_object, rectangles_others)
    return blindspot_r, blindspot_l, sidecollision_r, sidecollision_l


def normalize_angle(angle):
    # Normalizes the angle value
    if angle < 0:
        angle *= -1
    return angle


def create_blindspot_rectangle(vehicle, angle_of_car, angles):
    # Creates blind spot rectangle using provided angles
    multipliers = [4, 85, 85, 1]
    points = [calc_polygon_points(vehicle.x, vehicle.y, multiplier * 65536, angle_of_car + angle)
              for multiplier, angle in zip(multipliers, angles)]
    return Polygon(points)


def is_within_threshold(own_heading, other_heading):
    # Checks if the heading of another car is within a threshold
    lower_bound = (other_heading - 5000) % 65536
    upper_bound = (other_heading + 5000) % 65536

    if lower_bound > upper_bound:
        return own_heading > lower_bound or own_heading < upper_bound
    return lower_bound < own_heading < upper_bound
