import sys
import time
import random
import logging
import pyautogui as pag
from lib import mouse, keyboard, docked
from lib.vars import originx, originy, windowx, windowy, conf

sys.setrecursionlimit(9999999)

logging.basicConfig(format='(%(levelno)s) %(asctime)s - %(funcName)s -- %('
                           'message)s', level=logging.DEBUG)


def drag_items_from_ship_inv():
    # Click and drag all items from ship inventory to station inventory.
    namefield_station_inv_icon = pag.locateCenterOnScreen(
        './img/indicators/station_inv_name.bmp',
        confidence=conf,
        region=(originx, originy, windowx, windowy))

    (x, y) = namefield_station_inv_icon
    pag.moveTo((x + (random.randint(-5, 250))),
               (y + (random.randint(10, 25))),
               mouse.duration(), mouse.path())

    pag.mouseDown()
    station_inv = pag.locateCenterOnScreen('./img/buttons/station_inv.bmp',
                                           confidence=conf,
                                           region=(originx, originy,
                                                   windowx, windowy))
    (x, y) = station_inv
    pag.moveTo((x + (random.randint(-15, 60))),
               (y + (random.randint(-10, 10))),
               mouse.duration(), mouse.path())
    pag.mouseUp()
    logging.debug('moved all item stacks from ship inventory')
    return


def unload_ship():
    logging.debug('began unloading procedure')
    docked.open_ship_inv()
    specinv = docked.detect_spec_inv()
    items = docked.detect_items()

    if docked.detect_items() == 0:
        docked.detect_spec_inv()
        if specinv == 1:
            # Wait between 0 and 2s before actions for increased randomness.
            time.sleep(float(random.randint(0, 2000)) / 1000)
            docked.open_spec_inv_ore()
            items = docked.detect_items()

            while items == 1:
                time.sleep(float(random.randint(0, 2000)) / 1000)
                docked.focus_inv_window()
                time.sleep(float(random.randint(0, 2000)) / 1000)
                keyboard.select_all()
                time.sleep(float(random.randint(0, 2000)) / 1000)
                drag_items_from_ship_inv()
                time.sleep(2)
                docked.detect_items()
                logging.debug('finished unloading procedure')
                return 1

            if items == 0:
                logging.debug('finished unloading procedure')
                return 1

        elif specinv == 0:
            logging.warning('nothing to unload')
            return 1

    while items == 1:
        docked.focus_inv_window()
        time.sleep(float(random.randint(0, 2000)) / 1000)
        keyboard.select_all()
        time.sleep(float(random.randint(0, 2000)) / 1000)
        drag_items_from_ship_inv()
        time.sleep(2)
        docked.detect_spec_inv()
        items = docked.detect_items()

    if specinv == 1:
        docked.open_spec_inv_ore()
        items = docked.detect_items()

        while items == 1:
            docked.focus_inv_window()
            time.sleep(float(random.randint(0, 2000)) / 1000)
            keyboard.select_all()
            time.sleep(float(random.randint(0, 2000)) / 1000)
            drag_items_from_ship_inv()
            time.sleep(2)
            docked.detect_items()
            logging.debug('finished unloading procedure')
            return 1

    elif specinv == 0:
        logging.debug('finished unloading procedure')
        return 1
