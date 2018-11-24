import sys
import time
import random
import traceback

import pyautogui

from lib import mouse
from lib import keyboard
from lib import docked

pyautogui.FAILSAFE = True
sys.setrecursionlimit(100000)
conf = 0.95


def drag_items_from_hold():
    # dragitems to station item hangar
    namefield_station_hangar_icon = pyautogui.locateCenterOnScreen('./img/namefield_station_hangar.bmp',
                                                                   confidence=conf)
    (namefield_station_hangar_iconx, namefield_station_hangar_icony) = namefield_station_hangar_icon
    pyautogui.moveTo((namefield_station_hangar_iconx + (random.randint(-5, 250))),
                     (namefield_station_hangar_icony + (random.randint(10, 25))),
                     mouse.move_time(), mouse.mouse_path())
    pyautogui.mouseDown()
    station_hangar = pyautogui.locateCenterOnScreen('./img/station_hangar.bmp',
                                                    confidence=conf)
    (station_hangarx, station_hangary) = station_hangar
    pyautogui.moveTo((station_hangarx + (random.randint(-15, 60))),
                     (station_hangary + (random.randint(-10, 10))),
                     mouse.move_time(), mouse.mouse_path())
    pyautogui.mouseUp()
    print('moved all item stacks from hold')
    return


def unload_ship():
    print('began unloading procedure')
    docked.open_cargo_hold()
    specialhold = docked.look_for_special_hold()
    items = docked.look_for_items()
    if docked.look_for_items() == 0:
        # if no items in cargo hold, look for special hold
        docked.look_for_special_hold()
        if specialhold == 1:
            # wait between 0 and 2s before actions for increased randomness
            time.sleep(float(random.randint(0, 2000)) / 1000)
            docked.open_special_hold()
            items = docked.look_for_items()
            while items == 1:
                time.sleep(float(random.randint(0, 2000)) / 1000)
                docked.focus_inventory_window()
                time.sleep(float(random.randint(0, 2000)) / 1000)
                keyboard.select_all()
                time.sleep(float(random.randint(0, 2000)) / 1000)
                drag_items_from_hold()
                time.sleep(2)
                docked.look_for_items()
                print('finished unloading procedure')
                return 1
            if items == 0:
                print('finished unloading procedure')
                return 1
        elif specialhold == 0:
            print('error, nothing to unload')
            traceback.print_exc()
            traceback.print_stack()
            sys.exit()
    while items == 1:
        docked.focus_inventory_window()
        time.sleep(float(random.randint(0, 2000)) / 1000)
        keyboard.select_all()
        time.sleep(float(random.randint(0, 2000)) / 1000)
        drag_items_from_hold()
        time.sleep(2)
        docked.look_for_special_hold()
        items = docked.look_for_items()
    if specialhold == 1:
        docked.open_special_hold()
        items = docked.look_for_items()
        while items == 1:
            docked.focus_inventory_window()
            time.sleep(float(random.randint(0, 2000)) / 1000)
            keyboard.select_all()
            time.sleep(float(random.randint(0, 2000)) / 1000)
            drag_items_from_hold()
            time.sleep(2)
            docked.look_for_items()
            print('finished unloading procedure')
            return 1
    elif specialhold == 0:
        print('finished unloading procedure')
        return 1




