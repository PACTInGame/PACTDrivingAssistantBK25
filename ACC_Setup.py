from threading import Thread

import pygame
import time

import Menu
import pyinsim


def write_settings(throttle_axis, brake_axis, num_joystick, steering):
    file_string = "Important: DO NOT CHANGE THIS FILE MANUALLY. PLEASE USE SETUP_CRUISE_CONTROL.exe\n" \
                  "{} Throttle Axis\n" \
                  "{} Brake Axis\n" \
                  "{} Joystick\n" \
                  "{} Steering".format(throttle_axis, brake_axis, num_joystick, steering)

    try:
        with open('acc_settings.txt', 'w') as file:
            file.write(file_string)
        print("Settings saved successfully")
    except:
        print("An Error has occurred during saving. Make sure acc_settings.txt exists and you have enough rights.")


def set_up(game_object):
    t = Thread(target=start_setup, args=(game_object,))
    t.start()


def start_setup(game_object):
    Menu.close_menu(game_object)
    game_object.send_button(152, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 70, 75, 50, 8,
                            "^1Let go of your wheel and pedals now! DO NOT TOUCH THEM!")
    game_object.send_button(153, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 60, 75, 50, 8,
                            "^7Touch your wheel/pedals only when instructed! Starting Setup...")

    print("Hello")
    print("This setup will guide you through setting up the PACT Driving Assistant Cruise Control")
    time.sleep(1)
    game_object.send_button(153, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 60, 75, 50, 8,
                            "^7Starting Setup...")
    print("Please DO NOT touch your racing wheel or pedals until instructed to do so!")
    time.sleep(2)
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    time.sleep(2)
    game_object.send_button(153, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 60, 75, 50, 8,
                            "^7Detecting Controllers... ")
    if len(joysticks) > 0:
        print("I've detected the following controllers: ")
        for joystick in joysticks:
            print(joystick.get_name() + " ")
    else:
        print("Error, no game-pads/wheels/controllers detected. \n Please make sure your wheel is turned on and retry!")
    game_object.send_button(153, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 60, 75, 50, 8,
                            "^7Detected Controllers: " + str(len(joysticks)))
    pygame.init()
    time.sleep(4)
    game_object.send_button(153, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 60, 75, 50, 8,
                            "^7Press your THROTTLE axis now.")
    print("please press your THROTTLE axis now.")
    brake_axis = -1
    throttle_axis = -1
    num_joystick = -1
    steering = -1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                throttle_axis = event.axis
                num_joystick = event.joy
        if throttle_axis != -1:
            break
    game_object.send_button(153, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 60, 75, 50, 8,
                            "^7Detected Throttle Axis: " + str(throttle_axis))
    print("I have detected your throttle axis! It is axis " + str(throttle_axis) + ".")
    time.sleep(4)
    game_object.send_button(153, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 60, 75, 50, 8,
                            "Press your BRAKE axis now.")
    print("please press your BRAKE axis now.")
    loops = 5
    while True:
        for event in pygame.event.get():
            if loops < 0:
                if event.type == pygame.JOYAXISMOTION:
                    brake_axis = event.axis
        loops -= 1
        if brake_axis != -1:
            break
    game_object.send_button(153, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 60, 75, 50, 8,
                            "^7Detected Brake Axis: " + str(brake_axis))
    print("I have detected your brake axis! It is axis " + str(brake_axis) + ".")
    time.sleep(4)
    game_object.send_button(153, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 60, 75, 50, 8,
                            "Turn your STEERING axis now.")
    print("please turn your STEERING axis now.")
    loops = 5
    while True:
        for event in pygame.event.get():
            if loops < 0:
                if event.type == pygame.JOYAXISMOTION:
                    steering = event.axis
        loops -= 1
        if steering != -1:
            break
    game_object.send_button(153, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 60, 75, 50, 8,
                            "Detected Steering Axis: " + str(steering))
    print("I have detected your steer axis! It is axis " + str(steering) + ".")
    time.sleep(2)
    game_object.send_button(153, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 60, 75, 50, 8,
                            "Setup Complete, saving settings now...")
    print("Your settings will be saved. If you want to retry the setup, just restart this file!")
    write_settings(throttle_axis, brake_axis, num_joystick, steering)
    time.sleep(3)
    game_object.send_button(153, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 60, 75, 50, 8,
                            "Closing setup.")
    print("Closing Setup now")
    time.sleep(2)
    game_object.del_button(152)
    game_object.del_button(153)
    game_object.send_button(153, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 60, 75, 50, 8,
                            "^3Restart PACT Driving Assistant to apply changes.")
    game_object.send_button(152, pyinsim.ISB_DARK | pyinsim.ISB_CLICK, 70, 75, 50, 8,
                            "^3Something Wrong? Calibrate again in Keys/Axes menu.")
