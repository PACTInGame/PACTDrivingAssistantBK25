import math
import time

from shapely import Polygon

import Calculations
import Sounds
import pyinsim
from CarDataBase import get_size


def calc_polygon_points(own_x, own_y, length, angle):
    return own_x + length * math.cos(math.radians(angle)), own_y + length * math.sin(math.radians(angle))


def refactor_angle(angle):
    if angle > 360:
        return angle - 360
    else:
        return angle


def sensors(game_obj):
    cars = game_obj.cars_relevant
    own_x = game_obj.own_vehicle.x
    own_y = game_obj.own_vehicle.y
    own_heading = game_obj.own_vehicle.heading
    model = game_obj.own_vehicle.cname
    rect_obj = game_obj.rect_obj
    sensordata = []
    closest_distance = 4
    angle = 0
    angle_of_car = abs((own_heading - 16384) / 182.05)
    length, width = get_size(model)
    coeff = 65536

    a1 = math.degrees(math.atan((width / 2) / (length / 2)))
    angles = [refactor_angle(angle_of_car + a) for a in [a1, 180 - a1, 180 + a1, 360 - a1]]

    diagonal = math.sqrt((length / 2) ** 2 + (width / 2) ** 2)
    distances = [(diagonal + i) * coeff for i in range(4)]

    polygons = [Polygon([calc_polygon_points(own_x, own_y, d, angle) for angle in angles]) for d in distances]

    rectangles_others = create_rectangles_for_others(cars)
    rectangles_others.extend(rect_obj)
    for rectangle in rectangles_others:
        closest_distance = 4
        for i, poly in enumerate(polygons):
            if Calculations.polygon_intersect(rectangle[1], poly) and closest_distance > i:
                closest_distance = i

                angle = rectangle[0] if isinstance(rectangle[0], float) else Calculations.calculate_angle(own_x,
                                                                                                          rectangle[0][
                                                                                                              0],
                                                                                                          own_y,
                                                                                                          rectangle[0][
                                                                                                              1],
                                                                                                          own_heading)
        sensordata.append((closest_distance, angle))

    return sensordata


def create_rectangles_for_others(cars):
    rectangles = []
    coeff = 65536

    def calc_polygon_point(x, y, distance, angle):
        x_new = x + distance * math.cos(math.radians(angle))
        y_new = y + distance * math.sin(math.radians(angle))
        return x_new, y_new

    for car in cars:
        angle_of_car = (car[0].heading - 16384) / 182.05
        angle_of_car = abs(angle_of_car)
        length, width = get_size(car[0].cname)

        a1 = math.degrees(math.atan((width / 2) / (length / 2)))
        ang1, ang2, ang3, ang4 = angle_of_car + a1, angle_of_car + (180 - a1), angle_of_car + (
                180 + a1), angle_of_car + (360 - a1)

        diagonal = math.sqrt((length / 2) ** 2 + (width / 2) ** 2) + 0.1
        distance = diagonal * coeff
        corners = [calc_polygon_point(car[0].x, car[0].y, distance, angle) for angle in [ang1, ang2, ang3, ang4]]

        rectangles.append((car[1], Polygon(corners)))

    return rectangles


