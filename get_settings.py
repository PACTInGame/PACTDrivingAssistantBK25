def get_settings_from_file():
    change_set = ["^2", "^2", "^2", "^2", "^2", "^2", "^2", "^2", "^2", "^2", "medium", "^2", "normal", "^2", "^1",
                  "1920x1080", "0", "avg", "metric", "0", "0", "^2", "^2", "de", "^2", "^2", "^2", "^2", "^2", "^2", 0,
                  "^2", "^2"]
    try:
        with open("settings.txt") as fp:
            for i, line in enumerate(fp):
                if 2 <= i <= 11:
                    line = line.split()
                    if str(line[0]) == "on":
                        change_set[i - 2] = True
                    else:
                        change_set[i - 2] = False

                if i == 12:
                    line = line.split()
                    change_set[i - 2] = str(line[0])
                if i == 13:
                    line = line.split()
                    if str(line[0]) == "on":
                        change_set[i - 2] = True
                    else:
                        change_set[i - 2] = False
                if i == 14:
                    line = line.split()
                    change_set[i - 2] = str(line[0])
                if i == 15 or i == 16:
                    line = line.split()
                    if str(line[0]) == "on":
                        change_set[i - 2] = True
                    else:
                        change_set[i - 2] = False
                if i == 17:
                    line = line.split()
                    line = line[0].split("x")
                    change_set[i - 2] = str(line[0]) + "x" + str(line[1])

                if i == 18:
                    line = line.split()
                    change_set[i - 2] = int(line[0])

                if i == 19:
                    line = line.split()
                    change_set[i - 2] = str(line[0])

                if i == 20:
                    line = line.split()
                    change_set[i - 2] = str(line[0])

                if i == 21:
                    line = line.split()
                    change_set[i - 2] = int(line[0])

                if i == 22:
                    line = line.split()
                    change_set[i - 2] = int(line[0])

                if i == 23 or i == 24:
                    line = line.split()
                    if str(line[0]) == "on":
                        change_set[i - 2] = True
                    else:
                        change_set[i - 2] = False

                if i == 25:
                    line = line.split()
                    change_set[i - 2] = str(line[0])

                if i == 26 or i == 27 or i == 28 or i == 29 or i == 30 or i == 31:
                    line = line.split()
                    if str(line[0]) == "on":
                        change_set[i - 2] = True
                    else:
                        change_set[i - 2] = False

                if i == 32:
                    line = line.split()
                    change_set[i - 2] = int(line[0])

                if i == 33 or i == 34:
                    line = line.split()
                    if str(line[0]) == "on":
                        change_set[i - 2] = True
                    else:
                        change_set[i - 2] = False

        print("Settings loaded successfully")
        return change_set

    except Exception as e:
        print(e)
        print("Error loading settings. Make sure settings.txt exists in Folder.")


# SETUP ACC AXIS FROM MENU!
def get_acc_settings_from_file():
    throttle = -1
    brake = -1
    steer = -1
    joy = -1
    try:
        with open("acc_settings.txt") as fp:
            for i, line in enumerate(fp):
                if i == 1:
                    line = line.split()
                    throttle = int(line[0])
                if i == 2:
                    line = line.split()
                    brake = int(line[0])
                if i == 3:
                    line = line.split()
                    joy = int(line[0])
                if i == 4:
                    line = line.split()
                    steer = int(line[0])
        if throttle != -1 and brake != -1:
            print("ACC settings loaded successfully")
        else:
            print("ACC not set up yet. ACC unavailable.")
        return throttle, brake, steer, joy

    except:
        print("Error loading ACC settings. ACC unavailable settings.txt exists in Folder.")


