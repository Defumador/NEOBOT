import sys, pyautogui, os, time, random, ctypes
from lib import mouse, keyboard, while_docked

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 2.5
os.chdir('D:\OneDrive\Documents\personal_documents\scripting\PY-NEOBOT-GitHub\lib')

sys.setrecursionlimit(100000)
conf = 0.95


#look for 'name' column header in inventory window to indicate presence of items
def check_for_items():
    print('looking for item(s) in hangar')
    checknum = 1
    global namefield_station_hangar_icon  # var must be global since it's used in other functions
    global check_for_items_var  # return var must be global in order for other files to read it
    namefield_station_hangar_icon = pyautogui.locateCenterOnScreen('namefield_station_hangar.bmp',
                                                                   confidence=conf)
    while namefield_station_hangar_icon is None and checknum < 10:  # look for items at most 10 times
        print('looking for item(s) in hangar ...x',checknum)
        checknum += 1
        namefield_station_hangar_icon = pyautogui.locateCenterOnScreen('namefield_station_hangar.bmp',
                                                                       confidence=conf)
        if checknum >= 10:  # if loop expires, break out of loop
            break
        elif namefield_station_hangar_icon is not None:  # if found items while looping, return function
            print('found item(s) in hangar')
            check_for_items_var = 1
            return
    else:  # if found items on first loop, return function
        print('found item(s) in hangar')
        check_for_items_var = 1
        return
    print('no items in hangar')  # loop breaks to here
    check_for_items_var = 0
    return

    
def drag_items_to_cargo_hold():
    print('moving item stack to cargo hold')
    # look for 'name' column header at top of inventory window and offset mouse
    ship_cargo_hold_icon = pyautogui.locateCenterOnScreen('ship_cargo_hold.bmp',
                                                                 confidence=conf)
    while ship_cargo_hold_icon is None:
        print('cant find cargo hold')
        ship_cargo_hold_icon = pyautogui.locateCenterOnScreen('ship_cargo_hold.bmp',
                                                                     confidence=conf)
    else:  # if found icons, click on first item in station hangar and drag mouse to ship cargo hold
        print('found cargo hold')
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
        # check if 'set quantity' popup appears indicating not enough room in cargo hold
        print('moved item stack to cargo hold')
        return


def set_quantity_popup():
    # check if 'set quantity' popup appears indicating not enough room in cargo hold
    print('looking for set quantity popup')
    global set_quantity_popup_var
    set_quantity_to_deposit_in_cargo_hold_popup = \
        pyautogui.locateCenterOnScreen('set_quantity.bmp', confidence=conf)
    if set_quantity_to_deposit_in_cargo_hold_popup is None:
        print('no set quantity popup')
        set_quantity_popup_var = 0
        return
    else:
        print('found set quantity popup')
        keyboard.enter()  # confirm dialog box
        set_quantity_popup_var = 1
        return


# look for the warning indicating selected items aren't compatible with ship's special hold parameters
def special_hold_warning():
    print('looking for special hold warning')
    global special_hold_warning_var
    # special hold warning is partially transparent so confidence rating must be slightly lower than normal
    special_hold_warning = pyautogui.locateCenterOnScreen('special_hold_warning.bmp', confidence=0.8)
    if special_hold_warning is None:
        print('no special hold warning')
        special_hold_warning_var = 0
        return
    else:
        # if special hold warning appears, try dragging item to cargo hold instead
        print('detected special hold warning')
        special_hold_warning_var = 1
        return


# if ship has a specialized hold for specific items, try dragging station hangar inventory into it first
def look_for_special_hold():
    # look for drop down arrow next to ship indicating it has a special hold
    print('looking for special hold')
    global look_for_special_hold_var
    special_hold_dropown_arrow = pyautogui.locateCenterOnScreen('special_hold.bmp', confidence=conf)
    if special_hold_dropown_arrow is None:
        print('no special hold')
        look_for_special_hold_var = 0
        return
    else:
        print('found special hold')
        look_for_special_hold_var = 1
        return

