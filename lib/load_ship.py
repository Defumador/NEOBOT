import sys, time, random, traceback
import pyautogui as pag
from lib import mouse, keyboard, docked
from lib.vars import originx, originy, windowx, windowy, conf

sys.setrecursionlimit(9999999)

# A return value of 2 indicates the ship has been loaded and the station's
# inventory is empty.

# A return value of 1 indicates the ship has been fully loaded but more items
# remain in the station.

# A return value of 0 indicates the ship cannot be loaded in the manner chosen.


def drag_to_ship_inv():
    # Click and drag the first item stack from station's inventory to ship's
    # inventory. This function assumed the relevant window is already open.
    print('drag_to_ship_inv -- moving item stack to ship inventory')
    namefield_station_inv = pag.locateCenterOnScreen(
        './img/namefield_station_station inventory.bmp',
        confidence=conf, region=(originx, originy, windowx, windowy))

    if namefield_station_inv is None:
        print("drag_to_ship_inv -- can't find name column")
        traceback.print_exc()
        traceback.print_stack()
        sys.exit()

    elif namefield_station_inv is not None:
        ship_inv = pag.locateCenterOnScreen('./img/cargo_hold.bmp',
                                            confidence=conf,
                                            region=(originx, originy,
                                                    windowx, windowy))
        while ship_inv is None:
            print("drag_to_ship_inv -- can't find ship inventory")
            ship_inv = pag.locateCenterOnScreen('./img/cargo_hold.bmp',
                                                confidence=conf,
                                                region=(originx, originy,
                                                        windowx, windowy))
            time.sleep(1)
        if ship_inv is not None:
            (namefield_station_invx,
             namefield_station_invy) = namefield_station_inv
            (ship_invx, ship_invy) = ship_inv
            pag.moveTo((namefield_station_invx + (random.randint(-5, 250))),
                       (namefield_station_invy + (random.randint(10, 25))),
                       mouse.duration(), mouse.path())
            pag.mouseDown()
            pag.moveTo((ship_invx + (random.randint(-5, 60))),
                       (ship_invy + (random.randint(-8, 8))),
                       mouse.duration(), mouse.path())
            pag.mouseUp()
            return


def drag_to_ship_spec_inv():
    # Same as previous function, except drag item stack to ship's special
    # inventory.
    print('drag_to_ship_spec_inv -- moving item stack to special inventory')
    namefield_station_inv = pag.locateCenterOnScreen(
        './img/namefield_station_station inventory.bmp',
        confidence=conf, region=(originx, originy, windowx, windowy))

    if namefield_station_inv is None:
        print("drag_to_ship_spec_inv -- can't find name column")
        traceback.print_exc()
        traceback.print_stack()
        sys.exit()
    elif namefield_station_inv is not None:
        ship_inv = pag.locateCenterOnScreen('./img/cargo_hold.bmp',
                                            confidence=conf,
                                            region=(originx, originy,
                                                    windowx, windowy))
        while ship_inv is None:
            print("drag_to_ship_spec_inv -- can't find ship inventory")
            ship_inv = pag.locateCenterOnScreen('./img/cargo_hold.bmp',
                                                confidence=conf,
                                                region=(originx, originy,
                                                        windowx, windowy))
            time.sleep(1)
        if ship_inv is not None:
            (namefield_station_invx,
             namefield_station_invy) = namefield_station_inv
            (ship_invx, ship_invy) = ship_inv
            pag.moveTo((namefield_station_invx + (random.randint(-5, 250))),
                       (namefield_station_invy + (random.randint(10, 25))),
                       mouse.duration(), mouse.path())
            pag.mouseDown()
            pag.moveTo((ship_invx + (random.randint(-15, 40))),
                       (ship_invy + (random.randint(14, 24))),
                       mouse.duration(), mouse.path())
            pag.mouseUp()
            return


