import sys, pyautogui, os, time, random, ctypes
from lib import mouse, keyboard, while_docked, load_ship

pyautogui.FAILSAFE = True

sys.setrecursionlimit(100000)
conf = 0.95


def drag_items_from_cargo_hold():
    # dragitems to station item hangar
    # look for 'name' column header at top of inventory window and offset mouse
    namefield_station_hangar_icon = pyautogui.locateCenterOnScreen('namefield_station_hangar.bmp',
                                                                   confidence=conf)
    (namefield_station_hangar_iconx, namefield_station_hangar_icony) = namefield_station_hangar_icon
    pyautogui.moveTo((namefield_station_hangar_iconx + (random.randint(-5, 250))),
                     (namefield_station_hangar_icony + (random.randint(10, 25))),
                     mouse.move_time(), mouse.mouse_path())
    # wait up to 1 second before clicking, divide by 1000 to convert from miliseconds to seconds
    pyautogui.mouseDown()
    station_hangar = pyautogui.locateCenterOnScreen('station_hangar.bmp',
                                                                   confidence=conf)
    (station_hangarx, station_hangary) = station_hangar
    pyautogui.moveTo((station_hangarx + (random.randint(-15, 60))),
                     (station_hangary + (random.randint(-10, 10))),
                     mouse.move_time(), mouse.mouse_path())
    pyautogui.mouseUp()
    # after unloading main cargo hold, look for special cargo hold
    print('moved all item stacks from cargo hold')
    return


# drag items from inventory into ship special hold hold
def drag_items_from_special_hold():
    # check if ship has specialized hold that needs to be unloaded
    print('moving all item stacks from special hold')
   # select all items in special hold

    namefield_station_hangar = pyautogui.locateCenterOnScreen('namefield_station_hangar.bmp',
                                                                   confidence=conf)
    (namefield_station_hangarx, namefield_station_hangary) = namefield_station_hangar
    pyautogui.moveTo((namefield_station_hangarx + (random.randint(-5, 200))),
                     (namefield_station_hangary + (random.randint(10, 20))),
                     mouse.move_time(), mouse.mouse_path())
    # wait up to 1 second before clicking, divide by 1000 to convert from miliseconds to seconds
    pyautogui.mouseDown()
    station_hangar = pyautogui.locateCenterOnScreen('station_hangar.bmp',
                                                                   confidence=conf)
    (station_hangarx, station_hangary) = station_hangar
    pyautogui.moveTo((station_hangarx + (random.randint(-15, 40))),
                     (station_hangary + (random.randint(-10, 10))),
                     mouse.move_time(), mouse.mouse_path())
    pyautogui.mouseUp()
    print('moved all item stacks from special hold')
    return


def unload_ship():
    print('began unloading procedure')
    global unload_ship_var
    while_docked.open_cargo_hold()
    while_docked.look_for_items()
    if while_docked.look_for_items_var == 0:  # if no items, return function
        while_docked.look_for_special_hold()
        if while_docked.look_for_special_hold_var == 1:
            while_docked.open_special_hold()
            while_docked.look_for_items()
            while while_docked.look_for_items_var == 1:
                while_docked.focus_inventory_window()
                keyboard.select_all()
                drag_items_from_special_hold()
                time.sleep(2)
                while_docked.look_for_items()
                print('finished unloading procedure')
                return
            if while_docked.look_for_items_var == 0:
                print('finished unloading procedure')
                return
        elif while_docked.look_for_special_hold_var == 0:
            print('error, nothing to unload')
            sys.exit()
            return
    while while_docked.look_for_items_var == 1:
        print('unloading items from cargo hold')
        while_docked.focus_inventory_window()
        keyboard.select_all()
        drag_items_from_cargo_hold()
        time.sleep(2)
        while_docked.look_for_special_hold()
        while_docked.look_for_items()
    if while_docked.look_for_special_hold_var == 1:
        while_docked.open_special_hold()
        while_docked.look_for_items()
        while while_docked.look_for_items_var == 1:
            while_docked.focus_inventory_window()
            keyboard.select_all()
            drag_items_from_special_hold()
            time.sleep(2)
            while_docked.look_for_items()
            print('finished unloading procedure')
            return
    elif while_docked.look_for_special_hold_var == 0:
        print('finished unloading procedure')
        return
