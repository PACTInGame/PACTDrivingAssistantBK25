def calculate_warning(blindspot_l, blindspot_r, game_object, rectangles_others):
    side_collision_r, side_collision_l = False, False
    for rectangle in rectangles_others:
        print(is_left_threshold(game_object.own_vehicle.heading, rectangle[3]))
        if is_left_threshold(game_object.own_vehicle.heading,
                             rectangle[3]) and blindspot_l and game_object.own_vehicle.steer_forces > 50:
            side_collision_l = True
        elif is_right_threshold(game_object.own_vehicle.heading,
                                rectangle[3]) and blindspot_r and game_object.own_vehicle.steer_forces < -50:
            side_collision_r = True
    return side_collision_r, side_collision_l


def is_right_threshold(own_heading, other_heading):
    # Checks if the heading of another car is within a threshold
    lower_bound = (other_heading - 5000) % 65536
    upper_bound = (other_heading - 100) % 65536

    if lower_bound > upper_bound:
        return own_heading > lower_bound or own_heading < upper_bound
    return lower_bound < own_heading < upper_bound


def is_left_threshold(own_heading, other_heading):
    # Checks if the heading of another car is within a threshold
    lower_bound = (other_heading + 100) % 65536
    upper_bound = (other_heading + 5000) % 65536

    if lower_bound > upper_bound:
        return own_heading > lower_bound or own_heading < upper_bound
    return lower_bound < own_heading < upper_bound