def load_ship_bulk():
    # Load ship by selecting all item stacks and moving all stacks at once.
    print('load_ship_bulk -- beginning bulk loading procedure')
    items = docked.detect_items()

    if items is None:
        return 0

    elif items == 1:
        docked.focus_inv_window()
        keyboard.select_all()
        drag_to_ship_inv()
        time.sleep(
            2)  # After moving stack, wait and look for warnings.
        nospace = docked.not_enough_space_warning()
        setquant = docked.set_quant_warning()

        if nospace == 0 and setquant == 0:
            print('load_ship_bulk -- no warnings')
            return 2

        elif nospace == 1:  # If a warning appears, check if the ship has a
            # special inventory
            specinv = docked.detect_spec_inv()
            if specinv == 1:
                docked.focus_inv_window()
                keyboard.select_all()
                drag_to_ship_spec_inv()
                time.sleep(2)
                specinvwarning = docked.spec_inv_warning()
                nospace = docked.not_enough_space_warning()
                setquant = docked.set_quant_warning()

                if specinvwarning == 0 and setquant == 0 and nospace == 0:
                    docked.detect_items()  # If no warnings appear, look for
                    # more item stacks.
                    if items == 0:
                        return 2
                    else:
                        print('load_ship_bulk -- more items remaining')
                        return 0

                elif specinvwarning == 0 and setquant == 1 and nospace \
                        == 0:
                    return 1

                else:  # If a warning appears, try loading item stacks
                    # individually.
                    return 0

            elif specinv == 0:
                return 0

        elif setquant == 1:
            return 1


def load_ship_individually():
    # Load ship one item stack at a time.
    print('load_ship_individually -- beginning individual loading procedure')
    docked.open_station_inv()
    items = docked.detect_items()

    while items == 1:
        docked.focus_inv_window()
        drag_to_ship_inv()
        time.sleep(2)
        nospace = docked.not_enough_space_warning()
        setquant = docked.set_quant_warning()
        print(nospace, setquant)

        if nospace == 0 and setquant == 0:
            drag_to_ship_inv()
            time.sleep(2)
            nospace = docked.not_enough_space_warning()
            setquant = docked.set_quant_warning()
            docked.detect_items()

        elif nospace == 0 and setquant == 1:
            return 1

        # If a warning appears but item stacks are still present, check if ship
        # has a special inventory.
        elif nospace == 1 and setquant == 0:
            traceback.print_stack()
            specinv = docked.detect_spec_inv()
            if specinv == 1:
                drag_to_ship_spec_inv()
                time.sleep(2)
                specinvwarning = docked.spec_inv_warning()
                nospace = docked.not_enough_space_warning()
                setquant = docked.set_quant_warning()
                docked.detect_items()

                while specinvwarning == 0 and setquant == 0 and nospace == 0:
                    drag_to_ship_spec_inv()
                    time.sleep(2)
                    specinvwarning = docked.spec_inv_warning()
                    nospace = docked.not_enough_space_warning()
                    setquant = docked.set_quant_warning()
                    docked.detect_items()

                if items is None:
                    print(
                        'load_ship_individually -- done loading special '
                        'inventory')
                    return 2

                elif specinvwarning == 1 or setquant == 1 or nospace == 1:
                    return 1
            else:
                return 1

    if items is None:
        return 2


def load_ship_full():
    # Utilize both individual and bulk loading functions to load ship.
    docked.open_station_inv()
    items = docked.detect_items()

    if items == 1:
        lsb = load_ship_bulk()
        if lsb == 2:
            print('load_ship -- ship loaded entire station inventory')
            return 2

        elif lsb == 1:
            print(
                'load_ship -- ship is full and station inventory has more '
                'items')
            return 1

        elif lsb == 0:
            lsi = load_ship_individually()
            if lsi == 2:
                print('load_ship -- ship loaded entire station inventory')
                return 2

            elif lsi == 1:
                print(
                    'load_ship -- ship is full and station inventory has '
                    'more items')
                return 1

    elif items == 0:
        return 0
