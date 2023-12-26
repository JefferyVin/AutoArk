
from config import config
import pyautogui
import pydirectinput
import time
import random
import math
import argparse
from datetime import date
import input
import os
from colorprint import prCyan, prRed, prGreen
import Checks
from sleep import sleep
from input import mouseMoveTo
import Settings
from abilities import abilities


def enterChaosfromContentList():
    """Enter chaos dungeon from content list"""
    Checks.DetectBlackScreen()
    while True:
        # Leave chaos dungeon if already inside of one
        inChaos = Checks.inChaosCheck()
        if inChaos != None:
            prRed("Still in the last chaos run, quitting ripbozo")
            quitChaos()
            sleep(5000, 6000)
            while True:
                inTown = Checks.inCityCheck()
                if inTown != None:
                    Settings.states["status"] = "inCity"
                    prGreen("Status: inCity")
                    break
                sleep(5000, 6000)
        
        # Shortcut for content list
        input.shortcut(config["Shortcut-ContentList"])
        sleep(1200, 1400)
        
        # Click on shortcut button for chaos dungeon
        mouseMoveTo(x=886, y=346)
        sleep(500, 600)
        pydirectinput.click(x=886, y=346, button="left")
        sleep(1500, 1600)
        mouseMoveTo(x=886, y=346)
        sleep(500, 600)
        pydirectinput.click(x=886, y=346, button="left")
        sleep(500, 600)

        
        enterButton = Checks.locateCenterOnScreen(
            "./screenshots/enterButton.png",
            confidence=0.75,
            region=(1334, 754, 120, 60),
        )
        
        if enterButton == None:
            sleep(10, 200)
            continue

        SelectChaosLevel()
        
        
        if enterButton != None:
            x, y = enterButton
            mouseMoveTo(x=x, y=y)
            sleep(800, 900)
            pydirectinput.click(x=x, y=y, button="left")
            sleep(100, 200)
            pydirectinput.click(x=x, y=y, button="left")
            sleep(100, 200)
            pydirectinput.click(x=x, y=y, button="left")
            sleep(100, 200)
            pydirectinput.click(x=x, y=y, button="left")
            sleep(100, 200)
            pydirectinput.click(x=x, y=y, button="left")
            break
        else:
            mouseMoveTo(x=886, y=346)
            sleep(800, 900)
            pydirectinput.click(x=886, y=346, button="left")
            sleep(200, 300)
            pydirectinput.click(x=886, y=346, button="left")
            sleep(200, 300)
            pydirectinput.click(x=886, y=346, button="left")
            sleep(1800, 1900)

    sleep(500, 600)
    
    # repeatedly trying to click on accept button
    while True:
        acceptButton = Checks.locateCenterOnScreen(
            "./screenshots/acceptButton.png",
            confidence=0.75,
            region=config["regions"]["center"],
        )
        if acceptButton != None:
            x, y = acceptButton
            mouseMoveTo(x=x, y=y)
            sleep(200, 300)
            pydirectinput.click(x=x, y=y, button="left")
            sleep(100, 200)
            pydirectinput.click(x=x, y=y, button="left")
            sleep(100, 200)
            pydirectinput.click(x=x, y=y, button="left")
            break
        sleep(500, 600)
    Settings.states["status"] = "floor1"
    prGreen("Status: floor1")
    return

def saveAbilitiesScreenshots():
    for ability in abilities[config["characters"][Settings.states["currentCharacter"]]["class"]]:
        if ability["abilityType"] == "awakening":
            continue
        if ability["abilityType"] == "specialty1":
            continue
        if ability["abilityType"] == "specialty2":
            continue
        left = ability["position"]["left"]
        top = ability["position"]["top"]
        width = ability["position"]["width"]
        height = ability["position"]["height"]
        im = pyautogui.screenshot(region=(left, top, width, height),)
        
        Settings.states["abilityScreenshots"].append(
            {
                "key": ability["key"],
                "image": im,
                "cast": ability["cast"],
                "castTime": ability["castTime"],
                "hold": ability["hold"],
                "holdTime": ability["holdTime"],
                "directional": ability["directional"],
            }
        )
        sleep(200, 300)

