import pydirectinput
import pyautogui
import time
time.sleep(2)
# hold down key "down" for 1 sec
#pyautogui.keyDown("up")
pydirectinput.keyDown("up")
time.sleep(1)
pydirectinput.keyUp("up")