import time
import sys
import random
import logging

import pyautogui as pag

from lib import keyboard, mouse
from lib.overview import detect_target_lock, target_available
from lib.vars import originx, originy, windowx, windowy

sys.setrecursionlimit(9999999)

# The number of mining modules the ship has.
mining_lasers = 2

# Set which ores to mine. 1 is yes, 0 is no.
plagioclase = 1
scordite = 0
veldspar = 0
pyroxeres = 1
# need to add these ores
kernite = 0
morphite = 0
bistot = 0
arkonor = 0
crokite = 0
jaspet = 0
omber = 0
ochre = 0
gneiss = 0
hedbergite = 0
hemorphite = 0
mercoxit = 0

# Specify the target names you wish the script to search for in the Overview.
# For mining, this would be ore types.
target1 = './img/overview/ore_types/plagioclase.bmp'
target2 = './img/overview/ore_types/pyroxeres.bmp'
target3 = './img/overview/ore_types/veldspar.bmp'
target4 = './img/overview/ore_types/scordite.bmp'
target5 = 0

logging.basicConfig(format='(%(levelno)s) %(asctime)s - %(funcName)s -- %('
                           'message)s', level=logging.DEBUG)


def activate_miner():
    # Activate mining lasers in sequential order.
    if mining_lasers == 1:
        keyboard.keypress('f1')
        logging.debug('activating miner 1')
        while miner_out_of_range_popup() == 1:
            time.sleep(float(random.randint(10000, 20000)) / 1000)
            activate_miner()
        return 1

    elif mining_lasers == 2:
        keyboard.keypress('f1')
        logging.debug('activating miner 1')
        while miner_out_of_range_popup() == 1:
            time.sleep(float(random.randint(10000, 20000)) / 1000)
            keyboard.keypress('f1')
        else:
            keyboard.keypress('f2')
            logging.debug('activating miner 2')
            return 1

    elif mining_lasers == 3:
        keyboard.keypress('f1')
        logging.debug('activating miner 1')
        while miner_out_of_range_popup() == 1:
            time.sleep(float(random.randint(10000, 20000)) / 1000)
            keyboard.keypress('f1')
        else:
            keyboard.keypress('f2')
            logging.debug('activating miner 2')
            keyboard.keypress('f3')
            logging.debug('activating miner 3')
            return 1

    elif mining_lasers == 4:
        keyboard.keypress('f1')
        logging.debug('activating miner 1')
        while miner_out_of_range_popup() == 1:
            time.sleep(float(random.randint(10000, 20000)) / 1000)
            keyboard.keypress('f1')
        else:
            keyboard.keypress('f2')
            logging.debug('activating miner 2')
            keyboard.keypress('f3')
            logging.debug('activating miner 3')
            keyboard.keypress('f4')
            logging.debug('activating miner 4')
            return 1
    return 1


def asteroid_depleted_popup():
    # Check for popup indicating the asteroid currently being mined has been
    # depleted.
    logging.debug('asteroid still available')
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


def detect_overview_item():
    # Target asteroids based on ore rather than size.
    global plagioclase, pyroxeres, scordite, veldspar

    # Capture the overview to locate ore types
    overview = pag.screenshot(
        region=((originx + (windowx - (int(windowx / 3.8)))),
                originy, (int(windowx / 3.8)), windowy))

    target_list = []
    # Populate ore_list with only the ore types that the user wishes to
    # check for, as specified by the variables at the top of this file.
    if target1 != 0:
        target_list.append(target1)
    if target2 != 0:
        target_list.append(target2)
    if target3 != 0:
        target_list.append(target3)
    if target4 != 0:
        target_list.append(target4)

    # Iterate through ore_list until an ore is found.
    for item in target_list:
        #global ore_found
        item = pag.locate(ore_type, overview, confidence=0.92)
        if item is not None:
            logging.debug('found target at ' + (str(item)))
            (x, y, l, w) = item
            pag.moveTo((x + (originx + (windowx - (int(windowx / 3.8))))),
                       (y + originy),
                       1, mouse.path())
            return item
        else:
            logging.info('no more ore available in belt')
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
        logging.debug('inventory not yet full')
        return 0
    elif inv_full_popup_var is not None:
        logging.info('inventory full')
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
        logging.debug('out of module range')
        return 1
    if miner_out_of_range is None:
        logging.debug('within module range')
        return 0


def timer(timer_var):
    # Timeout timer for mining. If, for some reason, miner gets stuck in
    # belt, restart script after a certain period of time.
    logging.debug('time spent at site is ' + (str(timer_var)) + 's')
    if timer_var >= 800:
        logging.warning('timed out!')
        return 1
    elif timer_var < 800:
        return 0


def target_overview_item():
    '''
    Targets the closest user-defined item in the Overview, assuming overview is
    sorted by distance, with closest objects at the top.
    '''
    if detect_overview_item() is not None:
        # Break apart ore_found tuple into coordinates
        (x, y, l, w) = detect_overview_item
        # Adjust coordinates for screen
        x = (x + (originx + (windowx - (int(windowx / 3.8)))))
        y = (y + originy)
        pag.moveTo((x + (random.randint(-100, 20))),5
                   (y + (random.randint(-3, 3))),
                   mouse.duration(), mouse.path())
        mouse.click()
        keyboard.keypress('w')
        tries = 0
        while target_available() == 0 and tries <= 30:
            time.sleep(float(random.randint(1000, 2000)) / 1000)
            tries += 1
            logging.debug('target not yet within range ' + (str(tries)))
        if target_available() == 1 and tries <= 30:
            logging.debug('locking target')
            keyboard.keypress('ctrl')
            if detect_target_lock() == 1:
                return 1
            elif detect_target_lock() == 0:
                return 0
        elif target_available() == 0 and tries > 30:
            logging.warning('timed out waiting for target to get within range!')
            return 0
    else:
        logging.info('no targets available')
        return 0