def doFloor1():
    clearQuest()
    
    # check repair
    if config["auraRepair"]:
        if Settings.DEBUG:
            prCyan("Aura Repair")
        doAuraRepair(forced=False)

    # trigger start floor 1
    mouseMoveTo(x=845, y=600)
    sleep(450, 500)
    pydirectinput.click(button=config["move"])
    sleep(450, 500)
    
    _curr = config["characters"][Settings.states["currentCharacter"]]
    # Prefight prep
    # Summoner - switch to akir
    if _curr["class"] == "summoner":
        mouseMoveTo(x=1010, y=865)
        sleep(800, 900)
        pydirectinput.click(x=1010, y=865, button="left")
        sleep(800, 900)
    # Berserker Mayhem
    if  _curr["class"] == "berserker":
        pydirectinput.press(config["Specialty1"])
        sleep(800, 900)
        
        
    # delayed start for better aoe abiltiy usage at floor1 beginning
    if config["delayedStart"] != None:
        sleep(config["delayedStart"] - 100, config["delayedStart"] + 100)
    
    while True:
        result = useAbilities()
        if result == "portal":
            break
        
def quitChaos():
    """
    Quit chaos dungeon
    """
    # 
    checkChaosFinishSplashScreen()
    sleep(100, 200)
    while True:
        leaveButton = Checks.locateCenterOnScreen(
            config["ScreenshotsPath"] + "leave.png",
            grayscale=True,
            confidence=0.7,
            region=config["regions"]["leaveMenu"],
        )
        if leaveButton != None:
            x, y = leaveButton
            mouseMoveTo(x=x, y=y)
            sleep(500, 600)
            pydirectinput.click(button="left")
            sleep(200, 300)
        else:
            # incity check
            inTown = Checks.inCityCheck()
            if inTown != None:
                Settings.states["status"] = "inCity"
                prGreen("Status: inCity")
                return
        sleep(300, 400)
        # leave ok
        okButton = Checks.okCheck()
        if okButton != None:
            x, y = okButton
            mouseMoveTo(x=x, y=y)
            sleep(200, 300)
            pydirectinput.click(button="left")
            sleep(100, 200)
            pydirectinput.click(button="left")
            sleep(100, 200)
            mouseMoveTo(x=x, y=y)
            sleep(200, 300)
            pydirectinput.click(button="left")
            sleep(100, 200)
            pydirectinput.click(button="left")
            break
        sleep(300, 400)
    
    Settings.states["status"] = "inCity"
    prGreen("Status: inCity")
    sleep(5000, 7000)
    return

def waitForLoading():
    print("loading")
    blackScreenStartTime = int(time.time_ns() / 1000000)
    while True:
        currentTime = int(time.time_ns() / 1000000)
        if currentTime - blackScreenStartTime > config["blackScreenTimeLimit"]:
            # pyautogui.hotkey("alt", "f4")
            print("alt f4")
            pydirectinput.keyDown("alt")
            sleep(350, 400)
            pydirectinput.keyDown("f4")
            sleep(350, 400)
            pydirectinput.keyUp("alt")
            sleep(350, 400)
            pydirectinput.keyUp("f4")
            sleep(350, 400)
            sleep(10000, 15000)
            return
        leaveButton = Checks.locateCenterOnScreen(
            config["ScreenshotsPath"] + 
            "leave.png",
            grayscale=True,
            confidence=0.7,
            region=config["regions"]["leaveMenu"],
        )
        if leaveButton != None:
            return
        sleep(350, 400)

def checkChaosFinishSplashScreen():
    """Check if chaos dungeon is finished and click on ok button if it is"""
    clearOk = Checks.clearOkCheck()
    if clearOk != None:
        if Settings.DEBUG:
            prCyan("Clear Ok")
        x, y = clearOk
        mouseMoveTo(x=x, y=y)
        sleep(800, 900)
        pydirectinput.click(x=x, y=y, button="left")
        sleep(200, 300)
        mouseMoveTo(x=x, y=y)
        sleep(600, 800)
        pydirectinput.click(x=x, y=y, button="left")
        sleep(200, 300)
        return True
    if Settings.DEBUG:
        prCyan("No Clear Ok")
    return False

