import webbrowser

import keyboard

import Language
import Menu
import get_settings
import pyinsim


def send_mode(game_object):
    if game_object.current_menu == 0:
        if game_object.settings.pact_mode == 0:
            game_object.send_button(103, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 105, 0, 12, 5,
                                    game_object.language.translation(game_object.lang, "All_on"))
        elif game_object.settings.pact_mode == 1:
            game_object.send_button(103, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 105, 0, 12, 5,
                                    game_object.language.translation(game_object.lang, "All_off"))
        elif game_object.settings.pact_mode == 2:
            game_object.send_button(103, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 105, 0, 12, 5,
                                    game_object.language.translation(game_object.lang, "Cop_Mode"))

            game_object.send_button(131, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 110, 0, 12, 5,
                                    game_object.language.translation(game_object.lang, "Cop_Menu"))
        else:
            game_object.send_button(103, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 105, 0, 12, 5,
                                    game_object.language.translation(game_object.lang, "Race_Mode"))


def open_cop_menu(game_object):
    game_object.del_button(21)
    game_object.del_button(100)
    game_object.del_button(103)
    game_object.del_button(103)
    game_object.del_button(131)
    game_object.current_menu = 7
    game_object.send_button(132, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 95, 0, 12, 5,
                            game_object.language.translation(game_object.lang, "Automatic_Siren"))
    game_object.send_button(133, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 100, 0, 12, 5,
                            game_object.language.translation(game_object.lang, "Use_Indicators"))
    game_object.send_button(134, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 105, 0, 12, 5,
                            game_object.language.translation(game_object.lang, "Use_Lights"))
    game_object.send_button(135, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 110, 0, 12, 5,
                            game_object.language.translation(game_object.lang, "Use_Extra_Light"))
    game_object.send_button(136, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 115, 0, 12, 5,
                            game_object.language.translation(game_object.lang, "Use_Fog_Light"))
    game_object.send_button(137, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 120, 0, 12, 5,
                            game_object.language.translation(game_object.lang, "Track_Suspect"))
    game_object.send_button(138, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 125, 0, 12, 5,
                            game_object.language.translation(game_object.lang, "Close"))


def change_mode(game_object):
    mode = game_object.settings.pact_mode
    mode += 1
    if mode > 3:
        mode = 0

    game_object.settings.pact_mode = mode
    if mode == 3:
        game_object.INTERVAL = 100
        game_object.send_button(110, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 0, 88, 12, 5,
                                "Diff Last")
        game_object.send_button(111, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 0, 100, 12, 5,
                                "Diff Best")
    else:
        game_object.INTERVAL = 200
        for i in range(110, 121):
            game_object.del_button(i)
    send_mode(game_object)
    get_settings.write_settings(game_object)


def open_menu(game_object):
    lang = game_object.settings.language
    top = 80
    game_object.current_menu = 1
    game_object.del_button(21)
    game_object.del_button(100)
    game_object.del_button(103)
    game_object.del_button(131)

    game_object.send_button(21, pyinsim.ISB_DARK, top, 0, 20, 5, game_object.language.translation(lang, "Menu"))
    game_object.send_button(26, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 5, 0, 20, 5,
                            game_object.language.translation(lang, "General"))
    game_object.send_button(22, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 10, 0, 20, 5,
                            game_object.language.translation(lang, "Driving"))
    game_object.send_button(23, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 15, 0, 20, 5,
                            game_object.language.translation(lang, "Parking"))
    game_object.send_button(24, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 20, 0, 20, 5,
                            game_object.language.translation(lang, "Bus_Sim"))
    game_object.send_button(27, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 25, 0, 20, 5,
                            game_object.language.translation(lang, "Keys_Axes"))
    game_object.send_button(25, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 30, 0, 20, 5,
                            game_object.language.translation(lang, "Language"))

    game_object.send_button(40, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 35, 0, 20, 5,
                            game_object.language.translation(lang, "Close"))


