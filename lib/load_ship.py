import sys
import time
import random
import logging
import traceback
import pyautogui as pag
from lib import mouse, keyboard as key, docked, locate as lo
from lib.vars import originx, originy, windowx, windowy, conf

sys.setrecursionlimit(9999999)

# A return value of 2 indicates the ship has been loaded and the station's
# inventory is empty.

# A return value of 1 indicates the ship has been fully loaded but more items
# remain in the station.

# A return value of 0 indicates the ship cannot be loaded in the manner chosen.


logging.basicConfig(format='(%(levelno)s) %(asctime)s - %(funcName)s -- %('
                           'message)s', level=logging.DEBUG)


def drag_to_ship_inv():
    """Click and drag the first item stack from station's inventory to ship's
    inventory. This function assumed the relevant window is already open."""
    logging.debug('moving item stack to ship inventory')

    station_inv = lo.clocate('./img/indicators/station_inv_name.bmp')
    if station_inv is None:
        logging.critical("can't find name column")
        traceback.print_exc()
        traceback.print_stack()
        sys.exit()

    else:
        tries = 0
        ship_inv = lo.clocate('./img/buttons/ship_inv.bmp')
        while ship_inv is None and tries <= 25:
            tries += 1
            logging.critical("can't find ship inventory")
            time.sleep(float(random.randint(1000, 2000)) / 1000)
            ship_inv = lo.clocate('./img/buttons/ship_inv.bmp')

        if ship_inv is not None and tries <= 25:
            (x, y) = station_inv
            (sx, sy) = ship_inv
            pag.moveTo((x + (random.randint(-5, 250))),
                       (y + (random.randint(10, 25))),
                       mouse.duration(), mouse.path())
            time.sleep(float(random.randint(0, 1000)) / 1000)
            pag.mouseDown()
            time.sleep(float(random.randint(0, 1000)) / 1000)
            pag.moveTo((sx + (random.randint(-5, 60))),
                       (sy + (random.randint(-8, 8))),
                       mouse.duration(), mouse.path())
            time.sleep(float(random.randint(0, 1000)) / 1000)
            pag.mouseUp()
            return


def drag_to_ship_spec_inv(type):
    """Drag item stack to ship's special inventory."""
    logging.debug('moving item stack to special inventory')

    station_inv = lo.locate('./img/indicators/station_inv_name.bmp')
    if station_inv is not None:
        tries = 0
        spec_inv = lo.clocate('./img/buttons/spec_inv_' + type + '.bmp')
        while spec_inv is None and tries <= 25:
            tries += 1
            logging.critical("can't find ship inventory")
            time.sleep(float(random.randint(1000, 2000)) / 1000)
            spec_inv = lo.clocate('./img/buttons/spec_inv_' + type + '.bmp')

        if spec_inv is not None and tries <= 25:
            (x, y) = station_inv
            (sx, sy) = spec_inv
            pag.moveTo((x + (random.randint(-5, 250))),
                       (y + (random.randint(10, 25))),
                       mouse.duration(), mouse.path())
            time.sleep(float(random.randint(0, 1000)) / 1000)
            pag.mouseDown()
            time.sleep(float(random.randint(0, 1000)) / 1000)
            pag.moveTo((sx + (random.randint(-15, 40))),
                       (sy + (random.randint(-3, 3))),
                       mouse.duration(), mouse.path())
            time.sleep(float(random.randint(0, 1000)) / 1000)
            pag.mouseUp()
            return     
    else:
        logging.critical("can't find name column")
        traceback.print_exc()
        traceback.print_stack()
        sys.exit()


