import sys
import time
import ctypes
import random

import pyautogui as pag

from lib import mouse
from lib import keyboard

pag.FAILSAFE = True  # force script to stop if move mouse into top left
# corner of screen
sys.setrecursionlimit(
    100000)  # set high recursion limit for repeating functions
conf = 0.95  # set default confidence value for imagesearch  

# obtain screen dimensions
user32 = ctypes.windll.user32
screenx = user32.GetSystemMetrics(0)
screeny = user32.GetSystemMetrics(1)
halfscreenx = (int(screenx / 2))
halfscreeny = (int(screeny / 2))


def docked_check():
    # Check if the ship is currently docked by looking for the undock icon.
    undock_icon = pag.locateCenterOnScreen('./img/undock.bmp',
                                           confidence = conf)
    if undock_icon is None:
        print('docked_check -- not docked')
        return 0
    elif undock_icon is not None:
        print('docked_check -- docked')
        return 1


def open_cargo_hold():
    # Click on the ship's cargo hold button in inventory window while docked.
    print('open_cargo_hold -- opening cargo hold')
    cargo_hold = pag.locateCenterOnScreen('./img/cargo_hold.bmp',
                                          confidence = conf)
    while cargo_hold is None:
        print("open_cargo_hold -- can't find cargo hold")
        cargo_hold = pag.locateCenterOnScreen('./img/cargo_hold.bmp',
                                              confidence = conf)
        time.sleep(1)
    else:
        (cargo_holdx, cargo_holdy) = cargo_hold
        pag.moveTo((cargo_holdx + (random.randint(-4, 50))),
                   (cargo_holdy + (random.randint(-6, 6))),
                   mouse.move_time(), mouse.mouse_path())
        mouse.click()
        return


def open_special_hold():
    # If a special hold was found (ore hold, mineral hold, etc.) click on it in
    # inventory window while docked.
    print('open_special_hold -- opening special hold')
    special_hold = pag.locateCenterOnScreen('./img/special_hold.bmp',
                                            confidence = conf)
    while special_hold is None:
        print("open_special_hold -- can't find special hold")
        special_hold = pag.locateCenterOnScreen('./img/special_hold.bmp',
                                                confidence = conf)
        time.sleep(1)
    else:
        (special_holdx, special_holdy) = special_hold
        pag.moveTo((special_holdx + (random.randint(-4, 50))),
                   (special_holdy + (random.randint(15, 30))),
                   mouse.move_time(), mouse.mouse_path())
        mouse.click()
        return


def open_station_hangar():
    # Click on the station hangar button within inventory window while docked.
    print('open_station_hangar -- opening station hangar')
    station_hangar = pag.locateCenterOnScreen('./img/station_hangar.bmp',
                                              confidence = conf)
    while station_hangar is None:
        print(
            "open_station_hangar -- can't find inventory station hangar icon")
        station_hangar = pag.locateCenterOnScreen('./img/station_hangar.bmp',
                                                  confidence = conf)
        time.sleep(1)
    else:
        (station_hangarx, station_hangary) = station_hangar
        pag.moveTo((station_hangarx + (random.randint(-6, 50))),
                   (station_hangary + (random.randint(-6, 6))),
                   mouse.move_time(), mouse.mouse_path())
        mouse.click()
        return


def focus_inventory_window():
    # Click somewhere inside the station inventory window to focus it before
    # any items are selected. Look for the sorting buttons in top right corner
    # of the inventory window and position the mouse cursor relative to those
    # buttons to click a non-interactive area within the inventory window.
    sorting_station_hangar = pag.locateCenterOnScreen(
        './img/sorting_station_hangar.bmp', confidence = conf)
    while sorting_station_hangar is None:
        print("focus_inventory_window -- can't find sorting icon")
        sorting_station_hangar = pag.locateCenterOnScreen(
            './img/sorting_station_hangar.bmp', confidence = conf)
        time.sleep(1)
    else:
        (sorting_station_hangarx,
         sorting_station_hangary) = sorting_station_hangar
        pag.moveTo((sorting_station_hangarx - (random.randint(0, 250))),
                   (sorting_station_hangary + (random.randint(50, 300))),
                   mouse.move_time(), mouse.mouse_path())
        mouse.click()
        return


