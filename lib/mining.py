import time
import sys
import random
import logging

import pyautogui as pag

from lib import keyboard
from lib.vars import originx, originy, windowx, windowy

sys.setrecursionlimit(9999999)

# The number of mining modules the ship has.
mining_lasers = 2

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