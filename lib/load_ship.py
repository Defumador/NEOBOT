import sys, pyautogui, os, time, random, ctypes
from lib import mouse, keyboard, while_docked

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 2.5
os.chdir('D:\OneDrive\Documents\personal_documents\scripting\PY-NEOBOT-GitHub\lib')


sys.setrecursionlimit(100000)
conf = 0.95
x = 1


def check_for_items():
    global namefield_station_hangar_icon
    namefield_station_hangar_icon = pyautogui.locateCenterOnScreen('namefield_station_hangar_icon.png',
                                                                   confidence=conf)
    if namefield_station_hangar_icon is None:
        print('cant find namefield_station_hangar_icon')
        global x
        while x < 10: #try 10 times to locate icon
            x += 1
            print(x)
            check_for_items()
        else:
            x = 1
            print('all out of items')
            while_docked.undock()
    else:
        drag_items_to_cargo_bay()

def drag_items_to_cargo_bay():
    print('loading cargo bay')
    # look for 'name' column header at top of inventory window and offset mouse
    os.chdir('c:/users/austin/desktop/icons')
    ship_cargo_hold_icon = pyautogui.locateCenterOnScreen('ship_cargo_hold_icon.png',
                                                                 confidence=conf)
    while ship_cargo_hold_icon is None:
        print('cant find ship_cargo_hold_icon')
        ship_cargo_hold_icon = pyautogui.locateCenterOnScreen('ship_cargo_hold_icon.png',
                                                                     confidence=conf)
    else:  # if found icons, click on first item in station hangar and drag mouse to ship cargo bay
        print('found ship_cargo_hold_icon')
        (namefield_station_hangar_iconx, namefield_station_hangar_icony) = namefield_station_hangar_icon
        (ship_cargo_hold_iconx, ship_cargo_hold_icony) = ship_cargo_hold_icon
        pyautogui.moveTo((namefield_station_hangar_iconx + (random.randint(-5, 250))),
                         (namefield_station_hangar_icony + (random.randint(10, 25))),
                         mouse.move_time(), mouse.mouse_path())
        pyautogui.mouseDown()
        pyautogui.moveTo((ship_cargo_hold_iconx + (random.randint(-5, 60))),
                         (ship_cargo_hold_icony + (random.randint(-8, 8))),
                         mouse.move_time(), mouse.mouse_path())
        pyautogui.mouseUp()
        # check if 'set quantity' popup appears indicating not enough room in cargo bay
        #set_quantity_popup()
        if not_enough_room_popup() == 0:
            if set_quantity_popup() == 0:
                check_for_items()
            else:
                print('looking for special holdd')
                if look_for_special_hold() == 1:
                    drag_items_to_special_hold()
                    return
                else:
                    while_docked.undock()
        else:
            print('looking for special holdd')
            if look_for_special_hold() == 1:
                drag_items_to_special_hold()
                return
            else:
                while_docked.undock()


def set_quantity_popup():
    # check if 'set quantity' popup appears indicating not enough room in cargo bay
    set_quantity_to_deposit_in_cargo_bay_popup = \
        pyautogui.locateCenterOnScreen('set_quantity_to_deposit_in_cargo_bay_popup.png', confidence=conf)
    if set_quantity_to_deposit_in_cargo_bay_popup is None:
        print('no set quantity popup')
        return '0'  # if popup doesn't appear, continue moving items to cargo bay
    else:
        print('found set quantity popup')
        keyboard.enter()  # confirm dialog box
        return '1'


def not_enough_room_popup():
    print('not enough room popup running')
    os.chdir('c:/users/austin/desktop/icons')
    not_enough_room_in_hold = pyautogui.locateCenterOnScreen('not_enough_room_in_hold.png', confidence=conf)
    if not_enough_room_in_hold is None:
        print('enough room for more items')
        return 0
    else:
        print('found not enough room popup')
        keyboard.enter()  # confirm dialog box
        return 1


# if ship has a specialized hold for specific items, try dragging station hangar inventory into it first
def look_for_special_hold():
    # look for drop down arrow next to ship indicating it has a special hold
    special_hold_dropown_arrow = pyautogui.locateCenterOnScreen('hold.png', confidence=conf)
    if special_hold_dropown_arrow is None:
        print('no special hold')
        return 0
    else:
        print('found special hold')
        return 1


# look for the warning indicating selected items aren't compatible with ship's special hold parameters
def special_hold_warning():
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
        ship_cargo_hold_icon = pyautogui.locateCenterOnScreen('ship_cargo_hold_icon.png',
                                                                     confidence=conf)
        while ship_cargo_hold_icon is None:
            print('cant find ship_cargo_hold_icon, moving items to special hold')
            ship_cargo_hold_icon = pyautogui.locateCenterOnScreen('ship_cargo_hold_icon.png',
                                                                         confidence=conf)
        else:  # if found icons, click on first item in station hangar and drag mouse to ship cargo bay
            print('found ship_cargo_hold_icon, moving items to special hold')
            (namefield_station_hangar_iconx, namefield_station_hangar_icony) = namefield_station_hangar_icon
            (ship_cargo_hold_iconx, ship_cargo_hold_icony) = ship_cargo_hold_icon
            pyautogui.moveTo((namefield_station_hangar_iconx + (random.randint(-5, 250))),
                             (namefield_station_hangar_icony + (random.randint(10, 25))),
                             mouse.move_time(), mouse.mouse_path())
            # wait up to 1 second before clicking, divide by 1000 to convert from miliseconds to seconds
            time.sleep((random.randint(0, 10) / 10))
            pyautogui.mouseDown()
            time.sleep((random.randint(0, 10) / 10))
            pyautogui.moveTo((ship_cargo_hold_iconx + (random.randint(-15, 40))),
                             (ship_cargo_hold_icony + (random.randint(14, 24))),
                             mouse.move_time(), mouse.mouse_path())
            time.sleep((random.randint(0, 10) / 10))
            pyautogui.mouseUp()
            time.sleep((random.randint(0, 10) / 10))
            # check if 'set quantity' popup appears indicating not enough room in cargo bay
            if not_enough_room_popup() == 0:
                if set_quantity_popup() == 0:
                    if special_hold_warning() == 0:
                        drag_items_to_special_hold()
                    else:
                        return
                else:
                    return
            else:
                return


def load_ship():
    print('loading ship')
    check_for_items()
    while_docked.open_station_hangar()
    while_docked.focus_inventory_window()
    print('ship loaded')
    return