def look_for_items():
    # Look at the bottom-right corner of the station inventory window for the
    # '0 items found' text. If it isn't present, there must be items in the
    # station's inventory.
    global no_items_station_hangar
    global namefield_station_hangar
    no_items_station_hangar = pag.locateCenterOnScreen(
        './img/no_items_station_hangar.bmp',
        confidence = .99)
    if no_items_station_hangar is None:
        namefield_station_hangar = pag.locateCenterOnScreen(
            './img/namefield_station_hangar.bmp',
            confidence = conf)
        return 1
    elif no_items_station_hangar is not None:
        print('look_for_items -- no more items')
        return 0


def look_for_special_hold():
    # Look for a drop-down arrow next to your ship icon in the station
    # inventory window, indicating the ship has a special cargo hold.
    special_hold = pag.locateCenterOnScreen('./img/special_hold.bmp',
                                            confidence = conf)
    no_additional_bays = pag.locateCenterOnScreen(
        './img/no_additional_bays.bmp', confidence = conf)
    if special_hold is not None and no_additional_bays is None:
        print('look_for_special_hold -- found special hold')
        return 1
    else:
        return 0


def special_hold_warning():
    # Look for a popup indicating the selected inventory items aren't
    # compatible with the ship's special hold. This warning is partially
    # transparent so confidence rating must be slightly lower than normal.
    special_hold_warning_popup = pag.locateCenterOnScreen(
        './img/special_hold_warning.bmp', confidence = 0.8)
    if special_hold_warning_popup is None:
        return 0
    else:
        print('special_hold_warning -- detected special hold warning')
        return 1


def set_quantity_popup():
    # Check if a 'set quantity' window appears, indicating there isn't enough
    # space in the ship's hold for a full item stack.
    set_quantity = pag.locateCenterOnScreen('./img/set_quantity.bmp',
                                            confidence = conf)
    if set_quantity is None:
        return 0
    else:
        print('set_quantity_popup -- found set quantity popup')
        keyboard.enter()
        return 1


def not_enough_space_popup():
    # Check if a 'not enough space' popup appears, indicating the item stacks
    # selected will not fit into the ship's hold, or hold is already full.
    not_enough_space = pag.locateCenterOnScreen('./img/not_enough_space.bmp',
                                                confidence = conf)
    if not_enough_space is None:
        return 0
    else:
        print('not_enough_space_popup -- found not enough space popup')
        keyboard.enter()
        return 1


def undock():
    # Undock from the station with the default hotkey. The undock has been
    # completed once the script sees the cyan ship icon in the top left corner
    # of the client window, indicating a session change has just ocurred.
    print('undock -- undocking')
    pag.keyDown('alt')  # alt+u
    time.sleep(float(random.randint(200, 1200)) / 1000)
    pag.keyDown('u')
    time.sleep(float(random.randint(200, 1200)) / 1000)
    pag.keyUp('u')
    time.sleep(float(random.randint(200, 1200)) / 1000)
    pag.keyUp('alt')
    time.sleep(int((random.randint(5000, 10000) / 1000)))
    undocked = pag.locateCenterOnScreen('./img/session_change_undocked.bmp',
                                        confidence = 0.55,
                                        region = (
                                            0, 0, (int(screenx / 5)), screeny))
    while undocked is None:
        time.sleep(int((random.randint(3000, 10000) / 1000)))
        print('undock -- trying undocking second time')
        pag.keyDown('alt')
        time.sleep(float(random.randint(200, 1200)) / 1000)
        pag.keyDown('u')
        time.sleep(float(random.randint(200, 1200)) / 1000)
        pag.keyUp('u')
        time.sleep(float(random.randint(200, 1200)) / 1000)
        pag.keyUp('alt')
        time.sleep(int((random.randint(5000, 10000) / 1000)))
        undocked = pag.locateCenterOnScreen(
            './img/session_change_undocked.bmp', confidence = 0.55,
            region = (0, 0, (int(screenx / 5)), screeny))
    if undocked is not None:
        time.sleep(int((random.randint(2000, 3000) / 1000)))
        return