def listen_for_key(game_object, key):
    def use_new_key(event):
        new_key = event.name
        game_object.notifications.append(["^2New key: " + new_key, 1])
        if key == "shift_up":
            print("new:" + new_key)
            game_object.settings.SHIFT_UP_KEY = new_key
        elif key == "shift_down":
            game_object.settings.SHIFT_DOWN_KEY = new_key
        elif key == "ignition":
            game_object.settings.IGNITION_KEY = new_key
        elif key == "handbrake":
            game_object.settings.HANDBRAKE_KEY = new_key
        elif key == "throttle":
            game_object.settings.THROTTLE_KEY = new_key
        elif key == "brake":
            game_object.settings.BRAKE_KEY = new_key
        elif key == "spare_1":
            game_object.settings.SPARE_KEY_1 = new_key
        elif key == "spare_2":
            game_object.settings.SPARE_KEY_2 = new_key
        elif key == "throttle_axis":
            game_object.settings.THROTTLE_AXIS = new_key
        elif key == "brake_axis":
            game_object.settings.BRAKE_AXIS = new_key
        elif key == "steer_axis":
            game_object.settings.STEER_AXIS = new_key
        keyboard.unhook(use_new_key)
        game_object.settings.save_controls()
        open_keys_menu(game_object)
        return False

    # Listen for a key event
    game_object.notifications.append(["^3Listening for Key!", 1])
    keyboard.hook(use_new_key)


def open_keys_menu(game_object):
    # TODO : axes(multiple keys not yet supported)
    lang = game_object.settings.language
    game_object.current_menu = 6
    game_object.notifications.append(["^1Caution, axes not yet supported!", 2])
    top = 80
    for i in range(21, 41):
        game_object.del_button(i)
    game_object.send_button(21, pyinsim.ISB_DARK, top, 0, 20, 5, game_object.language.translation(lang, "Keys_Axes"))
    game_object.send_button(22, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 5, 0, 20, 5,
                            game_object.language.translation(lang, "Shift_Up"))
    game_object.send_button(23, pyinsim.ISB_LIGHT, top + 5, 20, 5, 5,
                            game_object.settings.SHIFT_UP_KEY)
    game_object.send_button(24, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 10, 0, 20, 5,
                            game_object.language.translation(lang, "Shift_Down"))
    game_object.send_button(25, pyinsim.ISB_LIGHT, top + 10, 20, 5, 5,
                            game_object.settings.SHIFT_DOWN_KEY)
    game_object.send_button(26, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 15, 0, 20, 5,
                            game_object.language.translation(lang, "Ignition"))
    game_object.send_button(27, pyinsim.ISB_LIGHT, top + 15, 20, 5, 5,
                            game_object.settings.IGNITION_KEY)
    game_object.send_button(28, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 20, 0, 20, 5,
                            game_object.language.translation(lang, "Handbrake"))
    game_object.send_button(29, pyinsim.ISB_LIGHT, top + 20, 20, 5, 5,
                            game_object.settings.HANDBRAKE_KEY)
    if game_object.own_vehicle.control_mode == 2:
        game_object.send_button(30, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 25, 0, 20, 5,
                                game_object.language.translation(lang, "Throttle_Axis"))
        game_object.send_button(31, pyinsim.ISB_LIGHT, top + 25, 20, 5, 5,
                                str(game_object.settings.THROTTLE_AXIS))
        game_object.send_button(32, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 30, 0, 20, 5,
                                game_object.language.translation(lang, "Brake_Axis"))
        game_object.send_button(33, pyinsim.ISB_LIGHT, top + 30, 20, 5, 5,
                                str(game_object.settings.BRAKE_AXIS))
        game_object.send_button(34, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 35, 0, 20, 5,
                                game_object.language.translation(lang, "Steer_Axis"))
        game_object.send_button(35, pyinsim.ISB_LIGHT, top + 35, 20, 5, 5,
                                str(game_object.settings.STEER_AXIS))
        game_object.send_button(36, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 40, 0, 20, 5,
                                game_object.language.translation(lang, "Clutch_Axis"))
        game_object.send_button(37, pyinsim.ISB_LIGHT, top + 40, 20, 5, 5,
                                str(game_object.settings.CLUTCH_AXIS))
    else:
        game_object.send_button(30, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 25, 0, 20, 5,
                                game_object.language.translation(lang, "Throttle_Key"))
        game_object.send_button(31, pyinsim.ISB_LIGHT, top + 25, 20, 5, 5,
                                game_object.settings.ACC_KEY)
        game_object.send_button(32, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 30, 0, 20, 5,
                                game_object.language.translation(lang, "Brake_Key"))
        game_object.send_button(33, pyinsim.ISB_LIGHT, top + 30, 20, 5, 5,
                                game_object.settings.BRAKE_KEY)
        game_object.send_button(34, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 35, 0, 20, 5,
                                game_object.language.translation(lang, "Spare_Key_1"))
        game_object.send_button(35, pyinsim.ISB_LIGHT, top + 35, 20, 5, 5,
                                game_object.settings.SPARE_KEY_1)
        game_object.send_button(36, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 40, 0, 20, 5,
                                game_object.language.translation(lang, "Spare_Key_2"))
        game_object.send_button(37, pyinsim.ISB_LIGHT, top + 40, 20, 5, 5,
                                game_object.settings.SPARE_KEY_2)
    game_object.send_button(40, pyinsim.ISB_DARK | pyinsim.ISB_CLICK,
                            top + 45, 0, 20, 5,
                            game_object.language.translation(lang, "Close"))


