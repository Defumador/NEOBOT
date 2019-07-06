import time
import sys
import random

import pyautogui as pag

from lib import keyboard, mouse
from lib.overview import detect_target_lock, target_available
from lib.vars import originx, originy, windowx, windowy

sys.setrecursionlimit(9999999)

mining_lasers = 2


def detect_asteroids():
    # Switch overview to 'mining' tab, check for asteroids, then switch back to
    # the 'general' tab. Prioritize larger asteroids by searching for them
    # first.
    # mining_overview_tab = pag.locateCenterOnScreen(
    # './img/mining_overview_tab.bmp',
    # confidence=0.90,
    # region=(originx, originy, screenwidth, screenheight))
    # general_overview_tab = pag.locateCenterOnScreen(
    # './img/general_overview_tab.bmp', confidence=0.90,
    # region=(originx, originy, screenwidth, screenheight))
    global asteroid_s
    global asteroid_m
    global asteroid_l

    asteroid_m = pag.locateCenterOnScreen('./img/overview/asteroid_m.bmp',
                                          confidence=0.90,
                                          region=((originx + (windowx - (
                                              int(windowx / 3.8)))),
                                                  originy,
                                                  (int(windowx / 3.8)),
                                                  windowy))
    if asteroid_m is not None:
        return 1
    asteroid_l = pag.locateCenterOnScreen('./img/overview/asteroid_l.bmp',
                                          confidence=0.90,
                                          region=((originx + (windowx - (
                                              int(windowx / 3.8)))),
                                                  originy,
                                                  (int(windowx / 3.8)),
                                                  windowy))
    if asteroid_l is not None:
        return 1
    asteroid_s = pag.locateCenterOnScreen('./img/overview/asteroid_s.bmp',
                                          confidence=0.90,
                                          region=((originx + (windowx - (
                                              int(windowx / 3.8)))),
                                                  originy,
                                                  (int(windowx / 3.8)),
                                                  windowy))
    if asteroid_s is not None:
        return 1
    else:
        print('detect_asteroids -- no more asteroids found at site')
    return 0


def target_asteroid():
    # Target the closest large-sized asteroid in overview, assuming overview is
    # sorted by distance, with closest objects at the top.
    # Switch to mining tab, target asteroid, then switch back to general tab.
    global asteroid_s
    global asteroid_m
    global asteroid_l

    if asteroid_m is not None:
        (asteroid_mediumx, asteroid_mediumy) = asteroid_m
        pag.moveTo((asteroid_mediumx + (random.randint(-2, 200))),
                   (asteroid_mediumy + (random.randint(-3, 3))),
                   mouse.duration(), mouse.path())
        mouse.click()
        keyboard.keypress('w')
        if target_available() == 0:
            time.sleep(float(random.randint(500, 1000)) / 1000)
            print('target_asteroid -- getting closer to target')
            time.sleep(float(random.randint(1000, 5000)) / 1000)
            tries = 0
            while target_available() == 0 and tries <= 30:
                time.sleep(10)
            if target_available() == 0 and tries > 30:
                print('target_asteroid -- timed out getting closer to target')
                return 0
        if target_available() == 1:
            keyboard.keypress('ctrl')
            time.sleep(float(random.randint(1000, 2000)) / 1000)
            print('target_asteroid -- locking target')
            detect_target_lock()
            return 1

    elif asteroid_l is not None:
        (asteroid_largex, asteroid_largey) = asteroid_l
        pag.moveTo((asteroid_largex + (random.randint(-2, 200))),
                   (asteroid_largey + (random.randint(-3, 3))),
                   mouse.duration(), mouse.path())
        mouse.click()
        keyboard.keypress('w')
        if target_available() == 0:
            print('target_asteroid -- getting closer to target')
            time.sleep(float(random.randint(1000, 5000)) / 1000)
            # This while loop is required to prevent script from constantly
            # issuing 'orbit' commands.
            tries = 0
            while target_available() == 0 and tries <= 30:
                time.sleep(10)
            if target_available() == 0 and tries > 30:
                print('target_asteroid -- timed out getting closer to target')
                return 0
        if target_available() == 1:
            keyboard.keypress('ctrl')
            time.sleep(float(random.randint(1000, 2000)) / 1000)
            print('target_asteroid -- locking target')
            detect_target_lock()
            return 1

    elif asteroid_s is not None:
        (asteroid_smallx, asteroid_smally) = asteroid_s
        pag.moveTo((asteroid_smallx + (random.randint(-2, 200))),
                   (asteroid_smally + (random.randint(-3, 3))),
                   mouse.duration(), mouse.path())
        mouse.click()
        keyboard.keypress('w')
        if target_available() == 0:
            print('target_asteroid -- getting closer to target')
            time.sleep(float(random.randint(1000, 5000)) / 1000)
            tries = 0
            while target_available() == 0 and tries <= 30:
                time.sleep(10)
            if target_available() == 0 and tries > 30:
                print('target_asteroid -- timed out getting closer to target')
                return 0
        if target_available() == 1:
            keyboard.keypress('ctrl')
            time.sleep(float(random.randint(1000, 2000)) / 1000)
            print('target_asteroid -- locking target')
            detect_target_lock()
            return 1

    else:
        print('target_asteroid -- no asteroids to target')
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
