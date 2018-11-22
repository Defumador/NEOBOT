import sys
import time
import ctypes
import random
import traceback

import pyautogui

from lib import mouse
from lib import keyboard

pyautogui.FAILSAFE = True  # force script to stop if move mouse into top left corner of screen
sys.setrecursionlimit(100000)  # set high recursion limit for repeating functions
conf = 0.95  # set default confidence value for imagesearch  


# check if ship is docked
def docked_check():
    global docked_check_var
    undock_icon = pyautogui.locateCenterOnScreen('./img/undock.bmp', confidence=conf)
    if undock_icon is None:
        print('not docked')
        docked_check_var = 0
        return
    elif undock_icon is not None:
        print('docked')
        docked_check_var = 1
        return


# click on ship cargo hold button in inventory window while docked
def open_cargo_hold():  
    print('opening cargo hold')
    cargo_hold = pyautogui.locateCenterOnScreen('./img/cargo_hold.bmp', confidence=conf)
    while cargo_hold is None:
        print('cant find cargo hold')
        cargo_hold = pyautogui.locateCenterOnScreen('./img/cargo_hold.bmp', confidence=conf)
    else:
        (cargo_holdx, cargo_holdy) = cargo_hold
        pyautogui.moveTo((cargo_holdx + (random.randint(-4, 50))),
                         (cargo_holdy + (random.randint(-6, 6))),
                         mouse.move_time(), mouse.mouse_path())

        mouse.click()
        return


# if a special hold was found, click on it in inventory window while docked
def open_special_hold():
    print('opening special hold')
    special_hold = pyautogui.locateCenterOnScreen('./img/special_hold.bmp', confidence=conf)
    while special_hold is None:
        print('cant find special hold')
        special_hold = pyautogui.locateCenterOnScreen('./img/special_hold.bmp', confidence=conf)
    else:
        (special_holdx, special_holdy) = special_hold
        pyautogui.moveTo((special_holdx + (random.randint(-4, 50))),
                         (special_holdy + (random.randint(15, 30))),
                         mouse.move_time(), mouse.mouse_path())
        mouse.click()
        return


# click on station hangar button in inventory window while docked
def open_station_hangar():  
    print('opening station hangar')
    station_hangar = pyautogui.locateCenterOnScreen('./img/station_hangar.bmp', confidence=conf)
    while station_hangar is None:
        print('cant find inventory station hangar icon')
        station_hangar = pyautogui.locateCenterOnScreen('./img/station_hangar.bmp', confidence=conf)
    else:
        (station_hangarx, station_hangary) = station_hangar
        pyautogui.moveTo((station_hangarx + (random.randint(-6, 50))),
                         (station_hangary + (random.randint(-6, 6))),
                         mouse.move_time(), mouse.mouse_path())
        mouse.click()
        return


# click inside the station inventory window to focus it before any items are selected
def focus_inventory_window():  
    # look for sorting buttons in top right corner of inventory window and offset mouse
    print('focusing inventory window')
    sorting_station_hangar = pyautogui.locateCenterOnScreen('./img/sorting_station_hangar.bmp', confidence=conf)
    while sorting_station_hangar is None:
        print('cant find sorting icon')
        sorting_station_hangar = pyautogui.locateCenterOnScreen('./img/sorting_station_hangar.bmp', confidence=conf)
    else:
        (sorting_station_hangarx, sorting_station_hangary) = sorting_station_hangar
        # offset mouse from sorting button to click within inventory window to focus it
        pyautogui.moveTo((sorting_station_hangarx - (random.randint(0, 250))),
                         (sorting_station_hangary + (random.randint(50, 300))),
                         mouse.move_time(), mouse.mouse_path())
        mouse.click()
        return


# look at the bottom-right corner of station inventory window to determine if '0 items found' appears
def look_for_items():
    global no_items_station_hangar  # var must be global since it's used in other functions
    global look_for_items_var 
    global namefield_station_hangar
    time.sleep(float(random.randint(800, 1000)) / 1000)
    no_items_station_hangar = pyautogui.locateCenterOnScreen('./img/no_items_station_hangar.bmp',
                                                             confidence=.99)
    if no_items_station_hangar is None:
        namefield_station_hangar = pyautogui.locateCenterOnScreen('./img/namefield_station_hangar.bmp',
                                                                  confidence=conf)
        look_for_items_var = 1
        return
    elif no_items_station_hangar is not None:
        print('no more items')
        look_for_items_var = 0
        return


