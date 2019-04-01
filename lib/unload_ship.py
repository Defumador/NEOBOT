import sys
import time
import random
import ctypes


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




atsite = 0
gotosite = 0
sys.setrecursionlimit(9999999)  # set high recursion limit for functions that
# call themselves.

conf = 0.95
alignment_time = 6  # Seconds (rounded up) current ship takes to begin a warp.

user32 = ctypes.windll.user32
screenx = user32.GetSystemMetrics(0)
screeny = user32.GetSystemMetrics(1)
halfscreenx = (int(screenx / 2))
halfscreeny = (int(screeny / 2))

window_resolutionx = 1024
window_resolutiony = 768

# get the coordinates of the eve client window and restrict image searching to
# within these boundaries.
# search for the eve neocom logo in top left corner of the eve client window.
# This will become the origin of the coordinate system.
origin = pag.locateCenterOnScreen('./img/buttons/neocom.bmp', confidence=0.90)
(originx, originy) = origin

# move the origin up and to the left slightly to get it to the exact top
# left corner of the eve client window. This is necessary  because the image
# searching algorithm returns coordinates to the center of the image rather
# than its top right corner.

windowx = originx + window_resolutionx
windowy = originy + window_resolutiony








sys.setrecursionlimit(9999999)


def drag_items_from_ship_inv():
    # Click and drag all items from ship inventory to station inventory.
    namefield_station_inv_icon = pag.locateCenterOnScreen(
        './img/indicators/station_inv_name.bmp',
        confidence=conf,
        region=(originx, originy, windowx, windowy))

    (namefield_station_inv_iconx,
     namefield_station_inv_icony) = namefield_station_inv_icon
    pag.moveTo((namefield_station_inv_iconx + (random.randint(-5, 250))),
               (namefield_station_inv_icony + (random.randint(10, 25))),
               mouse.duration(), mouse.path())

    pag.mouseDown()
    station_inv = pag.locateCenterOnScreen('./img/buttons/station_inv.bmp',
                                           confidence=conf,
                                           region=(originx, originy,
                                                   windowx, windowy))
    (station_invx, station_invy) = station_inv
    pag.moveTo((station_invx + (random.randint(-15, 60))),
               (station_invy + (random.randint(-10, 10))),
               mouse.duration(), mouse.path())
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