def get_controls_from_file():
    change_set = ["s", "x", "i", "2", "3", "1", "6", "down", "up", "q", "m", "k", "13"]
    try:
        with open("controls.txt") as fp:
            for i, line in enumerate(fp):
                if 1 <= i <= 10:
                    line = line.split()
                    change_set[i - 1] = line[0]
                elif 12 <= i <= 14:
                    line = line.split()
                    change_set[i - 2] = line[0]

        print("Controls loaded successfully")
        return change_set

    except Exception as e:
        print(e)
        print("Error loading control-settings. Make sure controls.txt exists in Folder.")


def write_settings(game_obj):
    settings = game_obj.settings
    file_string = "Important: Only change the letter in the at the beginning. Do not rearrange this layout. \n" \
                  'Assistance-Default-Settings ("on", or "off". Space necessary between setting and "<--"):\n' \
                  "{} <-- Head-up display\n" \
                  "{} <-- Forward collision warning\n" \
                  "{} <-- Blind spot warning\n" \
                  "{} <-- Cross traffic warning\n" \
                  "{} <-- Light assist\n" \
                  "{} <-- Park assist\n" \
                  "{} <-- Emergency assist\n" \
                  "{} <-- Lane assist\n" \
                  "{} <-- Cop aid system\n" \
                  "{} <-- Automatic Emergency Braking\n" \
                  "{} <-- Collision Warning Distance (early, medium, late)\n" \
                  "{} <-- Automatic Gearbox (when sequential Gearbox is set in LFS)\n" \
                  "{} <-- Lane departure warning intensity (early, normal, reduced)\n" \
                  "{} <-- Head-up display with images\n" \
                  "{} <-- stability control\n" \
                  "{} <-- Monitor resolution\n" \
                  "{} <-- warning sound (change in menu, when program is active)\n" \
                  "{} <-- Trip-computer mode\n" \
                  "{} <-- unit\n" \
                  "{} <-- HUD height offset\n" \
                  "{} <-- HUD width offset\n" \
                  "{} <-- automatic indicator turnoff\n" \
                  "{} <-- park emergency brake\n" \
                  "{} <-- language\n" \
                  "{} <-- audible parking aid\n" \
                  "{} <-- visual parking aid\n" \
                  "{} <-- side collision prevention\n" \
                  "{} <-- Indicator Sounds\n" \
                  "{} <-- Adaptive Brake Lights\n" \
                  "{} <-- Adaptive Brake Lights Style\n" \
                  "{} <-- Mode (0 = all on, 1 = all off, 2 = cop, 3 = race)\n" \
                  "{} <-- Stall-Protection\n" \
                  "{} <-- Realistic Clutch".format(settings.head_up_display,
                                                   settings.forward_collision_warning,
                                                   settings.blind_spot_warning,
                                                   settings.cross_traffic_warning,
                                                   settings.light_assist,
                                                   settings.park_distance_control,
                                                   settings.emergency_assist,
                                                   settings.lane_assist,
                                                   settings.cop_aid_system,
                                                   settings.automatic_emergency_braking,
                                                   settings.collision_warning_distance,
                                                   settings.automatic_gearbox,
                                                   settings.lane_dep_intensity,
                                                   settings.image_hud,
                                                   settings.PSC,
                                                   settings.resolution,
                                                   settings.collision_warning_sound,
                                                   settings.bc,
                                                   settings.unit,
                                                   settings.offset_h,
                                                   settings.offset_w,
                                                   settings.automatic_indicator_turnoff,
                                                   settings.park_emergency_brake,
                                                   settings.language,
                                                   settings.audible_parking_aid,
                                                   settings.visual_parking_aid,
                                                   settings.side_collision_prevention,
                                                   settings.indicator_sound,
                                                   settings.adaptive_brake_light,
                                                   settings.adaptive_brake_light_style,
                                                   settings.pact_mode,
                                                   settings.stall_protection,
                                                   settings.realistic_clutch)

    file_string = file_string.replace("True", "on")
    file_string = file_string.replace("False", "off")
    try:
        with open('settings.txt', 'w') as file:
            file.write(file_string)
        print("Settings saved successfully")
    except:
        print("An Error has Occurred during saving. Make sure settings.txt exists.")