def open_general_menu(game_object):
    lang = game_object.settings.language
    game_object.current_menu = 5
    top = 80
    for i in range(21, 41):
        game_object.del_button(i)
    game_object.send_button(21, pyinsim.ISB_DARK, top, 0, 20, 5, game_object.language.translation(lang, "General"))
    game_object.send_button(22, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 5, 0, 20, 5,
                            game_object.language.translation(lang, "Units"))
    game_object.send_button(23, pyinsim.ISB_LIGHT, top + 5, 20, 10, 5,
                            game_object.language.translation(lang, "Metric")
                            if game_object.settings.unit == "metric"
                            else game_object.language.translation(lang, "Imperial"))
    game_object.send_button(24, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 10, 0, 20, 5,
                            game_object.language.translation(lang, "HUD"))
    game_object.send_button(27, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 10, 20, 5, 5,
                            game_object.language.translation(lang, "up"))
    game_object.send_button(28, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 10, 25, 5, 5,
                            game_object.language.translation(lang, "down"))
    game_object.send_button(29, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 10, 30, 5, 5,
                            game_object.language.translation(lang, "left"))
    game_object.send_button(30, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 10, 35, 5, 5,
                            game_object.language.translation(lang, "right"))
    game_object.send_button(25, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 15, 0, 20, 5,
                            game_object.language.translation(lang, "Board_computer"))
    game_object.send_button(26, pyinsim.ISB_LIGHT, top + 15, 20, 10, 5,
                            game_object.language.translation(lang, "Range")
                            if game_object.settings.bc == "range"
                            else game_object.language.translation(lang, "Distance")
                            if game_object.settings.bc == "distance"
                            else game_object.language.translation(lang, "off"))
    game_object.send_button(31, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 20, 0, 20, 5,
                            game_object.language.translation(lang, "Indicator_Sound"))
    game_object.send_button(40, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 25, 0, 20, 5,
                            game_object.language.translation(lang, "Close"))


def open_bus_menu(game_object):
    lang = game_object.settings.language
    game_object.current_menu = 4
    top = 80
    for i in range(21, 41):
        game_object.del_button(i)
    game_object.send_button(21, pyinsim.ISB_DARK, top, 0, 20, 5, game_object.language.translation(lang, "Bus_Menu"))
    game_object.send_button(22, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 5, 0, 20, 5,
                            game_object.language.translation(lang, "Door_Sound"))
    game_object.send_button(23, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 10, 0, 20, 5,
                            game_object.language.translation(lang, "Route_Sound"))
    game_object.send_button(24, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 15, 0, 20, 5,
                            game_object.language.translation(lang, "Announcements"))
    game_object.send_button(25, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 20, 0, 20, 5,
                            game_object.language.translation(lang, "Sound_effects"))
    game_object.send_button(26, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 25, 0, 20, 5,
                            game_object.language.translation(lang, "Start_offline_sim"))
    game_object.send_button(40, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 30, 0, 20, 5,
                            game_object.language.translation(lang, "Close"))


