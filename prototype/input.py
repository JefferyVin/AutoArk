import pydirectinput
from tools import sleep
import random
from colorprint import prRed, prCyan
import Settings
import os
from pynput.mouse import Button, Controller

def shortcut(shorcutsequence):
    if len(shorcutsequence) == 1:
        if Settings.DEBUG:
            prCyan("KeyShortcut " + shorcutsequence[0])
        pydirectinput.press(shorcutsequence[0], interval=random.randint(100, 200)/1000)
    elif len(shorcutsequence) == 2:
        if Settings.DEBUG:
            prCyan("Shortcut " + shorcutsequence[0] + " " + shorcutsequence[1])
        pydirectinput.keyDown(shorcutsequence[0])
        sleep(100, 200)
        pydirectinput.press(shorcutsequence[1])
        sleep(100,200)
        pydirectinput.keyUp(shorcutsequence[0])
    else:
        prRed("Shortcut too long or User forgot to set Shortcut in config.py")
        
def mouseMoveTo(**kwargs):
    x = kwargs["x"]
    y = kwargs["y"]
    pydirectinput.moveTo(x=x, y=y)
    
def useskill(Key):
    if Key == "mouse1":
        mouse = Controller()
        mouse.click(Button.x2)
    elif Key == "mouse2":
        mouse = Controller()
        mouse.click(Button.x1)
    else:
        pydirectinput.press(Key)
    
if __name__ == "__main__":
    print("Input Script Running")
    Settings.init()
    if os.environ.get("DEBUG") == '1':
        Settings.DEBUG = True
        prRed("DEBUG Mode is on")
    print(Settings.DEBUG)
    shortcut(['x', 'd'])