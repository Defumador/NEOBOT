# encoding: utf-8
import time
import sys
import random
import logging

import pyautogui as pag

from src import keyboard, locate as lo
from src.vars import originx, originy, windowx, windowy

sys.setrecursionlimit(9999999)


def activate_miners(module_num):
    """Activates mining modules based on the number passed to this function.
    If the module is out of range, script will try to wait until ship gets
    within range before activating any more modules."""
    for n in range(1, (module_num + 1)):
        keyboard.keypress('f' + (str(n)))
        logging.debug('activating miner ' + (str(n)))
        out_of_range = miner_out_of_range_popup()
        tries = 0
        while out_of_range == 1 and tries <= 25:
            tries += 1
            time.sleep(float(random.randint(15000, 30000)) / 1000)
            out_of_range = miner_out_of_range_popup()
            if out_of_range == 0 and tries <= 25:
                time.sleep(float(random.randint(0, 3000)) / 1000)
                logging.debug('activating miner ' + (str(n)))
                keyboard.keypress('f' + (str(n)))
        if out_of_range == 0 and tries <= 25:
            continue
        elif out_of_range == 1 and tries > 25:
            logging.error('timed out waiting for ship to get within '
                          'module range')
            return 0
    return 1


def no_object_selected_indicator(haystack=0):
    """Checks if the 'selected item' window displays 'no object selected,
    ' this could be useful in the rare case in which an asteroid is destroyed
    but no 'asteroid depleted' popup appears."""
    # For evidence of an asteroid being destroyed with no 'asteroid depleted'
    # popup, see 2019-07-20_15-23-06 at 2h53m58s
    no_object = lo.hslocate('./img/indicators/no_object_selected.bmp', haystack=haystack, conf=0.9)
    if no_object != 0:
        logging.info('target no longer exists')
        return 1
    elif no_object == 0:
        logging.debug('target still exists')
        return 0


def asteroid_depleted_popup(haystack=0):
    """Checks for popup indicating the asteroid currently being mined has been
    depleted."""
    depleted = lo.hslocate('./img/popups/asteroid_depleted.bmp', haystack=haystack, conf=0.9)
    if depleted != 0:
        logging.debug('asteroid empty')
        return 1
    elif depleted == 0:
        logging.debug('asteroid still available')
        return 0


def ship_full_popup(haystack=0):
    """Checks for momentary popup indicating that the ship's inventory is full.
    This popup lasts about 5 seconds."""
    ship_full = lo.hslocate('./img/popups/ship_inv_full.bmp', haystack=haystack, conf=0.9)
    if ship_full != 0:
        logging.info('inventory full')
        return 1
    elif ship_full == 0:
        logging.debug('inventory not yet full')
        return 0


def miner_out_of_range_popup():
    """Checks if the ship's mining laser is out of range. If it is,
    orbit the asteroid at a specified distance and try activating the
    mining laser again in a few seconds."""
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


def time_at_site(timer_var):
    """Timeout timer for mining. If, for some reason, ship gets stuck in
    belt, the timer can be used to restart the script after a certain period of
    time."""
    logging.debug('time spent at site is ' + (str(timer_var)) + 's')
    if timer_var >= 800:
        logging.warning('timed out!')
        return 1
    elif timer_var < 800:
        return 0
