from shapely.geometry import Polygon

import Calculations
import CarDataBase


def forward_collision_warning(game_obj):
    game_obj.collision_warning_intensity, game_obj.collision_warning_brake_force = check_warning_needed(
        game_obj.cars_relevant, game_obj.own_vehicle.x,
        game_obj.own_vehicle.y,
        game_obj.own_vehicle.heading,
        game_obj.own_vehicle.speed,
        game_obj.own_vehicle.throttle,
        game_obj.own_vehicle.brake, game_obj.own_vehicle.gear,
        game_obj.settings.collision_warning_distance,
        1.0,
        game_obj.own_vehicle.collision_warning_multiplier[1],
        game_obj.own_vehicle.speed_mci,
        game_obj.own_vehicle.acc_active,
        game_obj.own_vehicle.length)


def calc_necessary_braking(abstand, relative_geschwindigkeit, verzoegerung_B):
    """
    Berechnet die notwendige Verzögerung, um eine Kollision zu vermeiden.

    :param abstand: Der Abstand zwischen den Fahrzeugen in Metern (m)
    :param relative_geschwindigkeit: Die relative Geschwindigkeit der Fahrzeuge in Metern pro Sekunde (m/s)
    :param verzoegerung_B: Die Verzögerung des vorausfahrenden Fahrzeugs in Metern pro Sekunde zum Quadrat (m/s^2)
    :return: Die notwendige Verzögerung des folgenden Fahrzeugs in Metern pro Sekunde zum Quadrat (m/s^2)
    """
    verzoegerung_B = -verzoegerung_B
    # Die Zeit bis zur Kollision berechnen (ohne Verzögerung)
    if relative_geschwindigkeit <= 0:
        return 0  # Wenn relative Geschwindigkeit <= 0, ist keine Verzögerung notwendig

    zeit_bis_kollision = abstand / relative_geschwindigkeit

    # Die Strecke berechnen, die Fahrzeug B in dieser Zeit zurücklegt
    strecke_B = 0.5 * verzoegerung_B * zeit_bis_kollision ** 2
    # Die notwendige Verzögerung für Fahrzeug A berechnen, um vor der Kollision zum Stillstand zu kommen
    notwendige_verzoegerung = (relative_geschwindigkeit ** 2) / (2 * (abstand - strecke_B))
    return -notwendige_verzoegerung


def calc_brake_distance(rel_speed, acc, br, dynamic, cname):
    l, w = CarDataBase.get_size(cname)
    if dynamic > 0:
        dynamic = dynamic * ((rel_speed * 0.05) + 1)
    else:
        dynamic = dynamic * 0.5
    rel_speed2 = rel_speed * rel_speed
    rel_speed3 = rel_speed2 * rel_speed
    rel_speed4 = rel_speed3 * rel_speed
    if rel_speed > 0:
        new_brake_distance = 0.0000003303 * rel_speed4 - 0.00002877 * rel_speed3 + 0.003215 * rel_speed2 + 0.07473 * rel_speed - 0.6175 + rel_speed * 0.05 + acc * 2 - br * 4 + dynamic + l / 2 + 2
    else:
        new_brake_distance = 0
    # brake_distance = ((
    #        -2.09284547856357 * 10 ** -8 * rel_speed ** 4 + 1.10548262781578 + 10 ** -5 * rel_speed ** 3 +
    #        1.10058179124046 * 10 ** -3 * rel_speed ** 2 + 0.107662075560879 * rel_speed + 0.69747816828)) +
    #        rel_speed * 0.15 + acc * 2 - br * 4 + dynamic + l / 2 - 2

    return new_brake_distance


def check_warning_needed(cars, own_x, own_y, own_heading, own_speed, accelerator, brake, gear, setting, warn_multi,
                         warn_length, own_speed_mci, acc_active, own_length):
    speed = own_speed_mci if own_speed_mci - own_speed > 2 else own_speed
    angle_of_car = abs((own_heading + 16384) / 182.05)
    ang1, ang2, ang3, ang4 = angle_of_car + 1, angle_of_car + 340, angle_of_car + 20, angle_of_car + 359
    braking_needed = 0.0
    (x1, y1) = Calculations.calc_polygon_points(own_x, own_y, 85 * 65536, ang1)
    (x2, y2) = Calculations.calc_polygon_points(own_x, own_y, 2.0 * 65536, ang2)
    (x3, y3) = Calculations.calc_polygon_points(own_x, own_y, 2.0 * 65536, ang3)
    (x4, y4) = Calculations.calc_polygon_points(own_x, own_y, 85 * 65536, ang4)

    own_rectangle = Polygon([(x1, y1), (x2, y2), (x3, y3), (x4, y4)])

    rectangles_others = Calculations.create_rectangles_for_collision_warning(cars)

    car_in_front = [rectangle[0] for rectangle in rectangles_others
                    if Calculations.polygon_intersect(rectangle[1], own_rectangle)]
    for car in car_in_front:
        if not (car[1] < 15 or car[1] > 345):
            car_in_front.remove(car)
    collision_warning = 0

    setting_multiplier = {
        2: [6, 5, 4],
        1: [7, 6.5, 5.5],
        0: [8.5, 8, 7]
    }

    multiply = [x * warn_multi for x in setting_multiplier.get(setting, setting_multiplier[0])]
    for car in car_in_front:
        ok = check_heading_within_bounds(car[0].heading, own_heading)
        speed_diff = speed - car[0].speed

        if ok and gear > 0 and speed > 1 and speed_diff < 130:
            # brake_distance = calc_brake_distance(speed_diff, accelerator, brake, car[0].dynamic, car[0].cname)

            # car_distance = car[0].distance
            #
            # if car_distance < brake_distance * multiply[0] + warn_length:
            #     collision_warning = max(collision_warning, 3)
            # elif car_distance < brake_distance * multiply[1] + warn_length:
            #     collision_warning = max(collision_warning, 2)
            # elif car_distance < brake_distance * multiply[2] + warn_length or car_distance < (
            #         5 + warn_length) + speed * 0.05:
            #     collision_warning = max(collision_warning, 1)
            print(car[0].cname)
            distance = car[0].distance - car[0].length / 2 - own_length / 2 - 2
            if distance < 0:
                distance = 0.01
            braking_needed = calc_necessary_braking(distance, speed_diff / 3.6, car[0].dynamic)
            print("Dynamic: ", car[0].dynamic)
            if braking_needed < -multiply[0]:
                collision_warning = 3
            elif braking_needed < -multiply[1]:
                collision_warning = max(collision_warning, 2)
            elif braking_needed < -multiply[2]:
                collision_warning = max(collision_warning, 1)
            elif braking_needed > -multiply[0]:
                collision_warning = 0

    if 1 < speed < 12 and not acc_active:
        collision_warning = 3

    return collision_warning, braking_needed


def check_heading_within_bounds(heading, own_heading):
    heading_car_two_big = (heading + 5000) % 65536
    heading_car_two_small = (heading - 5000) % 65536

    if heading_car_two_small < heading_car_two_big:
        return heading_car_two_small < own_heading < heading_car_two_big
    else:
        return own_heading > heading_car_two_small or own_heading < heading_car_two_big
