import sys
import time
import random

import pyautogui as pag

from lib import mouse
from lib import keyboard
from lib import docked

global screenx
global screeny
global halfscreenx
global halfscreeny
global windowx
global windowy
global originx
global originy
global conf

sys.setrecursionlimit(9999999)


def drag_items_from_ship_inv():
    # Click and drag all items from ship inventory to station inventory.
    namefield_station_inv_icon = pag.locateCenterOnScreen(
        './img/namefield_station_hangar.bmp',
        confidence=conf)
    (namefield_station_inv_iconx,
     namefield_station_inv_icony) = namefield_station_inv_icon
    pag.moveTo((namefield_station_inv_iconx + (random.randint(-5, 250))),
               (namefield_station_inv_icony + (random.randint(10, 25))),
               mouse.move_time(), mouse.mouse_path())

    pag.mouseDown()
    station_inv = pag.locateCenterOnScreen('./img/station_hangar.bmp',
                                           confidence=conf)
    (station_invx, station_invy) = station_inv
    pag.moveTo((station_invx + (random.randint(-15, 60))),
               (station_invy + (random.randint(-10, 10))),
               mouse.move_time(), mouse.mouse_path())
    pag.mouseUp()
    print(
        'drag_items_from_ship_inv -- moved all item stacks from ship '
        'inventory')
    return


def unload_ship():
    print('unload_ship -- began unloading procedure')
    docked.open_ship_inv()
    specinv = docked.look_for_spec_inv()
    items = docked.look_for_items()

    if docked.look_for_items() == 0:
        docked.look_for_spec_inv()
        if specinv == 1:
            # Wait between 0 and 2s before actions for increased randomness.
            time.sleep(float(random.randint(0, 2000)) / 1000)
            docked.open_spec_inv()
            items = docked.look_for_items()

            while items == 1:
                time.sleep(float(random.randint(0, 2000)) / 1000)
                docked.focus_inv_window()
                time.sleep(float(random.randint(0, 2000)) / 1000)
                keyboard.select_all()
                time.sleep(float(random.randint(0, 2000)) / 1000)
                drag_items_from_ship_inv()
                time.sleep(2)
                docked.look_for_items()
                print('unload_ship -- finished unloading procedure')
                return 1

            if items == 0:
                print('unload_ship -- finished unloading procedure')
                return 1

        elif specinv == 0:
            print('unload_ship -- nothing to unload')
            return 1

    while items == 1:
        docked.focus_inv_window()
        time.sleep(float(random.randint(0, 2000)) / 1000)
        keyboard.select_all()
        time.sleep(float(random.randint(0, 2000)) / 1000)
        drag_items_from_ship_inv()
        time.sleep(2)
        docked.look_for_spec_inv()
        items = docked.look_for_items()

    if specinv == 1:
        docked.open_spec_inv()
        items = docked.look_for_items()

        while items == 1:
            docked.focus_inv_window()
            time.sleep(float(random.randint(0, 2000)) / 1000)
            keyboard.select_all()
            time.sleep(float(random.randint(0, 2000)) / 1000)
            drag_items_from_ship_inv()
            time.sleep(2)
            docked.look_for_items()
            print('unload_ship -- finished unloading procedure')
            return 1
    elif specinv == 0:
        print('unload_ship -- finished unloading procedure')
        return 1
