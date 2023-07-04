from pygame import mixer

mixer.init()


def collision_warning_sound(sound):
    mixer.music.load('data\\warning_' + str(sound) + '.wav')
    mixer.music.play()


def beep():
    mixer.music.load('data\\emawarning.wav')
    mixer.music.play()


def beep_intense():
    mixer.music.load('data\\emawarning_intense.wav')
    mixer.music.play()


def yield_sound():
    mixer.music.load('data\\yield_warn.wav')
    mixer.music.play()


def playsound_indicator_on():
    mixer.music.load('data\\indicatorOn.wav')
    mixer.music.play()


def playsound_indicator_off():
    mixer.music.load('data\\indicatorOff.wav')
    mixer.music.play()
