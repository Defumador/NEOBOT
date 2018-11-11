import sys, time, pyautogui, os, random
from lib import mouse, keyboard, in_space
import numpy
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 2.5
os.chdir('D:\OneDrive\Documents\Scripts\Python\PY-NEOBOT-GitHub\lib')
defaultsleep = .5
sys.setrecursionlimit(100000)


# check if ship is docked
def docked_check():
    undock_icon = pyautogui.locateCenterOnScreen('undock_icon.png', confidence=0.9)
    if undock_icon is None:
        in_space.select_waypoint()
    else:
        at_home_check()

# check if ship has arrived back at its home station by looking for an entry in 'people and places' starting with 3 0's
def at_home_check():
    os.chdir('c:/users/austin/desktop/icons')
    at_home = pyautogui.locateCenterOnScreen('at_home.png', confidence = 0.95)
    if at_home is None:
        print('not at_home')
        at_dest_check()
    else:
        print('at home')
        return_to_dest()


# if at home station, unload ship cargo bay(s)
def unload_ship():
    # first select ship inventory
    print('unloading ship')
    os.chdir('c:/users/austin/desktop/icons')
    inventory_current_ship_icon = pyautogui.locateCenterOnScreen('inventory_current_ship_icon.png', confidence = 0.9)
    while inventory_current_ship_icon is None:
        print('cant find inventory_current_ship_icon')
        time.sleep(defaultsleep)
        inventory_current_ship_icon = pyautogui.locateCenterOnScreen('inventory_current_ship_icon.png', confidence=0.9)
    else:
        print('found inventory_current_ship_icon, unloading ship')
        (inventory_current_ship_iconx, inventory_current_ship_icony) = inventory_current_ship_icon
        # clicks the center of where the button was found
        pyautogui.moveTo((inventory_current_ship_iconx + (random.randint(-6, 6))), (inventory_current_ship_icony +
                        (random.randint(-6, 6))), mouse.move_time(),mouse. mouse_path())
        mouse.click()
        # then drag ship inventory to station
        focus_inventory_window()
        keyboard.select_all() # select all items in ship cargo bay

        # now drag items to station item hangar
        # look for 'name' column header at top of inventory window and offset mouse
        namefield_station_hangar_icon = pyautogui.locateCenterOnScreen('namefield_station_hangar_icon.png',
                                                                           confidence=0.9)
        inventory_station_hangar_icon = pyautogui.locateCenterOnScreen('inventory_station_hangar_icon.png',
                                                                       confidence=0.95)
        (namefield_station_hangar_iconx, namefield_station_hangar_icony) = namefield_station_hangar_icon
        (inventory_station_hangar_iconx, inventory_station_hangar_icony) = inventory_station_hangar_icon
        pyautogui.moveTo((namefield_station_hangar_iconx + (random.randint(-5, 200))),
                         (namefield_station_hangar_icony + (random.randint(10, 20))), mouse.move_time(),
                         mouse.mouse_path())
        # wait up to 1 second before clicking, divide by 1000 to convert from miliseconds to seconds
        time.sleep((random.randint(0, 1000) / 1000))
        pyautogui.mouseDown()
        time.sleep((random.randint(0, 1000) / 1000))
        pyautogui.moveTo((inventory_station_hangar_iconx + (random.randint(-15, 40))),
                         (inventory_station_hangar_icony + (random.randint(-10, 10))), mouse.move_time(),
                         mouse.mouse_path())
        time.sleep((random.randint(0, 1000) / 1000))
        pyautogui.mouseUp()
        time.sleep((random.randint(0, 1000) / 1000))
        # check if ship has specialized bay that needs to be unloaded
        look_for_special_hold()
        if look_for_special_hold() == 1:
            pyautogui.moveTo((inventory_current_ship_iconx + (random.randint(-10, 40))),
                             (inventory_current_ship_icony + (random.randint(14, 24))),
                             mouse.move_time(), mouse.mouse_path())
            mouse.click()
            focus_inventory_window()
            keyboard.select_all()  # select all items in ship cargo bay
            pyautogui.moveTo((namefield_station_hangar_iconx + (random.randint(-5, 200))),
                             (namefield_station_hangar_icony + (random.randint(10, 20))), mouse.move_time(),
                             mouse.mouse_path())
            # wait up to 1 second before clicking, divide by 1000 to convert from miliseconds to seconds
            time.sleep((random.randint(0, 1000) / 1000))
            pyautogui.mouseDown()
            time.sleep((random.randint(0, 1000) / 1000))
            pyautogui.moveTo((inventory_station_hangar_iconx + (random.randint(-15, 40))),
                             (inventory_station_hangar_icony + (random.randint(-10, 10))), mouse.move_time(),
                             mouse.mouse_path())
            time.sleep((random.randint(0, 1000) / 1000))
            pyautogui.mouseUp()
            time.sleep((random.randint(0, 1000) / 1000))
            undock()


