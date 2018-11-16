import sys, pyautogui, os, time, random, ctypes
from lib import mouse, keyboard, while_docked, load_ship

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 2.5

sys.setrecursionlimit(100000)
conf = 0.95


def drag_items_from_cargo_hold():
    # first select ship inventory
    print('moving all item stacks from cargo hold')
    os.chdir('c:/users/austin/desktop/icons')
    ship_cargo_hold_icon = pyautogui.locateCenterOnScreen('ship_cargo_hold.bmp',
                                                                 confidence=conf)
    while ship_cargo_hold_icon is None:
        print('cant find ship_cargo_hold_icon')
        ship_cargo_hold_icon = pyautogui.locateCenterOnScreen('ship_cargo_hold.bmp',
                                                                     confidence=conf)
    else:
        print('unloading cargo hold')
        (ship_cargo_hold_iconx, ship_cargo_hold_icony) = ship_cargo_hold_icon
        # clicks the center of where the button was found
        pyautogui.moveTo((ship_cargo_hold_iconx + (random.randint(-6, 6))),
                         (ship_cargo_hold_icony + (random.randint(-6, 6))),
                         mouse.move_time(), mouse.mouse_path())

        mouse.click()
        while_docked.focus_inventory_window()
        keyboard.select_all()  # select all items in ship cargo hold

        # dragitems to station item hangar
        # look for 'name' column header at top of inventory window and offset mouse
        namefield_station_hangar_icon = pyautogui.locateCenterOnScreen('namefield_station_hangar.bmp',
                                                                       confidence=conf)
        (namefield_station_hangar_iconx, namefield_station_hangar_icony) = namefield_station_hangar_icon
        pyautogui.moveTo((namefield_station_hangar_iconx + (random.randint(-5, 250))),
                         (namefield_station_hangar_icony + (random.randint(10, 25))),
                         mouse.move_time(), mouse.mouse_path())
        # wait up to 1 second before clicking, divide by 1000 to convert from miliseconds to seconds
        time.sleep((random.randint(0, 10) / 10))
        pyautogui.mouseDown()
        time.sleep((random.randint(0, 10) / 10))
        inventory_station_hangar_icon = pyautogui.locateCenterOnScreen('inventory_station_hangar.bmp',
                                                                       confidence=conf)
        (inventory_station_hangar_iconx, inventory_station_hangar_icony) = inventory_station_hangar_icon
        pyautogui.moveTo((inventory_station_hangar_iconx + (random.randint(-15, 60))),
                         (inventory_station_hangar_icony + (random.randint(-10, 10))),
                         mouse.move_time(), mouse.mouse_path())
        time.sleep((random.randint(0, 10) / 10))
        pyautogui.mouseUp()
        time.sleep((random.randint(0, 10) / 10))
        # after unloading main cargo hold, look for special cargo hold
        print('moved all item stacks from cargo hold')
        return


# drag items from inventory into ship special hold hold
def drag_items_from_special_hold():
    # check if ship has specialized hold that needs to be unloaded
    print('moving all item stacks from special hold')
    ship_cargo_hold_icon = pyautogui.locateCenterOnScreen('ship_cargo_hold.bmp',
                                                                 confidence=conf)
    (ship_cargo_hold_iconx, ship_cargo_hold_icony) = ship_cargo_hold_icon
    pyautogui.moveTo((ship_cargo_hold_iconx + (random.randint(-10, 60))),
                     (ship_cargo_hold_icony + (random.randint(14, 24))),
                     mouse.move_time(), mouse.mouse_path())

    mouse.click()
    while_docked.focus_inventory_window()
    keyboard.select_all()  # select all items in special hold

    namefield_station_hangar_icon = pyautogui.locateCenterOnScreen('namefield_station_hangar.bmp',
                                                                   confidence=conf)
    (namefield_station_hangar_iconx, namefield_station_hangar_icony) = namefield_station_hangar_icon
    pyautogui.moveTo((namefield_station_hangar_iconx + (random.randint(-5, 200))),
                     (namefield_station_hangar_icony + (random.randint(10, 20))),
                     mouse.move_time(), mouse.mouse_path())
    # wait up to 1 second before clicking, divide by 1000 to convert from miliseconds to seconds
    pyautogui.mouseDown()
    inventory_station_hangar_icon = pyautogui.locateCenterOnScreen('inventory_station_hangar.bmp',
                                                                   confidence=conf)
    (inventory_station_hangar_iconx, inventory_station_hangar_icony) = inventory_station_hangar_icon
    pyautogui.moveTo((inventory_station_hangar_iconx + (random.randint(-15, 40))),
                     (inventory_station_hangar_icony + (random.randint(-10, 10))),
                     mouse.move_time(), mouse.mouse_path())
    pyautogui.mouseUp()
    print('moved all item stacks from special hold')
    return


def unload_ship():
    print('began unloading procedure')
    while_docked.open_station_hangar()
    while_docked.focus_inventory_window()
    load_ship.check_for_items()
    while load_ship.check_for_items == 1:
        drag_items_from_cargo_hold()
        load_ship.check_for_items()
    else:
        load_ship.look_for_special_hold()
        if load_ship.look_for_special_hold == 1:
            load_ship.check_for_items()
            while load_ship.check_for_items == 1:
                drag_items_from_special_hold()
                load_ship.look_for_special_hold()
        elif load_ship.look_for_special_hold == 0:
            print('finished unloading procedure')
            return