def SelectChaosLevel():
    """Select chaos dungeon level"""
    _curr = config["characters"][Settings.states["currentCharacter"]]
    chaosTabPosition = {
        # punika
        1100: [[1113, 307], [524, 400]],
        1310: [[1113, 307], [524, 455]],
        1325: [[1113, 307], [524, 505]],
        1340: [[1113, 307], [524, 555]],
        1355: [[1113, 307], [524, 605]],
        1370: [[1113, 307], [524, 662]],
        1385: [[1113, 307], [524, 715]],
        1400: [[1113, 307], [524, 770]],
        # south vern
        1415: [[1066, 307], [524, 400]],
        1445: [[1066, 307], [524, 455]],
        1475: [[1066, 307], [524, 505]],
        1490: [[1066, 307], [524, 555]],
        1520: [[1066, 307], [524, 605]],
        1540: [[1066, 307], [524, 662]],
        1560: [[1066, 307], [524, 715]],
        # elgacia
        1580: [[1210, 307], [524, 400]],
        1600: [[1210, 307], [524, 455]],
        # voldis
        1610: [[1355, 307], [524, 400]],
    }
    
    mouseMoveTo(
        x=chaosTabPosition[_curr["ilvl-aor"]][0][0],
        y=chaosTabPosition[_curr["ilvl-aor"]][0][1],
    )
    sleep(800, 900)
    pydirectinput.click(
        x=chaosTabPosition[_curr["ilvl-aor"]][0][0],
        y=chaosTabPosition[_curr["ilvl-aor"]][0][1],
        button="left",
    )
    sleep(500, 600)
    pydirectinput.click(
        x=chaosTabPosition[_curr["ilvl-aor"]][0][0],
        y=chaosTabPosition[_curr["ilvl-aor"]][0][1],
        button="left",
    )
    sleep(500, 600)
    mouseMoveTo(
        x=chaosTabPosition[_curr["ilvl-aor"]][1][0],
        y=chaosTabPosition[_curr["ilvl-aor"]][1][1],
    )
    sleep(800, 900)
    pydirectinput.click(
        x=chaosTabPosition[_curr["ilvl-aor"]][1][0],
        y=chaosTabPosition[_curr["ilvl-aor"]][1][1],
        button="left",
    )
    sleep(500, 600)
    pydirectinput.click(
        x=chaosTabPosition[_curr["ilvl-aor"]][1][0],
        y=chaosTabPosition[_curr["ilvl-aor"]][1][1],
        button="left",
    )
    sleep(500, 600)

def clearQuest():
    quest = Checks.locateCenterOnScreen(
        config["ScreenshotsPath"] + "quest.png", confidence=0.9, region=(815, 600, 250, 200)
    )
    leveledup = Checks.locateCenterOnScreen(
        config["ScreenshotsPath"] + "leveledup.png", confidence=0.9, region=(815, 600, 250, 200)
    )
    gameMenu = Checks.locateCenterOnScreen(
        config["ScreenshotsPath"] + "gameMenu.png",
        confidence=0.95,
        region=config["regions"]["center"],
    )
    if gameMenu != None:
        if Settings.DEBUG:
            prCyan("Clear Game Menu")
        pydirectinput.press("esc")
        sleep(1800, 1900)
    if quest != None:
        if Settings.DEBUG:
            prCyan("Clear Quest")
        x, y = quest
        mouseMoveTo(x=x, y=y)
        sleep(1800, 1900)
        pydirectinput.click(x=x, y=y, button="left")
        sleep(1800, 1900)
        pydirectinput.press("esc")
        sleep(1800, 1900)
    elif leveledup != None:
        if Settings.DEBUG:
            prCyan("Clear Leveled Up")
        x, y = leveledup
        mouseMoveTo(x=x, y=y)
        sleep(1800, 1900)
        pydirectinput.click(x=x, y=y, button="left")
        sleep(1800, 1900)
        pydirectinput.press("esc")
        sleep(1800, 1900)