# check if ship has arrived back at its destination by looking for an entry in 'people and places' starting with 3 1's
def at_dest_check():
    os.chdir('c:/users/austin/desktop/icons')
    at_dest = pyautogui.locateCenterOnScreen('at_dest.png', confidence = 0.95)
    if at_dest is None:
        print('not at_dest')
        open_station_hangar()
    else:
        print('at dest')
        return_home()


# set waypoint back to home station before undocking from destination station
def return_home():
    os.chdir('c:/users/austin/desktop/icons')
    at_home = pyautogui.locateCenterOnScreen('at_home.png', confidence = 0.9)
    (at_homex, at_homey) = at_home
    pyautogui.moveTo((at_homex + (random.randint(-1, 20))), (at_homey + (random.randint(-3, 3))),
                     mouse.move_time(), mouse.mouse_path())
    mouse.click_right()  # right click to open dropdown menu
    pyautogui.moveRel((0 + (random.randint(10, 50))), (0 + (random.randint(20, 25))),
                     mouse.move_time(), mouse.mouse_path())
    mouse.click()  # click set destination in drop down
    open_station_hangar()


def return_to_dest():
    os.chdir('c:/users/austin/desktop/icons')
    at_dest = pyautogui.locateCenterOnScreen('at_dest.png', confidence = 0.9)
    (at_destx, at_desty) = at_dest
    pyautogui.moveTo((at_destx + (random.randint(-1, 20))), (at_desty + (random.randint(-3, 3))),
                     mouse.move_time(), mouse.mouse_path())
    mouse.click_right()  # right click to open dropdown menu
    pyautogui.moveRel((0 + (random.randint(10, 50))), (0 + (random.randint(20, 25))),
                     mouse.move_time(), mouse.mouse_path())
    mouse.click()  # click set destination in drop down
    unload_ship()


def open_station_hangar():  # click on station hangar button in inventory window while docked
    os.chdir('c:/users/austin/desktop/icons')
    station_hangar_icon = pyautogui.locateCenterOnScreen('inventory_station_hangar_icon.png', confidence = 0.9)
    while station_hangar_icon is None:
        print('cant find inventory_station_hangar_icon')
        time.sleep(defaultsleep)
        station_hangar_icon = pyautogui.locateCenterOnScreen('inventory_station_hangar_icon.png', confidence=0.9)
    else:
        print('found inventory_station_hangar_icon')
        (station_hangar_iconx, station_hangar_icony) = station_hangar_icon
        # clicks the center of where the button was found
        pyautogui.moveTo((station_hangar_iconx + (random.randint(-6, 6))),
                         (station_hangar_icony + (random.randint(-6, 6))),
                         mouse.move_time(),mouse. mouse_path())
        mouse.click()
        focus_inventory_window()
        look_for_special_hold()
        if look_for_special_hold() == 1:
            drag_items_to_special_hold()


def focus_inventory_window():  # click inside the station inventory window to focus it before items are selected
    # look for sorting buttons in top right corner of inventory window and offset mouse
    os.chdir('c:/users/austin/desktop/icons')
    sorting_station_hangar_icon = pyautogui.locateCenterOnScreen('sorting_station_hangar_icon.png',
                                                                 confidence = 0.9)
    while sorting_station_hangar_icon is None:
        print('cant find sorting_station_hangar_icon')
        time.sleep(defaultsleep)
        sorting_station_hangar_icon = pyautogui.locateCenterOnScreen('sorting_station_hangar_icon.png',
                                                                     confidence=0.9)
    else:
        print('found sorting_station_hangar_icon')
        (sorting_station_hangar_iconx, sorting_station_hangar_icony) = sorting_station_hangar_icon
        # offset mouse from sorting button to click within inventory window to focus it
        pyautogui.moveTo((sorting_station_hangar_iconx - (random.randint(40, 300))),
                         (sorting_station_hangar_icony + (random.randint(40, 300))),
                         mouse.move_time(), mouse.mouse_path())
        mouse.click()
        return


