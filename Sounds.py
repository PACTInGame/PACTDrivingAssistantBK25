from pygame import mixer

mixer.init()


def collision_warning_sound(sound):
    mixer.music.load('data\\sounds\\warning_' + str(sound) + '.wav')
    mixer.music.play()


def beep():
    mixer.music.load('data\\sounds\\emawarning.wav')
    mixer.music.play()


def pdc_front():
    mixer.music.load('data\\sounds\\beep_front.wav')
    mixer.music.play()


def pdc_rear():
    print("rear")
    mixer.music.load('data\\sounds\\beep_rear.wav')
    mixer.music.play()


def beep_intense():
    mixer.music.load('data\\sounds\\emawarning_intense.wav')
    mixer.music.play()


def yield_sound():
    mixer.music.load('data\\sounds\\yield_warn.wav')
    mixer.music.play()


def playsound_indicator_on():
    print("indicator on")
    mixer.music.load('data\\sounds\\indicatorOn.wav')
    mixer.music.play()


def playsound_indicator_off():
    mixer.music.load('data\\sounds\\indicatorOff.wav')
    mixer.music.play()


def play_bus_door_open():
    mixer.music.load('data\\sounds\\door_open.wav')
    mixer.music.play()


def play_bus_door_close():
    mixer.music.load('data\\sounds\\door_close.wav')
    mixer.music.play()


def new_route():
    mixer.music.load('data\\sounds\\bus_radio\\bl_new_route.wav')
    mixer.music.play()