def doAuraRepair(forced):
    # Check if repair needed
    if forced or Checks.locateCenterOnScreen(
        "./screenshots/repair.png",
        grayscale=True,
        confidence=0.4,
        region=(1500, 134, 100, 100),
    ):
        print("repairing")
        input.shortcut(config["Shortcut-Pet"])
        sleep(2500, 2600)
        mouseMoveTo(x=1142, y=661)
        sleep(2500, 2600)
        pydirectinput.click(1142, 661, button="left")
        sleep(5500, 5600)
        mouseMoveTo(x=1054, y=455)
        sleep(2500, 2600)
        pydirectinput.click(1054, 455, button="left")
        sleep(2500, 2600)
        pydirectinput.press("esc")
        sleep(2500, 2600)
        pydirectinput.press("esc")
        sleep(2500, 2600)

def useAbilities():
    Checks.diedCheck()
    Checks.healthCheck()
    
    if (Settings.states["status"] == "floor1" or Settings.states["status"] == "floor2") and Checks.checkPortal():
        calculateMinimapRelative(Settings.states["moveToX"], Settings.states["moveToY"])
        enterPortal()
        return "portal"
    
    allA = [*range(0, len(Settings.states["abilityScreenshots"]))]
    for i in allA:
        checkCDandCast(Settings.states["abilityScreenshots"][i])

def checkCDandCast(ability):
    if (Checks.locateCenterOnScreen(ability["image"], region=config["regions"]["abilities"])):
        if ability["directional"] == True:
            mouseMoveTo(x=Settings.states["moveToX"], y=Settings.states["moveToY"])
        else:
            mouseMoveTo(x=config["screenCenterX"], y=config["screenCenterY"])
        sleep(50, 60)

        if ability["cast"]:
            start_ms = int(time.time_ns() / 1000000)
            now_ms = int(time.time_ns() / 1000000)
            # spam until cast time before checking cd, to prevent 击倒后情况
            while now_ms - start_ms < ability["castTime"]:
                pydirectinput.press(ability["key"])
                sleep(50, 60)
                now_ms = int(time.time_ns() / 1000000)
            # while pyautogui.locateOnScreen(
            #     ability["image"], region=config["regions"]["abilities"]
            # ):
            #     pydirectinput.press(ability["key"])
        elif ability["hold"]:
            # TODO: FIXME: avoid hold for now...
            start_ms = int(time.time_ns() / 1000000)
            now_ms = int(time.time_ns() / 1000000)
            pydirectinput.keyDown(ability["key"])
            while now_ms - start_ms < ability["holdTime"]:
                # pydirectinput.keyDown(ability["key"])
                now_ms = int(time.time_ns() / 1000000)
            # while pyautogui.locateOnScreen(
            #     ability["image"], region=config["regions"]["abilities"]
            # ):
            #     pydirectinput.keyDown(ability["key"])
            pydirectinput.keyUp(ability["key"])
        else:
            # 瞬发 ability
            pydirectinput.press(ability["key"])
            start_ms = int(time.time_ns() / 1000000)
            now_ms = int(time.time_ns() / 1000000)
            while Checks.locateCenterOnScreen(
                ability["image"],
                region=config["regions"]["abilities"],
            ):
                pydirectinput.press(ability["key"])
                sleep(50, 60)
                now_ms = int(time.time_ns() / 1000000)
                if now_ms - start_ms > 15000:
                    print("unable to use spell for 15s, check if disconnected")
                    return

