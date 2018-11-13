import sys, pyautogui, os, time, random, ctypes
from lib import mouse, keyboard, while_docked

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 2.5
#os.chdir('D:\OneDrive\Documents\Scripts\Python\PY-NEOBOT-GitHub\lib')


sys.setrecursionlimit(100000)
conf = 0.95


def drag_items_to_cargo_bay():
    print('loading cargo bay')
    # look for 'name' column header at top of inventory window and offset mouse
    os.chdir('c:/users/austin/desktop/icons')
    namefield_station_hangar_icon = pyautogui.locateCenterOnScreen('namefield_station_hangar_icon.png',
                                                                   confidence=conf)
    while namefield_station_hangar_icon is None:
        print('cant find namefield_station_hangar_icon')
        namefield_station_hangar_icon = pyautogui.locateCenterOnScreen('namefield_station_hangar_icon.png',
                                                                       confidence=conf)
    else:
        print('found namefield_station_hangar_icon')
        # if icon found, look for ship cargo bay icon in inventory sidebar
        inventory_current_ship_icon = pyautogui.locateCenterOnScreen('inventory_current_ship_icon.png',
                                                                     confidence=conf)
        while inventory_current_ship_icon is None:
            print('cant find inventory_current_ship_icon')
            inventory_current_ship_icon = pyautogui.locateCenterOnScreen('inventory_current_ship_icon.png',
                                                                         confidence=conf)
        else:  # if found icons, click on first item in station hangar and drag mouse to ship cargo bay
            print('found inventory_current_ship_icon')
            (namefield_station_hangar_iconx, namefield_station_hangar_icony) = namefield_station_hangar_icon
            (inventory_current_ship_iconx, inventory_current_ship_icony) = inventory_current_ship_icon
            pyautogui.moveTo((namefield_station_hangar_iconx + (random.randint(-5, 200))),
                             (namefield_station_hangar_icony + (random.randint(10, 20))),
                             mouse.move_time(), mouse.mouse_path())
            pyautogui.mouseDown()
            pyautogui.moveTo((inventory_current_ship_iconx + (random.randint(-5, 20))),
                             (inventory_current_ship_icony + (random.randint(-5, 5))),
                             mouse.move_time(), mouse.mouse_path())
            pyautogui.mouseUp()
            # check if 'set quantity' popup appears indicating not enough room in cargo bay
            set_quantity()
            if set_quantity() == 0:
                drag_items_to_cargo_bay()
            else:
                look_for_special_hold()
                if look_for_special_hold() == 1:
                    drag_items_to_special_hold()
                    return


def set_quantity():
    os.chdir('c:/users/austin/desktop/icons')
    # check if 'set quantity' popup appears indicating not enough room in cargo bay
    set_quantity_to_deposit_in_cargo_bay_popup = \
        pyautogui.locateCenterOnScreen('set_quantity_to_deposit_in_cargo_bay_popup.png', confidence=conf)
    if set_quantity_to_deposit_in_cargo_bay_popup is None:
        print('no set quantity popup')
        return 0  # if popup doesn't appear, continue moving items to cargo bay
    else:
        print('found set quantity popup')
        keyboard.enter()  # confirm dialog box and undock
        return 1


# if ship has a specialized hold for specific items, try dragging station hangar inventory into it first
def look_for_special_hold():
    os.chdir('c:/users/austin/desktop/icons')
    # look for drop down arrow next to ship indicating it has a special hold
    special_hold_dropown_arrow = pyautogui.locateCenterOnScreen('hold.png', confidence=conf)
    if special_hold_dropown_arrow is None:
        print('no special hold')
        return 0
    else:
        print('found special hold')
        return 1


# look for the warning indicating selected items aren't compatible with ship's special hold parameters
def look_for_special_hold_warning():
    os.chdir('c:/users/austin/desktop/icons')
    # special hold warning is partially transparent so confidence rating must be slightly lower than normal
    special_hold_warning = pyautogui.locateCenterOnScreen('special_hold_warning.png', confidence=0.8)
    if special_hold_warning is None:
        print('no special hold warning')
        return 0
    else:
        # if special hold warning appears, try dragging item to cargo bay instead
        print('detected special hold warning')
        return 1


# drag items from inventory into ship special hold bay
def drag_items_to_special_hold():
    os.chdir('c:/users/austin/desktop/icons')
    # look for 'name' column header at top of inventory window and offset mouse
    namefield_station_hangar_icon = pyautogui.locateCenterOnScreen('namefield_station_hangar_icon.png',
                                                                   confidence=conf)
    while namefield_station_hangar_icon is None:
        print('cant find namefield_station_hangar_icon, moving items to special hold')
        namefield_station_hangar_icon = pyautogui.locateCenterOnScreen('namefield_station_hangar_icon.png',
                                                                       confidence=conf)
    else:
        print('found namefield_station_hangar_icon, moving items to special hold')
        # if icon found, look for ship cargo bay icon in inventory sidebar
        inventory_current_ship_icon = pyautogui.locateCenterOnScreen('inventory_current_ship_icon.png',
                                                                     confidence=conf)
        while inventory_current_ship_icon is None:
            print('cant find inventory_current_ship_icon, moving items to special hold')
            inventory_current_ship_icon = pyautogui.locateCenterOnScreen('inventory_current_ship_icon.png',
                                                                         confidence=conf)
        else:  # if found icons, click on first item in station hangar and drag mouse to ship cargo bay
            print('found inventory_current_ship_icon, moving items to special hold')
            (namefield_station_hangar_iconx, namefield_station_hangar_icony) = namefield_station_hangar_icon
            (inventory_current_ship_iconx, inventory_current_ship_icony) = inventory_current_ship_icon
            pyautogui.moveTo((namefield_station_hangar_iconx + (random.randint(-5, 200))),
                             (namefield_station_hangar_icony + (random.randint(10, 20))),
                             mouse.move_time(), mouse.mouse_path())
            # wait up to 1 second before clicking, divide by 1000 to convert from miliseconds to seconds
            time.sleep((random.randint(0, 10) / 10))
            pyautogui.mouseDown()
            time.sleep((random.randint(0, 10) / 10))
            pyautogui.moveTo((inventory_current_ship_iconx + (random.randint(-15, 40))),
                             (inventory_current_ship_icony + (random.randint(14, 24))),
                             mouse.move_time(), mouse.mouse_path())
            time.sleep((random.randint(0, 10) / 10))
            pyautogui.mouseUp()
            time.sleep((random.randint(0, 10) / 10))
            # check if 'set quantity' popup appears indicating not enough room in cargo bay
            set_quantity()
            if set_quantity() == 0:
                look_for_special_hold_warning()
                if look_for_special_hold_warning() == 0:
                    drag_items_to_special_hold()
                else:
                    return
            else:
                return


def load_ship():
    print('loading ship')
    while_docked.open_station_hangar()
    while_docked.focus_inventory_window()
    drag_items_to_cargo_bay()
    print('ship loaded')
    while_docked.undock()
    return



