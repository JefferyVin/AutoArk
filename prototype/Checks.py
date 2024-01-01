import pyautogui
from tools import sleep
import Checks
from input import mouseMoveTo
from config import config
import pydirectinput
import Settings
import time
import colorprint
import os
import math

def locateCenterOnScreen(*args, **kwargs):
    try:
        return pyautogui.locateCenterOnScreen(*args, **kwargs)
    except pyautogui.ImageNotFoundException:
        return None
    
def locateOnScreen(*args, **kwargs):
    try:
        return pyautogui.locateOnScreen(*args, **kwargs)
    except pyautogui.ImageNotFoundException:
        return None
    
def inChaosCheck():
    return locateCenterOnScreen(
        config["ScreenshotsPath"] + "inChaos.png",
        confidence=0.9,
        region=(247, 146, 222, 50),
    )

def inCityCheck():
    return locateCenterOnScreen(
        config["ScreenshotsPath"] + "inCity.png",
        confidence=0.75,
        region=(1870, 133, 25, 30),
    )
    
def AuraOfResonanceCheck():
    return locateCenterOnScreen(
        config["ScreenshotsPath"] + "aor.png",
        confidence=0.8, 
        region=(592, 304, 192, 95)
    )

def offlineCheck():
    return False

def gameCrashCheck():
    return False

def DetectBlackScreen():
    blackScreenStartTime = int(time.time_ns() / 1000000)
    if Settings.DEBUG:
        colorprint.prCyan('Waiting for Black Screen to end...')
    while True:
        im = pyautogui.screenshot(region=(1652, 168, 240, 210))
        r, g, b = im.getpixel((1772 - 1652, 272 - 168))
        if r + g + b > 10:
            if os.environ.get('DEBUG'):
                currentTime = int(time.time_ns() / 1000000)
                colorprint.prCyan('Blackscreen ended in ' + str((currentTime - blackScreenStartTime)) + 'ms')
            break
        sleep(200, 300)

        currentTime = int(time.time_ns() / 1000000)
        if currentTime - blackScreenStartTime > config["blackScreenTimeLimit"]:
            
            # pydirectinput.keyDown("alt")
            # sleep(350, 400)
            # pydirectinput.press("f4")
            # sleep(350, 400)
            # pydirectinput.keyUp("alt")
            
            colorprint.prRed("Alt-F4'd due to long black screen time (Change config.py-blackScreenTimeLimit if its too short)")
            sleep(10000, 15000)
            return
    sleep(600, 800)

def checkTimeout():
    currentTime = int(time.time_ns() / 1000000)
    # hacky way of quitting
    if Settings.states["instanceStartTime"] == -1:
        print("hacky timeout")
        return True
    if (
        Settings.states["multiCharacterMode"] == False
        and currentTime - Settings.states["instanceStartTime"] > config["timeLimit"]
    ):
        print("timeout triggered")
        timeout = pyautogui.screenshot()
        timeout.save("./debug/timeout_" + str(currentTime) + ".png")
        Settings.states["timeoutCount"] = Settings.states["timeoutCount"] + 1
        return True
    elif (
        Settings.states["multiCharacterMode"] == True
        and Settings.states["floor3Mode"] == True
        and currentTime - Settings.states["instanceStartTime"] > config["timeLimitAor"]
    ):
        print("timeout on aor triggered :(")
        timeout = pyautogui.screenshot()
        timeout.save("./debug/timeout_aor_" + str(currentTime) + ".png")
        Settings.states["timeoutCount"] = Settings.states["timeoutCount"] + 1
        return True
    return False

def okCheck():
    return locateCenterOnScreen(
            config["ScreenshotsPath"] + "ok.png",
            confidence=0.75,
            region=config["regions"]["center"],
        )

def clearOkCheck():
    return locateCenterOnScreen(
        config["ScreenshotsPath"] + "clearOk.png", confidence=0.75, region=(625, 779, 500, 155)
    )

def diedCheck():  # get information about wait a few second to revive
    if locateCenterOnScreen(
        config["ScreenshotsPath"] + "died.png",
        grayscale=True,
        confidence=0.9,
        region=(917, 145, 630, 550),
    ):
        colorprint.prRed("died")
        Settings.states["deathCount"] = Settings.states["deathCount"] + 1
        sleep(500, 1500)
        while (
            locateCenterOnScreen(
                config["ScreenshotsPath"] + "died.png",
                confidence=0.7,
                region=(917, 145, 630, 550),
            )
            != None
        ):
            mouseMoveTo(x=1275, y=454)
            sleep(1600, 1800)
            colorprint.prGreen("Revive clicked")
            pydirectinput.click(1275, 454, button="left")
            sleep(600, 800)
            mouseMoveTo(x=config["screenCenterX"], y=config["screenCenterY"])
            sleep(600, 800)
    return

def healthCheck():
    if config["useHealthPot"] == False:
        return
    x = int(
        config["healthCheckX"]
        + (870 - config["healthCheckX"]) * config["healthPotAtPercent"]
    )
    y = config["healthCheckY"]
    pyautogui.screenshot("healthCheck.png", region=(x+2, y, 1, 1))
    r1, g, b = pyautogui.pixel(x, y)
    r2, g, b = pyautogui.pixel(x - 2, y)
    r3, g, b = pyautogui.pixel(x + 2, y)
    # print(x, r, g, b)
    if r1 < 30 or r2 < 30 or r3 < 30:
        colorprint.prGreen("health pot pressed")
        pydirectinput.press(config["healthPot"])
        Settings.states["healthPotCount"] = Settings.states["healthPotCount"] + 1
        # print(r1, r2, r3)
        leaveButton = locateCenterOnScreen(
            config["ScreenshotsPath"] + "leave.png",
            grayscale=True,
            confidence=0.7,
            region=config["regions"]["leaveMenu"],
        )
        if leaveButton == None:
            return
        return
    return