def draw_pdc_buttons(game_obj, sensors):
    # Num 48-54
    x = game_obj.settings.offset_h
    y = game_obj.settings.offset_w
    c1 = b"^7"
    c2 = b"^7"
    c3 = b"^7"
    c4 = b"^7"
    c5 = b"^7"
    c6 = b"^7"
    front_beep = 0
    rear_beep = 0
    for sensor in sensors:
        if sensor[1] > 320 or sensor[1] < 40:
            if sensor[0] == 3 and not c1 == "^2" and not c1 == "^3" and not c1 == "^1":
                c1 = b"^6"
            elif sensor[0] == 2 and not c1 == "^3" and not c1 == "^1":
                c1 = b"^2"
                front_beep = 1 if front_beep < 1 else front_beep
            elif sensor[0] == 1 and not c1 == "^1":
                c1 = b"^3"
                front_beep = 2 if front_beep < 2 else front_beep
            elif sensor[0] == 0:
                c1 = b"^1"
                front_beep = 3 if front_beep < 3 else front_beep
        if 0 < sensor[1] < 60 or sensor[1] > 350:
            if sensor[0] == 3 and not c2 == "^2" and not c2 == "^3" and not c2 == "^1":
                c2 = b"^6"
            elif sensor[0] == 2 and not c2 == "^3" and not c2 == "^1":
                c2 = b"^2"
                front_beep = 1 if front_beep < 1 else front_beep
            elif sensor[0] == 1 and not c2 == "^1":
                c2 = b"^3"
                front_beep = 2 if front_beep < 2 else front_beep
            elif sensor[0] == 0:
                c2 = b"^1"
                front_beep = 3 if front_beep < 3 else front_beep
        if 120 < sensor[1] < 190:
            if sensor[0] == 3 and not c3 == "^2" and not c3 == "^3" and not c3 == "^1":
                c3 = b"^6"
            elif sensor[0] == 2 and not c3 == "^3" and not c3 == "^1":
                c3 = b"^2"
                rear_beep = 1 if rear_beep < 1 else rear_beep
            elif sensor[0] == 1 and not c3 == "^1":
                c3 = b"^3"
                rear_beep = 2 if rear_beep < 2 else rear_beep
            elif sensor[0] == 0:
                c3 = b"^1"
                rear_beep = 3 if rear_beep < 3 else rear_beep
        if 140 < sensor[1] < 220:
            if sensor[0] == 3 and not c4 == "^2" and not c4 == "^3" and not c4 == "^1":
                c4 = b"^6"
            elif sensor[0] == 2 and not c4 == "^3" and not c4 == "^1":
                c4 = b"^2"
                rear_beep = 1 if rear_beep < 1 else rear_beep
            elif sensor[0] == 1 and not c4 == "^1":
                c4 = b"^3"
                rear_beep = 2 if rear_beep < 2 else rear_beep
            elif sensor[0] == 0:
                c4 = b"^1"
                rear_beep = 3 if rear_beep < 3 else rear_beep
        if 170 < sensor[1] < 240:
            if sensor[0] == 3 and not c5 == "^2" and not c5 == "^3" and not c5 == "^1":
                c5 = b"^6"
            elif sensor[0] == 2 and not c5 == "^3" and not c5 == "^1":
                c5 = b"^2"
                rear_beep = 1 if rear_beep < 1 else rear_beep
            elif sensor[0] == 1 and not c5 == "^1":
                c5 = b"^3"
                rear_beep = 2 if rear_beep < 2 else rear_beep
            elif sensor[0] == 0:
                c5 = b"^1"
                rear_beep = 3 if rear_beep < 3 else rear_beep
        if 300 < sensor[1] < 360 or sensor[1] < 10:
            if sensor[0] == 3 and not c6 == "^2" and not c6 == "^3" and not c6 == "^1":
                c6 = b"^6"
            elif sensor[0] == 2 and not c6 == "^3" and not c6 == "^1":
                c6 = b"^2"
                front_beep = 1 if front_beep < 1 else front_beep
            elif sensor[0] == 1 and not c6 == "^1":
                c6 = b"^3"
                front_beep = 2 if front_beep < 2 else front_beep
            elif sensor[0] == 0:
                c6 = b"^1"
                front_beep = 3 if front_beep < 3 else front_beep
    game_obj.send_button(48, pyinsim.ISB_LMB, 110 + x, 120 + y, 5, 5, c6 + b'^J\x84\xac')
    game_obj.send_button(49, pyinsim.ISB_LMB, 110 + x, 123 + y, 5, 5, c1 + b'^J\x84\xaa')
    game_obj.send_button(50, pyinsim.ISB_LMB, 110 + x, 126 + y, 5, 5, c2 + b'^J\x84\xad')
    game_obj.send_button(51, pyinsim.ISB_LMB, 125 + x, 120 + y, 5, 5, c5 + b'^J\x84\xaf')
    game_obj.send_button(52, pyinsim.ISB_LMB, 125 + x, 123 + y, 5, 5, c4 + b'^J\x84\xaa')
    game_obj.send_button(53, pyinsim.ISB_LMB, 125 + x, 126 + y, 5, 5, c3 + b'^J\x84\xae')
    game_obj.send_button(54, pyinsim.ISB_LMB, 117 + x, 120 + y, 11, 5, b'^J\x81\xe1P\x81\xe2')
    game_obj.front_beep = front_beep
    game_obj.rear_beep = rear_beep