def open_drive_menu(game_object):
    print("open drive menu")
    lang = game_object.settings.language
    game_object.current_menu = 2
    top = 80
    for i in range(21, 41):
        game_object.del_button(i)
    game_object.send_button(21, pyinsim.ISB_DARK, top - 5, 0, 20, 5, game_object.language.translation(lang, "Driving"))
    game_object.send_button(31, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top, 0, 20, 5,
                            game_object.language.translation(lang, "Emergency_Brake"))
    game_object.send_button(32, pyinsim.ISB_LIGHT, top, 20, 20, 5,
                            game_object.language.translation(lang, "Emergency_Brake_Setting"))
    game_object.send_button(22, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 5, 0, 20, 5,
                            game_object.language.translation(lang, "Forward_Collision_Warning"))
    game_object.send_button(29, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 5, 20, 10, 5,
                            game_object.language.translation(lang, "Collision_Warning_Distance"))
    game_object.send_button(23, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 10, 0, 20, 5,
                            game_object.language.translation(lang, "Blind_Spot_Warning"))
    game_object.send_button(24, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 15, 0, 20, 5,
                            game_object.language.translation(lang, "Side_Collision_Prevention"))
    game_object.send_button(25, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 20, 0, 20, 5,
                            game_object.language.translation(lang, "Cross_Traffic_Warning"))
    game_object.send_button(26, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 25, 0, 20, 5,
                            game_object.language.translation(lang, "PSC"))
    game_object.send_button(27, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 30, 0, 20, 5,
                            game_object.language.translation(lang, "Light_Assist"))
    game_object.send_button(33, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 35, 0, 20, 5,
                            game_object.language.translation(lang, "Adaptive_Brake_Light"))
    game_object.send_button(34, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 35, 20, 10, 5,
                            game_object.language.translation(lang, "Adaptive_Brake_Light_Style"))
    game_object.send_button(28, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 40, 0, 20, 5,
                            game_object.language.translation(lang, "Automatic_Indicator_Turnoff"))
    game_object.send_button(30, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 45, 0, 20, 5,
                            game_object.language.translation(lang, "Gearbox"))
    game_object.send_button(40, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 50, 0, 20, 5,
                            game_object.language.translation(lang, "Close"))


def open_park_menu(game_object):
    game_object.current_menu = 3
    lang = game_object.settings.language
    top = 80
    for i in range(21, 41):
        game_object.del_button(i)
    game_object.send_button(21, pyinsim.ISB_DARK, top, 0, 20, 5, game_object.language.translation(lang, "Driving"))
    game_object.send_button(22, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 5, 0, 20, 5,
                            game_object.language.translation(lang, "Park_Distance_Control"))
    game_object.send_button(23, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 10, 0, 20, 5,
                            game_object.language.translation(lang, "Parking_Emergency_Brake"))
    game_object.send_button(24, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 15, 0, 20, 5,
                            game_object.language.translation(lang, "Visual_Parking_Aid"))
    game_object.send_button(25, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 20, 0, 20, 5,
                            game_object.language.translation(lang, "Audible_Parking_Aid"))
    game_object.send_button(40, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 25, 0, 20, 5,
                            game_object.language.translation(lang, "Close"))


def close_menu(game_object):
    game_object.current_menu = 0
    for i in range(21, 41):
        game_object.del_button(i)
    game_object.send_button(21, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 100, 0, 12, 5,
                            game_object.language.translation(game_object.lang, "Menu"))
    if game_object.update_available:
        game_object.send_button(100, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 95, 0, 12, 5,
                                game_object.language.translation(game_object.lang, "Update"))

    get_settings.write_settings(game_object)
    send_mode(game_object)


def close_cop_menu(game_object):
    for i in range(131, 141):
        game_object.del_button(i)
    close_menu(game_object)


def ask(game_obj):
    game_obj.del_button(100)
    game_obj.send_button(100, pyinsim.ISB_DARK, 95, 75, 50, 5,
                         game_obj.language.translation(game_obj.lang, "Google_Drive"))
    game_obj.send_button(101, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 100, 75, 15, 5, "^2Yes")
    game_obj.send_button(102, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 100, 110, 15, 5, "^1Cancel")


def close_ask(game_obj):
    for i in range(100, 103):
        game_obj.del_button(i)
    game_obj.send_button(100, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 95, 0, 12, 5,
                         game_obj.language.translation(game_obj.lang, "Update"))


def open_google_drive(game_object):
    webbrowser.open("https://drive.google.com/drive/folders/1Byr4onJvHW1MP7zCei0HUgOUG9t5R_Dl?usp=share_link")
    close_ask(game_object)
