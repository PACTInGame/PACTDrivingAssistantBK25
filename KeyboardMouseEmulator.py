import pydirectinput
import keyboard

import pyinsim

SPARE_KEY = "m"


def use_keyboard_collision_warning(game_object):
    game_object.insim.send(pyinsim.ISP_MST,
                           Msg=b"/key " + game_object.settings.SPARE_KEY_1.encode() + b" brake")
    game_object.insim.send(pyinsim.ISP_MST,
                           Msg=b"/key " + game_object.settings.SPARE_KEY_2.encode() + b" throttle")
    pydirectinput.keyDown(SPARE_KEY)
    if not game_object.holding_brake:
        game_object.holding_brake = True


def release_brake(game_object):
    if game_object.holding_brake:
        game_object.insim.send(pyinsim.ISP_MST,
                               Msg=b"/key " + game_object.settings.BRAKE_KEY.encode() + b" brake")
        game_object.insim.send(pyinsim.ISP_MST,
                               Msg=b"/key " + game_object.settings.ACC_KEY.encode() + b" throttle")
        pydirectinput.keyUp(SPARE_KEY)
        game_object.holding_brake = False