# drag items from inventory into ship special hold hold
def drag_items_to_special_hold():
    # look for 'name' column header at top of inventory window and offset mouse
    print('moving item stack to special hold')
    namefield_station_hangar_icon = pyautogui.locateCenterOnScreen('namefield_station_hangar.bmp',
                                                                   confidence=conf)
    while namefield_station_hangar_icon is None:
        print('found namefield column header, moving items to special hold')
        namefield_station_hangar_icon = pyautogui.locateCenterOnScreen('namefield_station_hangar.bmp',
                                                                       confidence=conf)
    else:
        print('found namefield column header, moving items to special hold')
        # if icon found, look for ship cargo hold icon in inventory sidebar
        ship_cargo_hold_icon = pyautogui.locateCenterOnScreen('ship_cargo_hold.bmp',
                                                                     confidence=conf)
        while ship_cargo_hold_icon is None:
            print('cant find ship_cargo_hold_icon, moving items to special hold')
            ship_cargo_hold_icon = pyautogui.locateCenterOnScreen('ship_cargo_hold.bmp',
                                                                         confidence=conf)
        else:  # if found icons, click on first item in station hangar and drag mouse to ship cargo hold
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


def not_enough_room_popup():
    print('looking for not enough room popup')
    global not_enough_room_popup_var
    not_enough_room_in_hold = pyautogui.locateCenterOnScreen('not_enough_room.bmp', confidence=conf)
    if not_enough_room_in_hold is None:
        print('enough room for more items')
        not_enough_room_popup_var = 0
        return
    else:
        print('found not enough room popup')
        keyboard.enter()  # confirm dialog box
        not_enough_room_popup_var = 1
        return


def load_ship_bulk():  # load ship by selecting all item stacks and moving them all at once
    #os.chdir('C:/Users/Austin/Desktop/icons')
    print('beginning bulk loading procedure')
    global load_ship_bulk_var
    while_docked.open_station_hangar()
    check_for_items()
    if check_for_items_var == 0:  # if no items, return function
        load_ship_bulk_var = 0
        return
    elif check_for_items_var == 1:
        while_docked.focus_inventory_window()
        keyboard.select_all()
        drag_items_to_cargo_hold()
        not_enough_room_popup()  # after moving stack to cargo hold, look for warnings
        set_quantity_popup()
        if not_enough_room_popup_var == 0 and set_quantity_popup_var == 0:  # if no warnings, keep moving items
            print('done loading ship cargo hold by bulk')
            load_ship_bulk_var = 1
            return
        else:  # if warning appears, look for additional cargo hold
            look_for_special_hold()
            if look_for_special_hold_var == 1:
                while_docked.focus_inventory_window()
                keyboard.select_all()
                drag_items_to_special_hold()
                special_hold_warning()
                set_quantity_popup()
                not_enough_room_popup()
                if special_hold_warning_var == 0 and set_quantity_popup_var == 0 and not_enough_room_popup_var == 0:
                    print('done loading ship cargo and special hold by bulk')
                    load_ship_bulk_var = 1
                    return
                else:  # if warning appears, try loading items individually
                    print('ship cannot be fully loaded in bulk')
                    load_ship_bulk_var = 0
    print('ship cannot be fully loaded in bulk')
    return
    

def load_ship_individually():  # load ship one item stack at a time
    print('beginning individual loading procedure')
    global load_ship_individually_var
    while_docked.open_station_hangar()
    check_for_items()
    if check_for_items_var == 0:  # if no items, return function
        load_ship_individually_var = 0
        return
    elif check_for_items_var == 1:
        while_docked.focus_inventory_window()
        drag_items_to_cargo_hold()
        not_enough_room_popup()  # after moving stack to cargo hold, look for warnings
        set_quantity_popup()
        while not_enough_room_popup_var == 0 and set_quantity_popup_var == 0:  # if no warnings, keep moving items
            drag_items_to_cargo_hold()
            not_enough_room_popup()
            set_quantity_popup()
        else:  # if warning appears, look for additional cargo hold
            look_for_special_hold()
            if look_for_special_hold_var == 1:
                drag_items_to_special_hold()
                special_hold_warning()
                set_quantity_popup()
                not_enough_room_popup()
                while special_hold_warning_var == 0 and set_quantity_popup_var == 0 and not_enough_room_popup_var == 0:
                    drag_items_to_special_hold()  # if no warnings, keep moving items to special hold
                    special_hold_warning()
                    set_quantity_popup()
                    not_enough_room_popup()
                else:  # if warning appears, end function
                    load_ship_individually_var = 1
                    print('done loading special hold')
                    return
            else:  # if warning appears, end function
                load_ship_individually_var = 1
                print('done loading cargo hold')
                return
    print('finished loading procedure')
    return


def load_ship():  # use both individual and bulk functions to load ship
    global load_ship_var
    load_ship_bulk()
    if load_ship_bulk_var == 0:
        load_ship_individually()
    load_ship_var = 1
    return
