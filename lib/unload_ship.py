import sys
import time
import random
import logging
import pyautogui as pag
from lib import mouse, keyboard, docked, locate as lo
from lib.vars import originx, originy, windowx, windowy, conf

sys.setrecursionlimit(9999999)

logging.basicConfig(format='(%(levelno)s) %(asctime)s - %(funcName)s -- %('
                           'message)s', level=logging.DEBUG)


def drag_items_from_ship_inv():
    # Click and drag all items from ship inventory to station inventory.
    (x1, y1) = lo.clocate('./img/indicators/station_inv_name.bmp')
    (x2, y2) = lo.clocate('./img/buttons/station_inv.bmp')
    
    pag.moveTo((x1 + (random.randint(-5, 250))),
               (y1 + (random.randint(10, 25))),
               mouse.duration(), mouse.path())
    time.sleep(float(random.randint(0, 1000)) / 1000)
    pag.mouseDown()
    time.sleep(float(random.randint(0, 1000)) / 1000)
    pag.moveTo((x2 + (random.randint(-15, 60))),
               (y2 + (random.randint(-10, 10))),
               mouse.duration(), mouse.path())
    time.sleep(float(random.randint(0, 1000)) / 1000)
    pag.mouseUp()
    logging.debug('moved all item stacks from ship inventory')
    return


def unload_ship():
    logging.debug('began unloading procedure')
    docked.open_ship_inv()
    items = docked.detect_items()

    if items == 1:
        time.sleep(float(random.randint(0, 2000)) / 1000)
        docked.focus_inv_window()
        time.sleep(float(random.randint(0, 2000)) / 1000)
        keyboard.hotkey('ctrl','a')
        time.sleep(float(random.randint(0, 2000)) / 1000)
        drag_items_from_ship_inv()
        time.sleep(2)
        items = docked.detect_items()

    if items == 0:
        logging.debug('finished unloading main inventory')
        
        specinv_list = ['ore','fleet']
        for invtype in specinv_list:
            if docked.detect_spec_inv(invtype) == 1:
                time.sleep(float(random.randint(0, 2000)) / 1000)
                docked.open_spec_inv_ore(invtype)
                items = docked.detect_items()
                
                while items == 1:
                    time.sleep(float(random.randint(0, 2000)) / 1000)
                    docked.focus_inv_window()
                    time.sleep(float(random.randint(0, 2000)) / 1000)
                    keyboard.hotkey('ctrl','a')
                    time.sleep(float(random.randint(0, 2000)) / 1000)
                    drag_items_from_ship_inv()
                    time.sleep(float(random.randint(0, 2000)) / 1000)
                    items == docked.detect_items()
                    logging.debug('finished unloading' + (str(invtype)) + 'inventory')
                    return 1
                if items == 0:
                    logging.debug('finished unloading procedure')
                    return 1

            elif docked.detect_spec_inv(invtype) == 0:
                logging.debug('finished unloading procedure')
                return 1
