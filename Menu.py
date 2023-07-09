import Language
import pyinsim


def open_menu(game_object):
    lang = game_object.settings.language
    top = 80
    game_object.del_button(21)
    game_object.send_button(21, pyinsim.ISB_DARK, top, 0, 20, 5, game_object.language.translation(lang, "Menu"))
    game_object.send_button(22, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 5, 0, 20, 5, game_object.language.translation(lang, "Driving"))
    game_object.send_button(23, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 10, 0, 20, 5, game_object.language.translation(lang, "Parking"))
    game_object.send_button(24, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 15, 0, 20, 5, game_object.language.translation(lang, "Bus_Sim"))
    game_object.send_button(25, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 20, 0, 20, 5, game_object.language.translation(lang, "Language"))
    game_object.send_button(40, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, top + 25, 0, 20, 5,
                            game_object.language.translation(lang, "Close"))


def close_menu(game_object):
    for i in range(21, 41):
        game_object.delete_button(i)
    game_object.send_button(21, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 100, 0, 7, 5, "Menu")
