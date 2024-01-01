import Checks
import characters
import chaos
import abilities
from config import config
import input
import Settings
from sleep import sleep
import colorprint
import pyautogui
from pynput.mouse import Button, Controller

Settings.init()
sleep(100, 200)
Checks.healthCheck()