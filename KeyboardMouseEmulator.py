import pydirectinput
import keyboard


def use_keyboard_collision_warning(game_object):
    pydirectinput.keyDown(game_object.settings.BRAKE_KEY)
    if not game_object.holding_brake:
        pydirectinput.press(game_object.settings.IGNITION_KEY)
        print("pressed brake")
        game_object.holding_brake = True
    check_if_user_presses_brake(game_object)


def release_brake(game_object):
    #TODO Fix this (brake is released three times)
    if game_object.holding_brake:
        if (not check_if_user_presses_brake(game_object)) or check_if_user_presses_accel(game_object):
            pydirectinput.keyUp(game_object.settings.BRAKE_KEY)
            pydirectinput.press(game_object.settings.IGNITION_KEY)
            game_object.holding_brake = False
            print("released brake")


def check_if_user_presses_brake(game_object):
    return keyboard.is_pressed(game_object.settings.BRAKE_KEY)


def check_if_user_presses_accel(game_obj):
    return keyboard.is_pressed(game_obj.settings.ACC_KEY)


def use_mouse_collision_warning(game_object):
    pydirectinput.mouseDown(button='right')