# if ship has a specialized hold for specific items, try dragging station hangar inventory into it first
def look_for_special_hold():
    os.chdir('c:/users/austin/desktop/icons')
    # look for drop down arrow next to ship indicating it has a special hold
    special_hold_dropown_arrow = pyautogui.locateCenterOnScreen('hold.png', confidence = 0.94)
    if special_hold_dropown_arrow is None:
        print('no special hold')
        return 0
    else:
        print('found special hold')
        return 1

# drag items from inventory into ship special hold bay
def drag_items_to_special_hold():
    os.chdir('c:/users/austin/desktop/icons')
    # look for 'name' column header at top of inventory window and offset mouse
    namefield_station_hangar_icon = pyautogui.locateCenterOnScreen('namefield_station_hangar_icon.png',
                                                                   confidence=0.9)
    while namefield_station_hangar_icon is None:
        print('cant find namefield_station_hangar_icon, moving items to special hold')
        time.sleep(defaultsleep)
        namefield_station_hangar_icon = pyautogui.locateCenterOnScreen('namefield_station_hangar_icon.png',
                                                                       confidence=0.9)
    else:
        print('found namefield_station_hangar_icon, moving items to special hold')
        # if icon found, look for ship cargo bay icon in inventory sidebar
        inventory_current_ship_icon = pyautogui.locateCenterOnScreen('inventory_current_ship_icon.png',
                                                                     confidence=0.9)
        while inventory_current_ship_icon is None:
            print('cant find inventory_current_ship_icon, moving items to special hold')
            time.sleep(defaultsleep)
            inventory_current_ship_icon = pyautogui.locateCenterOnScreen('inventory_current_ship_icon.png',
                                                                         confidence=0.9)
        else:  # if found icons, click on first item in station hangar and drag mouse to ship cargo bay
            print('found inventory_current_ship_icon, moving items to special hold')
            (namefield_station_hangar_iconx, namefield_station_hangar_icony) = namefield_station_hangar_icon
            (inventory_current_ship_iconx, inventory_current_ship_icony) = inventory_current_ship_icon
            pyautogui.moveTo((namefield_station_hangar_iconx + (random.randint(-5, 200))),
                             (namefield_station_hangar_icony + (random.randint(10, 20))),
                             mouse.move_time(), mouse.mouse_path())
            # wait up to 1 second before clicking, divide by 1000 to convert from miliseconds to seconds
            time.sleep((random.randint(0, 100) / 1000))
            pyautogui.mouseDown()
            time.sleep((random.randint(0, 100) / 1000))
            pyautogui.moveTo((inventory_current_ship_iconx + (random.randint(-15, 40))),
                             (inventory_current_ship_icony + (random.randint(14, 24))),
                             mouse.move_time(), mouse.mouse_path())
            time.sleep((random.randint(0, 100) / 1000))
            pyautogui.mouseUp()
            time.sleep((random.randint(0, 100) / 1000))
            # check if 'set quantity' popup appears indicating not enough room in cargo bay
            set_quantity_to_deposit_in_cargo_bay_popup = \
                pyautogui.locateCenterOnScreen('set_quantity_to_deposit_in_cargo_bay_popup.png', confidence=0.9)
            if set_quantity_to_deposit_in_cargo_bay_popup is None:
                print('cant find set_quantity_to_deposit_in_cargo_bay_popup')
                time.sleep(defaultsleep)
                look_for_special_hold_warning()
                drag_items_to_special_hold()
            else:
                print('found set_quantity_to_deposit_in_cargo_bay_popup')
                time.sleep(defaultsleep)
                keyboard.enter()  # confirm dialog box and undock
                drag_items_to_cargo_bay()


# look for the warning indicating selected items aren't compatible with ship's special hold parameters
def look_for_special_hold_warning():
    os.chdir('c:/users/austin/desktop/icons')
    special_hold_warning = pyautogui.locateCenterOnScreen('special_hold_warning.png', confidence = 0.8)
    if special_hold_warning is None:
        print('no special hold warning')
        drag_items_to_cargo_bay()
    else:
        # if special hold warning appears, try dragging item to cargo bay instead
        print('found special hold warning')
        drag_items_to_special_hold()