# look for drop-down arrow next to ship icon in station inventory window to determine if ship has special hold
def look_for_special_hold():
    global look_for_special_hold_var
    special_hold = pyautogui.locateCenterOnScreen('./img/special_hold.bmp', confidence=conf)
    if special_hold is None:
        look_for_special_hold_var = 0
        return
    else:
        print('found special hold')
        look_for_special_hold_var = 1
        return


# look for warning indicating selected items aren't compatible with ship's special hold 
def special_hold_warning():
    global special_hold_warning_var
    # special hold warning is partially transparent so confidence rating must be slightly lower than normal
    special_hold_warning_popup = pyautogui.locateCenterOnScreen('./img/special_hold_warning.bmp', confidence=0.8)
    if special_hold_warning_popup is None:
        special_hold_warning_var = 0
        return
    else:
        print('detected special hold warning')
        special_hold_warning_var = 1
        return


# check if 'set quantity' popup appears indicating not enough space in cargo hold for full item stack
def set_quantity_popup():
    global set_quantity_popup_var
    set_quantity = \
        pyautogui.locateCenterOnScreen('./img/set_quantity.bmp', confidence=conf)
    if set_quantity is None:
        set_quantity_popup_var = 0
        return
    else:
        print('found set quantity popup')
        keyboard.enter() 
        set_quantity_popup_var = 1
        return


# check if 'not enough space' popup appears indicating not all item stacks will fit into hold or hold is already full
def not_enough_space_popup():
    global not_enough_space_popup_var
    not_enough_space = pyautogui.locateCenterOnScreen('./img/not_enough_space.bmp', confidence=conf)
    if not_enough_space is None:
        not_enough_space_popup_var = 0
        return
    else:
        print('found not enough space popup')
        keyboard.enter()  
        not_enough_space_popup_var = 1
        return


# obtain screen dimensions
user32 = ctypes.windll.user32
screenwidth = user32.GetSystemMetrics(0)
screenheight = user32.GetSystemMetrics(1)
halfscreenwidth = (int(screenwidth / 2))
halfscreenheight = (int(screenheight / 2))


# undock from station, look for undock button in right half of screen only
def undock():
    print('began undocking procedure')
    undock_button = pyautogui.locateCenterOnScreen('./img/undock.bmp', confidence=conf)
    if undock_button is None:
        print('cant find undock button')
        traceback.print_exc()
        traceback.print_stack()
        sys.exit()
    elif undock_button is not None:
        (undockx, undocky) = undock_button
        pyautogui.moveTo((undockx + (random.randint(-25, 25))),
                         (undocky + (random.randint(-15, 15))),
                         mouse.move_time(), mouse.mouse_path())
        mouse.click()
        # move mouse away from button to prevent tooltips from blocking other buttons
        pyautogui.moveTo((random.randint(0, (screenheight - 100))),
                         (random.randint(0, ((screenwidth - 100) / 2))),
                         mouse.move_time(), mouse.mouse_path())
        # wait a semi-random period of time for undock to complete to mimic human behavior
        time.sleep((random.randint(100, 250) / 10))
        return


'''
#look for 'name' column header in inventory window to indicate presence of items DEPRECATED ///////////////////////////
def look_for_items_oldfunc():
    print('looking for item(s) in hangar')
    look_for_items_loop_num = 0
    global namefield_station_hangar  # var must be global since it's used in other functions
    global look_for_items_var  # return var must be global in order for other files to read it
    namefield_station_hangar = pyautogui.locateCenterOnScreen('namefield_station_hangar.bmp',
                                                                   confidence=conf)
    while namefield_station_hangar is None and look_for_items_loop_num < 10:  # look for items at most 10 times
        print('looking for item(s) in hangar ...x',look_for_items_loop_num)
        look_for_items_loop_num += 1
        namefield_station_hangar = pyautogui.locateCenterOnScreen('namefield_station_hangar.bmp',
                                                                       confidence=conf)
        if look_for_items_loop_num >= 10:  # if loop expires, break out of loop
            break
        elif namefield_station_hangar is not None:  # if found items while looping, return function
            print('found item(s) in hangar')
            look_for_items_var = 1
            return
    else:  # if found items on first loop, return function
        print('found item(s) in hangar')
        look_for_items_var = 1
        return
    print('no items in hangar')  # loop breaks to here
    look_for_items_var = 0
    return
'''