def enterPortal():
    # repeatedly move and press g until black screen
    sleep(1100, 1200)
    print("moving to portal x: {} y: {}".format(Settings.states["moveToX"], Settings.states["moveToY"]))
    print("move for {} ms".format(Settings.states["moveTime"]))
    if Settings.states["moveTime"] > 550:
        print("blink")
        pydirectinput.click(
            x=Settings.states["moveToX"], y=Settings.states["moveToY"], button=config["move"]
        )
        sleep(100, 150)
        pydirectinput.press(config["blink"])

    enterTime = int(time.time_ns() / 1000000)
    while True:
        # try to enter portal until black screen
        im = pyautogui.screenshot(region=(1652, 168, 240, 210))
        r, g, b = im.getpixel((1772 - 1652, 272 - 168))
        # print(r + g + b)
        if r + g + b < 60:
            print("portal entered")
            mouseMoveTo(x=config["screenCenterX"], y=config["screenCenterY"])
            return True

        nowTime = int(time.time_ns() / 1000000)
        falseTime = 6000
        if nowTime - enterTime > falseTime:
            # clear mobs a bit with first spell before scanning for portal again
            pydirectinput.press(Settings.states["abilityScreenshots"][0]["key"])
            sleep(100, 150)
            pydirectinput.press(config["meleeAttack"])
            sleep(100, 150)
            return False
        # hit move and press g
        if (
            Settings.states["moveToX"] == config["screenCenterX"]
            and Settings.states["moveToY"] == config["screenCenterY"]
        ):
            pydirectinput.press(config["interact"])
            sleep(100, 120)
        else:
            pydirectinput.press(config["interact"])
            pydirectinput.click(
                x=Settings.states["moveToX"], y=Settings.states["moveToY"], button=config["move"]
            )
            sleep(60, 70)

def calculateMinimapRelative(x, y):
    selfLeft = config["minimapCenterX"]
    selfTop = config["minimapCenterY"]
    # if abs(selfLeft - x) <= 3 and abs(selfTop - y) <= 3:
    #     states["moveToX"] = config["screenCenterX"]
    #     states["moveToY"] = config["screenCenterY"]
    #     return

    x = x - selfLeft
    y = y - selfTop
    distBtwPoints = math.sqrt(x * x + y * y)
    Settings.states["moveTime"] = int(distBtwPoints * 16)

    dist = 200
    if y < 0:
        dist = -dist

    if x == 0:
        if y < 0:
            newY = y - abs(dist)
        else:
            newY = y + abs(dist)
        # print("relative to center pos newX: 0 newY: {}".format(int(newY)))
        Settings.states["moveToX"] = 0 + config["screenCenterX"]
        Settings.states["moveToY"] = int(newY) + config["screenCenterY"]
        return
    if y == 0:
        if x < 0:
            newX = x - abs(dist)
        else:
            newX = x + abs(dist)
        # print("relative to center pos newX: {} newY: 0".format(int(newX)))
        Settings.states["moveToX"] = int(newX) + config["screenCenterX"]
        Settings.states["moveToY"] = 0 + config["screenCenterY"]
        return

    k = y / x
    # newX = x + dist
    newY = y + dist
    # newY = k * (newX - x) + y
    newX = (newY - y) / k + x

    # print("before confining newX: {} newY: {}".format(int(newX), int(newY)))
    if newX < 0 and abs(newX) > config["clickableAreaX"]:
        newX = -config["clickableAreaX"]
        if newY < 0:
            newY = newY + abs(dist) * 0.25
        else:
            newY = newY - abs(dist) * 0.25
    elif newX > 0 and abs(newX) > config["clickableAreaX"]:
        newX = config["clickableAreaX"]
        if newY < 0:
            newY = newY + abs(dist) * 0.25
        else:
            newY = newY - abs(dist) * 0.25

    if newY < 0 and abs(newY) > config["clickableAreaY"]:
        newY = -config["clickableAreaY"]
        if newX < 0:
            newX = newX + abs(dist) * 0.7
        else:
            newX = newX - abs(dist) * 0.7
    elif newY > 0 and abs(newY) > config["clickableAreaY"]:
        newY = config["clickableAreaY"]
        if newX < 0:
            newX = newX + abs(dist) * 0.7
        else:
            newX = newX - abs(dist) * 0.7

    # print(
    #     "after confining relative to center pos newX: {} newY: {}".format(
    #         int(newX), int(newY)
    #     )
    # )
    Settings.states["moveToX"] = int(newX) + config["screenCenterX"]
    Settings.states["moveToY"] = int(newY) + config["screenCenterY"]
    return

if __name__ == "__main__":
    prGreen("Chaos Script Running")
    Settings.init()
    if os.environ.get("DEBUG"):
        Settings.DEBUG = True
        prCyan("DEBUG Mode is on")
    
    enterChaosfromContentList()
    waitForLoading()
    saveAbilitiesScreenshots()
    doFloor1()
    