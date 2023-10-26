import webbrowser

import Language
import pyinsim


def open_menu(game_object):
    lang = game_object.settings.language
    top = 80
    game_object.current_menu = 1
    game_object.del_button(21)
    game_object.del_button(100)

    game_object.send_button(21, pyinsim.ISB_DARK, top, 0, 20, 5, game_object.language.translation(lang, "Menu"))
    game_object.send_button(22, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 5, 0, 20, 5,
                            game_object.language.translation(lang, "Driving"))
    game_object.send_button(23, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 10, 0, 20, 5,
                            game_object.language.translation(lang, "Parking"))
    game_object.send_button(24, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 15, 0, 20, 5,
                            game_object.language.translation(lang, "Bus_Sim"))
    game_object.send_button(25, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 20, 0, 20, 5,
                            game_object.language.translation(lang, "Language"))
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
    print(game_object.settings.bus_offline_sim)
    game_object.send_button(40, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 30, 0, 20, 5,
                            game_object.language.translation(lang, "Close"))


def open_drive_menu(game_object):
    print("open drive menu")
    lang = game_object.settings.language
    game_object.current_menu = 2
    top = 80
    for i in range(21, 41):
        game_object.del_button(i)
    game_object.send_button(21, pyinsim.ISB_DARK, top, 0, 20, 5, game_object.language.translation(lang, "Driving"))
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
    game_object.send_button(28, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 35, 0, 20, 5,
                            game_object.language.translation(lang, "Automatic_Indicator_Turnoff"))
    game_object.send_button(40, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 40, 0, 20, 5,
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
    game_object.send_button(40, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 20, 0, 20, 5,
                            game_object.language.translation(lang, "Close"))


def close_menu(game_object):
    print("close menu")
    game_object.current_menu = 0
    for i in range(21, 41):
        game_object.del_button(i)
    game_object.send_button(21, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 100, 0, 7, 5, "Menu")
    if game_object.update_available:
        game_object.send_button(100, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 95, 0, 12, 5, "Update avail.")


def ask(game_obj):
    game_obj.del_button(100)
    game_obj.send_button(100, pyinsim.ISB_DARK, 95, 85, 30, 5, "^7This will forward you to Google "
                                                               "Drive. Continue?")
    game_obj.send_button(101, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 100, 85, 15, 5, "^2Yes")
    game_obj.send_button(102, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 100, 100, 15, 5, "^1Cancel")

def close_ask(game_obj):
    for i in range(100, 103):
        game_obj.del_button(i)
    game_obj.send_button(100, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 95, 0, 12, 5, "Update avail.")
def open_google_drive(game_object):
    webbrowser.open("https://drive.google.com/drive/folders/1Byr4onJvHW1MP7zCei0HUgOUG9t5R_Dl?usp=share_link")
    close_ask(game_object)