# drag items from inventory into ship cargo bay
def drag_items_to_cargo_bay():
    # look for 'name' column header at top of inventory window and offset mouse
    os.chdir('c:/users/austin/desktop/icons')
    namefield_station_hangar_icon = pyautogui.locateCenterOnScreen('namefield_station_hangar_icon.png',
                                                                   confidence = 0.9)
    while namefield_station_hangar_icon is None:
        print('cant find namefield_station_hangar_icon')
        time.sleep(defaultsleep)
        namefield_station_hangar_icon = pyautogui.locateCenterOnScreen('namefield_station_hangar_icon.png',
                                                                       confidence=0.9)
    else:
        print('found namefield_station_hangar_icon')
        # if icon found, look for ship cargo bay icon in inventory sidebar
        inventory_current_ship_icon = pyautogui.locateCenterOnScreen('inventory_current_ship_icon.png',
                                                                     confidence = 0.9)
        while inventory_current_ship_icon is None:
            print('cant find inventory_current_ship_icon')
            time.sleep(defaultsleep)
            inventory_current_ship_icon = pyautogui.locateCenterOnScreen('inventory_current_ship_icon.png',
                                                                         confidence=0.9)
        else:  # if found icons, click on first item in station hangar and drag mouse to ship cargo bay
            print('found inventory_current_ship_icon')
            (namefield_station_hangar_iconx, namefield_station_hangar_icony) = namefield_station_hangar_icon
            (inventory_current_ship_iconx, inventory_current_ship_icony) = inventory_current_ship_icon
            pyautogui.moveTo((namefield_station_hangar_iconx + (random.randint(-5, 200))),
                             (namefield_station_hangar_icony + (random.randint(10, 20))),
                             mouse.move_time(), mouse.mouse_path())
            # wait before clicking, divide by 1000 to convert from miliseconds to seconds
            time.sleep((random.randint(0, 100) / 1000))
            pyautogui.mouseDown()
            time.sleep((random.randint(0, 100) / 1000))
            pyautogui.moveTo((inventory_current_ship_iconx + (random.randint(-5, 20))),
                             (inventory_current_ship_icony + (random.randint(-5, 5))),
                             mouse.move_time(), mouse.mouse_path())
            time.sleep((random.randint(0, 100) / 1000))
            pyautogui.mouseUp()
            time.sleep((random.randint(0, 100) / 1000))
            # check if 'set quantity' popup appears indicating not enough room in cargo bay
            set_quantity_to_deposit_in_cargo_bay_popup = \
                pyautogui.locateCenterOnScreen('set_quantity_to_deposit_in_cargo_bay_popup.png', confidence=0.9)
            if set_quantity_to_deposit_in_cargo_bay_popup is None:
                print('cant find set_quantity_to_deposit_in_cargo_bay_popup')
                time.sleep(defaultsleep)
                drag_items_to_cargo_bay()  # if popup doesn't appear, continue moving items to cargo bay
            else:
                print('found set_quantity_to_deposit_in_cargo_bay_popup')
                time.sleep(defaultsleep)
                keyboard.enter()  # confirm dialog box and undock
                undock()

def set_quantity():
    os.chdir('c:/users/austin/desktop/icons')
    # check if 'set quantity' popup appears indicating not enough room in cargo bay
    set_quantity_to_deposit_in_cargo_bay_popup =\
        pyautogui.locateCenterOnScreen('set_quantity_to_deposit_in_cargo_bay_popup.png', confidence = 0.9)
    if set_quantity_to_deposit_in_cargo_bay_popup is None:
        print('cant find set_quantity_to_deposit_in_cargo_bay_popup')
        time.sleep(defaultsleep)
        return 0  # if popup doesn't appear, continue moving items to cargo bay
    else:
        print('found set_quantity_to_deposit_in_cargo_bay_popup')
        time.sleep(defaultsleep)
        keyboard.enter()  # confirm dialog box and undock
        return 1

def undock():
    os.chdir('c:/users/austin/desktop/icons')
    undock_icon = pyautogui.locateCenterOnScreen('undock_icon.png', confidence = 0.9)
    while undock_icon is None:
        print('cant find undock button')
        time.sleep(defaultsleep)
        undock_icon = pyautogui.locateCenterOnScreen('undock_icon.png', confidence=0.9)
    else:
        print('undocking')
        (undock_iconx, undock_icony) = undock_icon
        # clicks the center of where the button was found
        pyautogui.moveTo((undock_iconx + (random.randint(-25,25))),
                         (undock_icony + (random.randint(-15,15))),
                         mouse.move_time(), mouse.mouse_path())
        mouse.click()
        time.sleep(12)  # wait for undock to complete
        in_space.select_waypoint()
