import time
import sys
import random

import pyautogui as pag

from lib import keyboard, mouse
from lib.overview import detect_target_lock, target_available
from lib.vars import originx, originy, windowx, windowy

sys.setrecursionlimit(9999999)

# The number of mining modules the ship has.
mining_lasers = 2

# FOR FUTURE USE, MINING ORES BY PRIORITY
# The ores to mine, in order of priority. A lower value is higher priority.
# plagioclase = 1
# scordite = 4
# pyroxeres = 2
# veldspar = 3
## Sort the ores into a dictionary.
# ores_dict = {1: "plagioclase", 2: "pyroxeres", 3: "scordite", 4: "veldspar"}

# Set which ores to mine. 1 is yes, 0 is no.
plagioclase = 1
scordite = 0
veldspar = 0
pyroxeres = 1


def activate_miner():
    # Activate mining lasers in sequential order.
    if mining_lasers == 1:
        keyboard.keypress('f1')
        while miner_out_of_range_popup() == 1:
            time.sleep(float(random.randint(10000, 20000)) / 1000)
            activate_miner()
        return 1

    elif mining_lasers == 2:
        keyboard.keypress('f1')
        while miner_out_of_range_popup() == 1:
            time.sleep(float(random.randint(10000, 20000)) / 1000)
            keyboard.keypress('f1')
        else:
            print('pressing f2')
            keyboard.keypress('f2')
            return 1

    elif mining_lasers == 3:
        keyboard.keypress('f1')
        while miner_out_of_range_popup() == 1:
            time.sleep(float(random.randint(10000, 20000)) / 1000)
            keyboard.keypress('f1')
        else:
            keyboard.keypress('f2')
            keyboard.keypress('f3')
            return 1

    elif mining_lasers == 4:
        keyboard.keypress('f1')
        while miner_out_of_range_popup() == 1:
            time.sleep(float(random.randint(10000, 20000)) / 1000)
            keyboard.keypress('f1')
        else:
            keyboard.keypress('f2')
            keyboard.keypress('f3')
            keyboard.keypress('f4')
            return 1
    print('activate_mining_laser -- called')
    return 1


def asteroid_depleted_popup():
    # Check for popup indicating the asteroid currently being mined has been
    # depleted.
    print('asteroid_depleted_popup -- not detected')
    return 0


'''
asteroid_depleted_popup_var = pag.locateCenterOnScreen(
    './img/overview/asteroid_depleted.bmp',
    confidence=0.90,
    region=(originx, originy, windowx, windowy))
if asteroid_depleted_popup_var is None:
    return 0
elif asteroid_depleted_popup_var is not None:
    print('asteroid_depleted_popup -- detected')
    return 1
'''


def detect_ore():
    # Target asteroids based on ore rather than size.
    global plagioclase, pyroxeres, scordite, veldspar

    # Capture the overview to locate ore types
    overview = pag.screenshot(
        region=((originx + (windowx - (int(windowx / 3.8)))),
                originy, (int(windowx / 3.8)), windowy))

    ore_list = []
    # Populate ore_list with only the ore types that the user wishes to
    # check for, as specified by the variables at the top of this file.
    if pyroxeres == 1:
        ore_list.append('./img/overview/ore_types/plagioclase.bmp')
    if plagioclase == 1:
        ore_list.append('./img/overview/ore_types/pyroxeres.bmp')
    if scordite == 1:
        ore_list.append('./img/overview/ore_types/scordite.bmp')
    if veldspar == 1:
        ore_list.append('./img/overview/ore_types/veldspar.bmp')

    # Iterate through ore_list until an ore is found.
    for ore_type in ore_list:
        global ore_found
        ore_found = pag.locate(ore_type, overview, confidence=0.92)
        if ore_found is not None:
            print('found ore at', ore_found)
            (x, y, l, w) = ore_found
            pag.moveTo((x + (originx + (windowx - (int(windowx / 3.8))))),
                       (y + originy),
                       1, mouse.path())
            return 1
        else:
            print('detect_ore -- no more ore to mine')
            return 0


def inv_full_popup():
    # Check for momentary popup indicating cargo/ore hold is full.
    # This popup lasts about 5 seconds.
    inv_full_popup_var = pag.locateCenterOnScreen(
        './img/popups/ship_inv_full.bmp',
        confidence=0.9,
        region=(originx, originy,
                windowx, windowy))
    if inv_full_popup_var is None:
        print('inv_full_popup -- not detected')
        return 0
    elif inv_full_popup_var is not None:
        print('inv_full_popup -- detected')
        return 1


def miner_out_of_range_popup():
    # Check if the ship's mining laser is out of range. If it is,
    # orbit the asteroid at a specified distance and try activating the
    # mining laser again in a few seconds.
    miner_out_of_range = pag.locateCenterOnScreen(
        './img/popups/miner_out_of_range.bmp',
        confidence=0.90,
        region=(originx, originy, windowx, windowy))
    while miner_out_of_range is not None:
        print('miner_out_of_range_popup -- out of module range')
        return 1
    if miner_out_of_range is None:
        print('miner_out_of_range_popup -- in module range')
        return 0


def target_ore():
    # Target the closest user-defined ore in overview, assuming overview is
    # sorted by distance, with closest objects at the top.
    # Switch to mining tab, target asteroid, then switch back to general tab.
    global ore_found

    if ore_found is not None:
        # Break apart ore_found tuple into coordinates
        (x, y, l, w) = ore_found
        # Adjust coordinates for screen
        x = (x + (originx + (windowx - (int(windowx / 3.8)))))
        y = (y + originy)
        pag.moveTo((x + (random.randint(-100, 20))),
                   (y + (random.randint(-3, 3))),
                   mouse.duration(), mouse.path())
        mouse.click()
        keyboard.keypress('w')
        if target_available() == 0:
            time.sleep(float(random.randint(500, 1000)) / 1000)
            print('target_ore -- getting closer to target')
            time.sleep(float(random.randint(1000, 5000)) / 1000)
            tries = 0
            while target_available() == 0 and tries <= 30:
                time.sleep(10)
            if target_available() == 0 and tries > 30:
                print('target_ore -- timed out getting closer to target')
                return 0
        if target_available() == 1:
            keyboard.keypress('ctrl')
            time.sleep(float(random.randint(1000, 2000)) / 1000)
            print('target_ore -- locking target')
            if detect_target_lock() == 1:
                return 1
            elif detect_target_lock() == 0:
                return 0
    else:
        print('target_ore -- no asteroids to target')
        return 0
