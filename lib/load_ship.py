import sys
import time
import random
import traceback

import pyautogui as pag

from lib import mouse
from lib import keyboard
from lib import docked

pag.FAILSAFE = True
sys.setrecursionlimit(100000)
conf = 0.95


# click and drag first item stack in inventory to ship cargo hold, function assumes cargo hold is already open
def drag_items_to_cargo_hold():
    print('moving item stack to cargo hold')
    namefield_station_hangar = pag.locateCenterOnScreen('./img/namefield_station_hangar.bmp',
                                                        confidence=conf)
    if namefield_station_hangar is None:
        print('cant find name column')
        traceback.print_exc()
        traceback.print_stack()
        sys.exit()
    elif namefield_station_hangar is not None:
        # if icon found, look for ship cargo hold icon in inventory sidebar
        cargo_hold = pag.locateCenterOnScreen('./img/cargo_hold.bmp',
                                              confidence=conf)
        while cargo_hold is None:
            print('cant find ship cargo hold')
            cargo_hold = pag.locateCenterOnScreen('./img/cargo_hold.bmp',
                                                  confidence=conf)
        # if found icons, click on first item in station hangar and drag mouse to ship cargo hold
        if cargo_hold is not None:
            (namefield_station_hangarx, namefield_station_hangary) = namefield_station_hangar
            (ship_cargo_holdx, ship_cargo_holdy) = cargo_hold
            pag.moveTo((namefield_station_hangarx + (random.randint(-5, 250))),
                       (namefield_station_hangary + (random.randint(10, 25))),
                       mouse.move_time(), mouse.mouse_path())
            pag.mouseDown()
            pag.moveTo((ship_cargo_holdx + (random.randint(-5, 60))),
                       (ship_cargo_holdy + (random.randint(-8, 8))),
                       mouse.move_time(), mouse.mouse_path())
            pag.mouseUp()
            return


# click and drag first item stack in inventory to ship special hold, function assumes special hold is already open
def drag_items_to_special_hold():
    print('moving item stack to special hold')
    namefield_station_hangar = pag.locateCenterOnScreen('./img/namefield_station_hangar.bmp',
                                                        confidence=conf)
    if namefield_station_hangar is None:
        print('cant find name column')
        traceback.print_exc()
        traceback.print_stack()
        sys.exit()
    elif namefield_station_hangar is not None:
        # if icon found, look for ship cargo hold icon in inventory sidebar
        cargo_hold = pag.locateCenterOnScreen('./img/cargo_hold.bmp',
                                              confidence=conf)
        while cargo_hold is None:
            print('cant find ship cargo hold')
            cargo_hold = pag.locateCenterOnScreen('./img/cargo_hold.bmp',
                                                  confidence=conf)
        if cargo_hold is not None:
            (namefield_station_hangarx, namefield_station_hangary) = namefield_station_hangar
            (cargo_holdx, cargo_holdy) = cargo_hold
            pag.moveTo((namefield_station_hangarx + (random.randint(-5, 250))),
                       (namefield_station_hangary + (random.randint(10, 25))),
                       mouse.move_time(), mouse.mouse_path())
            pag.mouseDown()
            pag.moveTo((cargo_holdx + (random.randint(-15, 40))),
                       (cargo_holdy + (random.randint(14, 24))),
                       mouse.move_time(), mouse.mouse_path())
            pag.mouseUp()
            return


def load_ship_bulk():  # load ship by selecting all item stacks and moving them all at once
    print('beginning bulk loading procedure')
    items = docked.look_for_items()

    if items is None:
        return 0

    elif items == 1:
        docked.focus_inventory_window()
        keyboard.select_all()
        drag_items_to_cargo_hold()
        time.sleep(2)  # after moving stack to cargo hold, wait and look for warnings
        nospace = docked.not_enough_space_popup()
        setquant = docked.set_quantity_popup()

        if nospace == 0 and setquant == 0:
            print('no warnings')
            return 2  # 2 indicating ship is loaded and hangar is completley empty

        else:  # if warning appears, look for additional cargo hold
            specialhold = docked.look_for_special_hold()
            if specialhold == 1:
                docked.focus_inventory_window()
                keyboard.select_all()
                drag_items_to_special_hold()
                time.sleep(2)
                specialholdwarning = docked.special_hold_warning()
                docked.set_quantity_popup()
                docked.not_enough_space_popup()

                if specialholdwarning == 0 and setquant == 0 and nospace == 0:
                    docked.look_for_items()  # if no warnings, look for more items
                    if items == 0:
                        return 2
                    else:
                        print('more items remaining')
                        return 0

                elif specialholdwarning == 0 and setquant == 1 and nospace == 0:
                    return 1

                else:  # if warning appears, try loading items individually
                    return 0  # 0 indicating ship cannot be fully loaded in bulk
            else:
                return 1
    return


# load ship one item stack at a time
def load_ship_individually():
    print('beginning individual loading procedure')
    docked.open_station_hangar()
    items = docked.look_for_items()

    if items is None:
        return 2  # 2 indicating ship is loaded and hangar is completley empty

    elif items == 1:
        docked.focus_inventory_window()
        drag_items_to_cargo_hold()
        time.sleep(2)
        nospace = docked.not_enough_space_popup()
        setquant = docked.set_quantity_popup()
        docked.look_for_items()

        while nospace == 0 and setquant == 0 and items == 1:
            drag_items_to_cargo_hold()  # if no warnings, keep moving items
            time.sleep(2)
            docked.not_enough_space_popup()
            docked.set_quantity_popup()
            docked.look_for_items()

        if nospace == 0 and setquant == 0 and items == 0:
            print('done loading main hold')
            return 2  # 2 indicating ship is loaded and hangar is completley empty

        # if warning appears but items are still present, look for additional cargo hold
        elif (nospace == 1 or setquant == 1) and items == 1:
            specialhold = docked.look_for_special_hold()

            if specialhold == 1:
                drag_items_to_special_hold()
                time.sleep(2)
                specialholdwarning = docked.special_hold_warning()
                docked.set_quantity_popup()
                docked.not_enough_space_popup()
                docked.look_for_items()

                # if no warnings, keep moving items to special hold
                while specialholdwarning == 0 and setquant == 0 and nospace == 0 and items == 1:
                    drag_items_to_special_hold()
                    time.sleep(2)
                    docked.special_hold_warning()
                    docked.set_quantity_popup()
                    docked.not_enough_space_popup()
                    docked.look_for_items()

                if items is None:
                    print('done loading special hold')
                    return 2

                elif specialholdwarning == 1 or setquant == 1 or nospace == 1:
                    return 1  # 1 indicating ship is full but more items remain in hangar
        else:
            return 1  # 1 indicating ship is full but more items remain in hangar
    return


# use both individual and bulk functions to load ship
def load_ship():
    docked.open_station_hangar()
    items = docked.look_for_items()
    if items == 1:
        lsb = load_ship_bulk()
        if lsb == 2:
            print('ship loaded entire hangar')
            return 2
        elif lsb == 1:
            print('ship is full and hangar has more items')
            return 1

        elif lsb == 0:  # 0 indicating ship cannot be fully loaded in bulk
            lsi = load_ship_individually()
            if lsi == 2:
                print('ship loaded entire hangar')
                return 2
            elif lsi == 1:
                print('ship is full and hangar has more items')
                return 1
    elif items == 0:
        return 0