def checkPortal():
    # check portal image
    portal = locateCenterOnScreen(
        config["ScreenshotsPath"] +
        "portal.png",
        region=config["regions"]["minimap"],
        confidence=0.7,
    )
    portalTop = locateCenterOnScreen(
        config["ScreenshotsPath"] +
        "portalTop.png",
        region=config["regions"]["minimap"],
        confidence=0.7,
    )
    portalBot = locateCenterOnScreen(
        config["ScreenshotsPath"] +
        "portalBot.png",
        region=config["regions"]["minimap"],
        confidence=0.7,
    )
    if portal != None:
        x, y = portal
        Settings.states["moveToX"] = x
        Settings.states["moveToY"] = y
        print(
            "portal image x: {} y: {}".format(Settings.states["moveToX"], Settings.states["moveToY"])
        )
        return True
    elif portalTop != None:
        x, y = portalTop
        Settings.states["moveToX"] = x
        Settings.states["moveToY"] = y + 7
        print(
            "portalTop image x: {} y: {}".format(
                Settings.states["moveToX"], Settings.states["moveToY"]
            )
        )
        return True
    elif portalBot != None:
        x, y = portalBot
        Settings.states["moveToX"] = x
        Settings.states["moveToY"] = y - 7
        print(
            "portalBot image x: {} y: {}".format(
                Settings.states["moveToX"], Settings.states["moveToY"]
            )
        )
        return True
    minimap = pyautogui.screenshot(region=config["regions"]["minimap"])  # Top Right
    width, height = minimap.size
    order = spiralSearch(width, height, math.floor(width / 2), math.floor(height / 2))
    for entry in order:
        if entry[1] >= width or entry[0] >= height:
            continue
        r, g, b = minimap.getpixel((entry[1], entry[0]))
        inRange = False
        inRange = (
            r in range(75, 85) and g in range(140, 150) and b in range(250, 256)
        ) or (
            r in range(120, 130) and g in range(210, 220) and b in range(250, 256)
        )
        if inRange:
            left, top, _w, _h = config["regions"]["minimap"]
            Settings.states["moveToX"] = left + entry[1]
            Settings.states["moveToY"] = top + entry[0]
            if r in range(75, 85) and g in range(140, 150) and b in range(250, 256):
                Settings.states["moveToY"] = Settings.states["moveToY"] - 1
            elif r in range(120, 130) and g in range(210, 220) and b in range(250, 256):
                Settings.states["moveToY"] = Settings.states["moveToY"] + 1
            print(
                "portal pixel x: {} y: {}, r: {} g: {} b: {}".format(
                    Settings.states["moveToX"], Settings.states["moveToY"], r, g, b
                )
            )
            return True
    return False

def spiralSearch(rows, cols, rStart, cStart):
    ans = []  # 可以通过长度来退出返回
    end = rows * cols  # 边界扩张
    i = i1 = i2 = rStart
    # 分别是当前点,上下边界的上边界，下边界
    j = j1 = j2 = cStart  # 当前，左、右边界
    while True:
        j2 += 1
        while j < j2:
            if 0 <= j < cols and 0 <= i:  # i刚减完
                ans.append([i, j])
            j += 1
            if 0 > i:  # i超过了，跳过优化
                j = j2  # 没有答案可添加
        i2 += 1
        while i < i2:
            if 0 <= i < rows and j < cols:
                ans.append([i, j])
            i += 1
            if j >= cols:
                i = i2
        j1 -= 1
        while j > j1:
            if 0 <= j < cols and i < rows:
                ans.append([i, j])
            j -= 1
            if i >= rows:
                j = j1
        i1 -= 1
        while i > i1:
            if 0 <= i < rows and 0 <= j:
                ans.append([i, j])
            i -= 1
            if 0 > j:
                i = i1
        if len(ans) == end:
            return ans

def closeGameByClickingDialogue():
    """
    # ok = pyautogui.locateCenterOnScreen(
    #     "./screenshots/ok.png",
    #     region=config["regions"]["center"],
    # )
    # if ok != None:
    #     x, y = ok
    #     mouseMoveTo(x=x, y=y)
    #     sleep(300, 400)
    #     pydirectinput.click(x=x, y=y, button="left")
    # else:
    #     mouseMoveTo(x=960, y=500)
    #     sleep(300, 400)
    #     pydirectinput.click(button="left")
    """
    while True:
        ok = Checks.locateCenterOnScreen(
            config["ScreenshotsPath"] + "ok.png", region=config["regions"]["center"], confidence=0.75
        )
        enterServer = Checks.locateCenterOnScreen(
            config["ScreenshotsPath"] + "enterServer.png",
            confidence=0.8,
            region=(885, 801, 160, 55),
        )
        if ok != None:
            x, y = ok
            mouseMoveTo(x=x, y=y)
            sleep(300, 400)
            pydirectinput.click(x=x, y=y, button="left")
            print("clicked ok")
        elif enterServer != None:
            break
        else:
            break
        sleep(1300, 1400)
    Settings.states["status"] = "restart"
    sleep(12000, 13000)