def load_ship_bulk():
    """Load ship by selecting all item stacks and moving all stacks at once."""
    logging.debug('beginning bulk loading procedure') 

    if docked.detect_items() == 0:
        return 0

    else:
        docked.focus_inv_window()
        key.hotkey('ctrl', 'a')
        drag_to_ship_inv()

        time.sleep(float(random.randint(1500, 3000)) / 1000)
        nospace = docked.not_enough_space_warning()
        setquant = docked.set_quant_warning()

        if nospace == 0 and setquant == 0:
            logging.debug('no warnings')
            return 2
  
        # If there isn't enough space in the main ship inventory,
        # check if it has a special inventory. Iterate through a
        # list of possible special inventory types.
        specinv_list = ['ore','fleet']
        if nospace == 1:
            for invtype in specinv_list:
                if docked.detect_spec_inv(invtype) == 1:
                    docked.focus_inv_window()
                    key.hotkey('ctrl','a')
                    drag_to_ship_spec_inv(invtype)

                    time.sleep(float(random.randint(1500, 3000)) / 1000)
                    specinvwarning = docked.spec_inv_warning()
                    nospace = docked.not_enough_space_warning()
                    setquant = docked.set_quant_warning()

                    # If no warnings appear, look for more item stacks,
                    # just to be sure the station is empty.
                    if specinvwarning == 0 and setquant == 0 and nospace == 0:
                        if docked.detect_items() == 1: 
                            logging.debug('more items remaining')
                            return 0
                        else:
                            logging.debug('station empty')
                            return 2

                    elif specinvwarning == 0 and setquant == 1 and nospace \
                            == 0:
                        logging.debug('cannot load in bulk')
                        return 1

                    else:
                        return 0
                else:
                    return 0
        else:
            return 0
            

def load_ship_individually():
    """Load ship one item stack at a time."""
    logging.debug('beginning individual loading procedure')
    docked.open_station_inv()
    items = docked.detect_items()

    while items == 1:
        docked.focus_inv_window()
        drag_to_ship_inv()

        time.sleep(float(random.randint(1000, 3000)) / 1000)
        nospace = docked.not_enough_space_warning()
        setquant = docked.set_quant_warning()
        print(nospace, setquant)

        if nospace == 0 and setquant == 0:
            drag_to_ship_inv()

            time.sleep(float(random.randint(1500, 3000)) / 1000)
            nospace = docked.not_enough_space_warning()
            setquant = docked.set_quant_warning()
            items = docked.detect_items()

        elif nospace == 0 and setquant == 1:
            return 1

        # If a warning appears but item stacks are still present, check if ship
        # has a special inventory.
        specinv_list = ['ore','fleet']
        if nospace == 1:
            for invtype in specinv_list:
                items = docked.detect_items()
                if docked.detect_spec_inv(invtype) == 1:
                    drag_to_ship_spec_inv(invtype)

                    time.sleep(float(random.randint(1500, 3000)) / 1000)
                    specinvwarning = docked.spec_inv_warning()
                    nospace = docked.not_enough_space_warning()
                    setquant = docked.set_quant_warning()
                    items = docked.detect_items()

                    while specinvwarning == 0 and setquant == 0 and nospace == 0 and \
                        items == 1:
                        drag_to_ship_spec_inv(invtype)

                        time.sleep(float(random.randint(1500, 3000)) / 1000)
                        specinvwarning = docked.spec_inv_warning()
                        nospace = docked.not_enough_space_warning()
                        setquant = docked.set_quant_warning()
                        items = docked.detect_items()

                    if items == 0:
                        logging.debug('done loading' + (str(invtype)) + 'inventory')
                        return 2

                    elif specinvwarning == 1 or setquant == 1 or nospace == 1:
                        logging.debug('items remain')
                        return 1
                    else:
                        logging.debug('station empty')
                        return 2
                else:
                    logging.debug('items remain')
                    return 1             
        else:
            logging.debug('station empty')
            return 2
    if items == 0:
        logging.debug('station empty')
        return 2


def load_ship_full():
    """Utilize both individual and bulk loading functions to load ship."""
    docked.open_station_inv()
    items = docked.detect_items()

    if items == 1:
        lsb = load_ship_bulk()
        if lsb == 2:
            logging.debug('ship loaded entire station inventory')
            return 2

        elif lsb == 1:
            logging.debug('ship is full and station inventory has more items')
            return 1

        elif lsb == 0:
            lsi = load_ship_individually()
            if lsi == 2:
                logging.debug('ship loaded entire station inventory')
                return 2

            elif lsi == 1:
                logging.debug('ship is full and station inventory has more  '
                              'items')
                return 1

    elif items == 0:
        return 0
