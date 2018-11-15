import sys, pyautogui, os, time, random, ctypes
from lib import mouse, keyboard, while_docked

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 2.5
os.chdir('D:\OneDrive\Documents\personal_documents\scripting\PY-NEOBOT-GitHub\lib')

sys.setrecursionlimit(100000)
conf = 0.95
x = 1


def check_for_items():
    print('looking for item(s) in hangar')
    global namefield_station_hangar_icon
    namefield_station_hangar_icon = pyautogui.locateCenterOnScreen('namefield_station_hangar_icon.png',
                                                                   confidence=conf)
    if namefield_station_hangar_icon is None:
        print('looking for item(s) in hangar ...x'x)
        global x
        while x < 10: #try 10 times to locate icon
            x += 1
            check_for_items()
        else:
            x = 1
            print('no items in hangar')
            check_for_items = 0
            return check_for_items
    else:
        print('found item(s) in hangar')
        check_for_items = 1
        return check_for_items

    
def drag_items_to_cargo_bay():
    print('moving item stack to cargo bay')
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
        print('moved item stack to cargo bay')
        return


def set_quantity_popup():
    # check if 'set quantity' popup appears indicating not enough room in cargo bay
    print('looking for set quantity popup')
    set_quantity_to_deposit_in_cargo_bay_popup = \
        pyautogui.locateCenterOnScreen('set_quantity_to_deposit_in_cargo_bay_popup.png', confidence=conf)
    if set_quantity_to_deposit_in_cargo_bay_popup is None:
        print('no set quantity popup')
        set_quantity_popup = 0
        return set_quantity_popup
    else:
        print('found set quantity popup')
        keyboard.enter()  # confirm dialog box
        set_quantity_popup = 1
        return set_quantity_popup


def not_enough_room_popup():
    print('looking for not enough room popup')
    os.chdir('c:/users/austin/desktop/icons')
    not_enough_room_in_hold = pyautogui.locateCenterOnScreen('not_enough_room_in_hold.png', confidence=conf)
    if not_enough_room_in_hold is None:
        print('enough room for more items')
        not_enough_room_popup = 0
        return not_enough_room_popup
    else:
        print('found not enough room popup')
        keyboard.enter()  # confirm dialog box
        not_enough_room_popup = 1
        return not_enough_room_popup

    
# if ship has a specialized hold for specific items, try dragging station hangar inventory into it first
def look_for_special_hold():
    # look for drop down arrow next to ship indicating it has a special hold
    print('looking for special hold')
    special_hold_dropown_arrow = pyautogui.locateCenterOnScreen('hold.png', confidence=conf)
    if special_hold_dropown_arrow is None:
        print('no special hold')
        look_for_special_hold = 0
        return look_for_special_hold
    else:
        print('found special hold')
        look_for_special_hold = 1
        return look_for_special_hold


# look for the warning indicating selected items aren't compatible with ship's special hold parameters
def special_hold_warning():
    print('looking for special hold warning')
    # special hold warning is partially transparent so confidence rating must be slightly lower than normal
    special_hold_warning = pyautogui.locateCenterOnScreen('special_hold_warning.png', confidence=0.8)
    if special_hold_warning is None:
        print('no special hold warning')
        special_hold_warning = 0
        return special_hold_warning
    else:
        # if special hold warning appears, try dragging item to cargo bay instead
        print('detected special hold warning')
        special_hold_warning = 1
        return special_hold_warning


# drag items from inventory into ship special hold bay
def drag_items_to_special_hold():
    # look for 'name' column header at top of inventory window and offset mouse
    print('moving item stack to special hold')
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
            pyautogui.mouseDown()
            pyautogui.moveTo((ship_cargo_hold_iconx + (random.randint(-15, 40))),
                             (ship_cargo_hold_icony + (random.randint(14, 24))),
                             mouse.move_time(), mouse.mouse_path())
            pyautogui.mouseUp()
            print('moved item stack to special hold')
            return


def load_ship():
    print('beginning loading procedure')
    while_docked.open_station_hangar()
    check_for_items()
    if check_for_items = 0
        load_ship = 1
        return load_ship
    elif check_for_items = 1
        while_docked.focus_inventory_window()
        drag_items_to_cargo_bay()
        not_enough_room_popup()
        if not_enough_room_popup = 0
            set_quantity_popup()
            if set_quantity_popup = 0
                load_ship()
            elif set_quantity_popup = 1
                look_for_special_hold()
                if look_for_special_hold = 1
                    drag_items_to_special_hold()
                    special_hold_warning()
                    while special_hold_warning = 0
                        set_quantity_popup()
                        if set_quantity_popup = 0
                            not_enough_room()
                            if not_enough_room = 0
                                drag_items_to_special_hold()
                                special_hold_warning()
                            elif special_hold warning = 1
                                load_ship = 1
                                print('ending loading procedure')
                                return load_ship
                        elif set_quantity_popup = 1
                            load_ship = 1
                            print('ending loading procedure')
                            return load_ship
                    elif not_enough_room_popup = 1
                        load_ship = 1
                        print('ending loading procedure')
                        return load_ship
                elif look_for_special_hold = 0
                    load_ship = 1
                    print('ending loading procedure')
                    return load_ship
        elif not_enough_room_popup = 1
            look_for_special_hold()
            if look_for_special_hold = 1
                drag_items_to_special_hold()
                special_hold_warning()
                while special_hold_warning = 0
                    set_quantity_popup()
                    if set_quantity_popup = 0
                        not_enough_room()
                        if not_enough_room = 0
                            drag_items_to_special_hold()
                            special_hold_warning()
                        elif special_hold warning = 1
                            load_ship = 1
                            print('ending loading procedure')
                            return load_ship
                    elif set_quantity_popup = 1
                        load_ship = 1
                        print('ending loading procedure')
                        return load_ship
                elif not_enough_room_popup = 1
                    load_ship = 1
                    print('ending loading procedure')
                    return load_ship
            elif look_for_special_hold = 0
                load_ship = 1
                print('ending loading procedure')
                return load_ship
    print('done loading ship')        
    return