def beep(game_obj):
    timer = time.perf_counter()
    print("started")
    while not (game_obj.front_beep == 0 and game_obj.rear_beep == 0):
        print(game_obj.rear_beep)
        if game_obj.front_beep == 1:
            if timer < time.perf_counter() - 0.6:
                Sounds.pdc_front()
                timer = time.perf_counter()
        elif game_obj.front_beep == 2:
            if timer < time.perf_counter() - 0.4:
                Sounds.pdc_front()
                timer = time.perf_counter()
        elif game_obj.front_beep == 3:
            if timer < time.perf_counter() - 0.2:
                Sounds.pdc_front()
                timer = time.perf_counter()
        if game_obj.rear_beep == 1:
            if timer < time.perf_counter() - 0.6:
                Sounds.pdc_rear()
                timer = time.perf_counter()
        elif game_obj.rear_beep == 2:
            if timer < time.perf_counter() - 0.4:
                Sounds.pdc_rear()
                timer = time.perf_counter()
        elif game_obj.rear_beep == 3:
            if timer < time.perf_counter() - 0.2:
                Sounds.pdc_rear()
                timer = time.perf_counter()

def del_pdc_buttons(game_object):
    for i in range(48, 55):
        game_object.del_button(i)
def draw_pdc_buttons_refactored(game_obj, sensors):
    # TODO: Make it work properly
    # Num 48-54
    x = game_obj.settings.offset_h
    y = game_obj.settings.offset_w
    color_map = [b"^7", b"^7", b"^7", b"^7", b"^7", b"^7"]

    button_colors = [b"^1", b"^3", b"^6", b"^2"]

    ranges_and_colors = [
        ((320, 40, 0), 0),
        ((350, 60, 0), 1),
        ((120, 190, 1), 2),
        ((140, 220, 2), 3),
        ((170, 240, 3), 4),
        ((300, 360, 10), 5)
    ]

    for sensor in sensors:
        sensor_value = sensor[0]
        for range_info in ranges_and_colors:
            if range_info[0][0] < sensor[1] < range_info[0][1] or sensor[1] < range_info[0][2]:
                range_index = range_info[1]
                if sensor_value == 3 and color_map[range_index] != button_colors[0]:
                    color_map[range_index] = button_colors[3]
                elif sensor_value < 3 and color_map[range_index] != button_colors[sensor_value]:
                    color_map[range_index] = button_colors[sensor_value]

    button_list = [(48, 100 + x, 130 + y, color_map[5] + b'^J\x84\xac'),
                   (49, 100 + x, 133 + y, color_map[0] + b'^J\x84\xaa'),
                   (50, 100 + x, 136 + y, color_map[1] + b'^J\x84\xad'),
                   (51, 115 + x, 130 + y, color_map[4] + b'^J\x84\xaf'),
                   (52, 115 + x, 133 + y, color_map[3] + b'^J\x84\xaa'),
                   (53, 115 + x, 136 + y, color_map[2] + b'^J\x84\xae'),
                   (54, 107 + x, 130 + y, b'^J\x81\xe1P\x81\xe2')]

    for button in button_list:
        game_obj.send_button(button[0], pyinsim.ISB_LMB, button[1], button[2], 5, 5, button[3])
