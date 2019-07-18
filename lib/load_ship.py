import sys
import time
import random
import logging
import traceback
import pyautogui as pag
from lib import mouse, keyboard, docked
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
    if clocate('./img/indicators/station_inv_name.bmp') is None:
        logging.critical("can't find name column")
        traceback.print_exc()
        traceback.print_stack()
        sys.exit()

    else:
        tries = 0
        while clocate('./img/buttons/ship_inv.bmp') is None and tries <= 25:
            tries += 1
            logging.critical("can't find ship inventory")
            time.sleep(float(random.randint(1000, 2000)) / 1000)
            namefield_station_in = clocate_var
            
        if clocate('./img/buttons/ship_inv.bmp') is not None and tries <= 25:
            (x, y) = namefield_station_inv
            (ship_invx, ship_invy) = clocate_var
            pag.moveTo((x + (random.randint(-5, 250))),
                       (y + (random.randint(10, 25))),
                       mouse.duration(), mouse.path())
            pag.mouseDown()
            pag.moveTo((ship_invx + (random.randint(-5, 60))),
                       (ship_invy + (random.randint(-8, 8))),
                       mouse.duration(), mouse.path())
            pag.mouseUp()
            return


def drag_to_ship_spec_inv(type):
    """Drag item stack to ship's special inventory."""
    logging.debug('moving item stack to special inventory')

    if lo.locate('./img/indicators/station_inv_name.bmp') is not None:
        tries = 0
        namefield_station_inv = locate_var
        
        while lo.clocate('./img/buttons/spec_inv_' + type + '.bmp') is None and tries <= 25:
            tries += 1
            logging.critical("can't find ship inventory")
            time.sleep(float(random.randint(1000, 2000)) / 1000)
            
        if lo.locate('./img/buttons/spec_inv_' + type + '.bmp') is not None and tries <= 25:
            (x, y) = namefield_station_inv
            spec_inv = locate_var
            (sx, sy) = spec_inv
            pag.moveTo((x + (random.randint(-5, 250))),
                       (y + (random.randint(10, 25))),
                       mouse.duration(), mouse.path())
            pag.mouseDown()
            pag.moveTo((sx + (random.randint(-15, 40))),
                       (sy + (random.randint(-3, 3))),
                       mouse.duration(), mouse.path())
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
    items = docked.detect_items()

    if items is None:
        return 0

    elif items == 1:
        docked.focus_inv_window()
        keyboard.select_all()
        drag_to_ship_inv()

        time.sleep(float(random.randint(1000, 3000)) / 1000)
        nospace = docked.not_enough_space_warning()
        setquant = docked.set_quant_warning()

        if nospace == 0 and setquant == 0:
            logging.debug('no warnings')
            return 2

        elif nospace == 1:  # If a warning appears, check if the ship has a
            # special inventory
            if docked.detect_spec_inv('ore') == 1:
                docked.focus_inv_window()
                keyboard.select_all()
                drag_to_ship_spec_inv('ore')

                time.sleep(float(random.randint(1000, 3000)) / 1000)
                specinvwarning = docked.spec_inv_warning()
                nospace = docked.not_enough_space_warning()
                setquant = docked.set_quant_warning()

                if specinvwarning == 0 and setquant == 0 and nospace == 0:
                    docked.detect_items()  # If no warnings appear, look for
                    # more item stacks.
                    if items == 0:
                        return 2
                    else:
                        logging.debug('more items remaining')
                        return 0

                elif specinvwarning == 0 and setquant == 1 and nospace \
                        == 0:
                    return 1

                else:  # If a warning appears, try loading item stacks
                    # individually.
                    return 0
                
            if docked.detect_spec_inv('fleet') == 1:
                docked.focus_inv_window()
                keyboard.select_all()
                drag_to_ship_spec_inv('fleet')

                time.sleep(float(random.randint(1000, 3000)) / 1000)
                specinvwarning = docked.spec_inv_warning()
                nospace = docked.not_enough_space_warning()
                setquant = docked.set_quant_warning()

                if specinvwarning == 0 and setquant == 0 and nospace == 0:
                    docked.detect_items()  # If no warnings appear, look for
                    # more item stacks.
                    if items == 0:
                        return 2
                    else:
                        logging.debug('more items remaining')
                        return 0

                elif specinvwarning == 0 and setquant == 1 and nospace \
                        == 0:
                    return 1

                else:  # If a warning appears, try loading item stacks
                    # individually.
                    return 0

            else:
                return 0

        elif setquant == 1:
            return 1


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

            time.sleep(float(random.randint(1000, 3000)) / 1000)
            nospace = docked.not_enough_space_warning()
            setquant = docked.set_quant_warning()

            docked.detect_items()

        elif nospace == 0 and setquant == 1:
            return 1

        # If a warning appears but item stacks are still present, check if ship
        # has a special inventory.
        elif nospace == 1 and setquant == 0:
            traceback.print_stack()
            
            if docked.detect_spec_inv('ore') == 1:
                drag_to_ship_spec_inv('ore')

                time.sleep(float(random.randint(1000, 3000)) / 1000)
                specinvwarning = docked.spec_inv_warning()
                nospace = docked.not_enough_space_warning()
                setquant = docked.set_quant_warning()

                docked.detect_items()

                while specinvwarning == 0 and nospace == 0:
                    drag_to_ship_spec_inv('ore')

                    time.sleep(float(random.randint(1000, 3000)) / 1000)
                    specinvwarning = docked.spec_inv_warning()
                    nospace = docked.not_enough_space_warning()
                    setquant = docked.set_quant_warning()

                    docked.detect_items()

                if items is None:
                    logging.debug('done loading ore inventory')
                    return 2

                elif specinvwarning == 1 or nospace == 1:
                    return 1
            
            if docked.detect_spec_inv('fleet') == 1:
                drag_to_ship_spec_inv('fleet')

                time.sleep(float(random.randint(1000, 3000)) / 1000)
                specinvwarning = docked.spec_inv_warning()
                nospace = docked.not_enough_space_warning()
                setquant = docked.set_quant_warning()

                docked.detect_items()

                while specinvwarning == 0 and setquant == 0 and nospace == 0:
                    drag_to_ship_spec_inv('fleet')

                    time.sleep(float(random.randint(1000, 3000)) / 1000)
                    specinvwarning = docked.spec_inv_warning()
                    nospace = docked.not_enough_space_warning()
                    setquant = docked.set_quant_warning()

                    docked.detect_items()

                if items is None:
                    logging.debug('done loading fleet inventory')
                    return 2

                elif specinvwarning == 1 or setquant == 1 or nospace == 1:
                    return 1
            else:
                return 1             
    if items is None:
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
