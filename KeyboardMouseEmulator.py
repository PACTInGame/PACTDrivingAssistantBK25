import pydirectinput
import keyboard

import pyinsim

SPARE_KEY = "m"


def use_keyboard_collision_warning(game_object):
    # Todo check if this is possible somehow
    game_object.insim.send(pyinsim.ISP_MST,
                        Msg=b"/key M brake")
    pydirectinput.keyDown(SPARE_KEY)
    if not game_object.holding_brake:
        #pydirectinput.press(game_object.settings.IGNITION_KEY)
        game_object.holding_brake = True
    check_if_user_presses_brake(game_object)


def release_brake(game_object):
    if game_object.holding_brake:
        game_object.insim.send(pyinsim.ISP_MST,
                               Msg=b"/key down brake")
        if (not check_if_user_presses_brake(game_object)) or check_if_user_presses_accel(game_object):
            pydirectinput.keyUp(SPARE_KEY)
            #pydirectinput.press(game_object.settings.IGNITION_KEY)
            game_object.holding_brake = False


def check_if_user_presses_brake(game_object):
    return keyboard.is_pressed(game_object.settings.BRAKE_KEY)


def check_if_user_presses_accel(game_obj):
    return keyboard.is_pressed(game_obj.settings.ACC_KEY)


def use_mouse_collision_warning(game_object):
    pydirectinput.mouseDown(button='right')
