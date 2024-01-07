import get_settings
import pyinsim


def settings_handling(message, game_object):
    message = message.split(': ^L$')[1]
    answer = "done."
    if message == "help":
        answer = "If you need more help, please visit the forum page."
        game_object.insim.send(pyinsim.ISP_MSL, Msg=b"$acc up : increase acc speed by 5 kph")
        game_object.insim.send(pyinsim.ISP_MSL, Msg=b"$acc down : decrease acc speed by 5 kph")
        game_object.insim.send(pyinsim.ISP_MSL, Msg=b"$acc on : set acc speed to current speed")
        game_object.insim.send(pyinsim.ISP_MSL, Msg=b"$acc off : turn off acc")
        game_object.insim.send(pyinsim.ISP_MSL, Msg=b"$set x on : turn on setting x")
        game_object.insim.send(pyinsim.ISP_MSL, Msg=b"$set x off : turn off setting x")
        game_object.insim.send(pyinsim.ISP_MSL,
                               Msg=b"available settings : hud, collisionwarn, crosstrafficwarn, blindspot, light, psc, gearbox")
        game_object.insim.send(pyinsim.ISP_MSL, Msg=b"$setup gearbox : start the gearbox setup for a new mod")
        game_object.insim.send(pyinsim.ISP_MSL, Msg=b"$mode x: x = all on/ all off/ cop/ race")
        game_object.insim.send(pyinsim.ISP_MSL, Msg=b"$siren on/off : turn on/off siren")
        game_object.insim.send(pyinsim.ISP_MSL, Msg=b"$strobe on/off : turn on/off strobe")
    elif message == "acc up":
        pass
    elif message == "acc down":
        pass
    elif message == "acc on":
        pass
    elif message == "acc off":
        pass
    elif message == "set hud on":
        pass
    elif message == "set hud off":
        pass
    elif message == "set collisionwarn on":
        pass
    elif message == "set collisionwarn off":
        pass
    elif message == "set crosstrafficwarn on":
        pass
    elif message == "set crosstrafficwarn off":
        pass
    elif message == "set blindspot on":
        pass
    elif message == "set blindspot off":
        pass
    elif message == "set light on":
        pass
    elif message == "set light off":
        pass
    elif message == "set psc on":
        game_object.settings.PSC = True
        get_settings.write_settings(game_object)
        answer = "PSC is turned on"
    elif message == "set psc off":
        game_object.settings.PSC = False

        answer = "PSC is turned off"
    elif message == "set gearbox on":
        pass
    elif message == "set gearbox off":
        pass
    elif message == "setup gearbox":
        pass
    elif message == "mode all on":
        pass
    elif message == "mode all off":
        pass
    elif message == "mode cop":
        pass
    elif message == "mode race":
        pass
    elif message == "siren on":
        pass
    elif message == "siren off":
        pass
    elif message == "strobe on":
        pass
    elif message == "strobe off":
        pass

    else:
        answer = "Unknown Command"
    game_object.insim.send(pyinsim.ISP_MSL, Msg=answer.encode())
    get_settings.write_settings(game_object)


def handle_commands(message, game_object):
    if '^L$' in message:
        settings_handling(message, game_object)
