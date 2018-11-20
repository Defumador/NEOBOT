import sys, pyautogui, os, time, random, ctypes
from lib import mouse, keyboard, while_docked, navigation

pyautogui.FAILSAFE = True

sys.setrecursionlimit(100000)
conf = 0.95


def drag_items_to_cargo_hold():
    print('moving item stack to cargo hold')
    global namefield_station_hangar
    # look for 'name' column header at top of inventory window and offset mouse
    cargo_hold = pyautogui.locateCenterOnScreen('cargo_hold.bmp',
                                                                 confidence=conf)
    while cargo_hold is None:
        print('cant find cargo hold')
        cargo_hold = pyautogui.locateCenterOnScreen('cargo_hold.bmp',
                                                                     confidence=conf)
    else:  # if found icons, click on first item in station hangar and drag mouse to ship cargo hold
        print('found cargo hold')
        (namefield_station_hangarx, namefield_station_hangary) = while_docked.namefield_station_hangar
        (ship_cargo_holdx, ship_cargo_holdy) = cargo_hold
        pyautogui.moveTo((namefield_station_hangarx + (random.randint(-5, 250))),
                         (namefield_station_hangary + (random.randint(10, 25))),
                         mouse.move_time(), mouse.mouse_path())
        pyautogui.mouseDown()
        pyautogui.moveTo((ship_cargo_holdx + (random.randint(-5, 60))),
                         (ship_cargo_holdy + (random.randint(-8, 8))),
                         mouse.move_time(), mouse.mouse_path())
        pyautogui.mouseUp()
        # check if 'set quantity' popup appears indicating not enough space in cargo hold
        print('moved item stack to cargo hold')
        return


# drag items from inventory into ship special hold hold
def drag_items_to_special_hold():
    # look for 'name' column header at top of inventory window and offset mouse
    print('moving item stack to special hold')
    namefield_station_hangar = pyautogui.locateCenterOnScreen('namefield_station_hangar.bmp',
                                                                   confidence=conf)
    while namefield_station_hangar is None:
        print('found namefield column header, moving items to special hold')
        namefield_station_hangar = pyautogui.locateCenterOnScreen('namefield_station_hangar.bmp',
                                                                       confidence=conf)
    else:
        print('found namefield column header, moving items to special hold')
        # if icon found, look for ship cargo hold icon in inventory sidebar
        cargo_hold = pyautogui.locateCenterOnScreen('cargo_hold.bmp',
                                                                     confidence=conf)
        while cargo_hold is None:
            print('cant find ship_cargo_hold_icon, moving items to special hold')
            cargo_hold = pyautogui.locateCenterOnScreen('cargo_hold.bmp',
                                                                         confidence=conf)
        else:  # if found icons, click on first item in station hangar and drag mouse to ship cargo hold
            print('found ship_cargo_hold_icon, moving items to special hold')
            (namefield_station_hangarx, namefield_station_hangary) = namefield_station_hangar
            (cargo_holdx, cargo_holdy) = cargo_hold
            pyautogui.moveTo((namefield_station_hangarx + (random.randint(-5, 250))),
                             (namefield_station_hangary + (random.randint(10, 25))),
                             mouse.move_time(), mouse.mouse_path())
            # wait up to 1 second before clicking, divide by 1000 to convert from miliseconds to seconds
            pyautogui.mouseDown()
            pyautogui.moveTo((cargo_holdx + (random.randint(-15, 40))),
                             (cargo_holdy + (random.randint(14, 24))),
                             mouse.move_time(), mouse.mouse_path())
            pyautogui.mouseUp()
            print('moved item stack to special hold')
            return


def load_ship_bulk():  # load ship by selecting all item stacks and moving them all at once
    #os.chdir('C:/Users/Austin/Desktop/icons')
    print('beginning bulk loading procedure')
    global load_ship_bulk_var
    while_docked.open_station_hangar()
    while_docked.look_for_items()
    if while_docked.look_for_items_var == 0:  # if no items, return function
        load_ship_bulk_var = 0  # 0 indicating station is already empty
        return
    elif while_docked.look_for_items_var == 1:
        while_docked.focus_inventory_window()
        keyboard.select_all()
        drag_items_to_cargo_hold()
        time.sleep(2)
        while_docked.not_enough_space_popup()  # after moving stack to cargo hold, look for warnings
        while_docked.set_quantity_popup()
        if while_docked.not_enough_space_popup_var == 0 and while_docked.set_quantity_popup_var == 0:  # if no warnings, keep moving items
            print('done loading ship cargo hold by bulk')
            load_ship_bulk_var = 2  # 2 indicating ship is full and hangar is completley empty
            return
        else:  # if warning appears, look for additional cargo hold
            while_docked.look_for_special_hold()
            if while_docked.look_for_special_hold_var == 1:
                while_docked.focus_inventory_window()
                keyboard.select_all()
                drag_items_to_special_hold()
                time.sleep(2)
                while_docked.special_hold_warning()
                while_docked.set_quantity_popup()
                while_docked.not_enough_space_popup()
                if while_docked.special_hold_warning_var == 0 and while_docked.set_quantity_popup_var == 0\
                        and while_docked.not_enough_space_popup_var == 0:
                    while_docked.look_for_items()
                    if while_docked.look_for_items_var == 0:
                        print('done loading ship cargo and special hold by bulk')
                        load_ship_bulk_var = 2  # 2 indicating ship is full and hangar is completley empty
                        return
                    else:
                        print('more items remaining')
                        load_ship_bulk_var = 0  # 0 indicating ship cannot be fully loaded in bulk
                        return
                elif while_docked.special_hold_warning_var == 0 and while_docked.set_quantity_popup_var == 1\
                        and while_docked.not_enough_space_popup_var == 0:
                    print('done loading ship cargo and special hold by bulk but more items remain in station')
                    load_ship_bulk_var = 1  # 1 indicating ship is full but more items remain in hangar
                    return
                else:  # if warning appears, try loading items individually
                    print('ship cannot be fully loaded in bulk')
                    load_ship_bulk_var = 0  # 0 indicating ship cannot be fully loaded in bulk
    print('ship cannot be fully loaded in bulk')
    return
    

def load_ship_individually():  # load ship one item stack at a time
    print('beginning individual loading procedure')
    global load_ship_individually_var
    while_docked.open_station_hangar()
    while_docked.look_for_items()
    if while_docked.look_for_items_var == 0:  # if no items, return function
        load_ship_individually_var = 2  # 2 indicating ship is full and hangar is completley empty
        return
    elif while_docked.look_for_items_var == 1:
        while_docked.focus_inventory_window()
        drag_items_to_cargo_hold()
        time.sleep(2)
        while_docked.not_enough_space_popup()  # after moving stack to cargo hold, look for warnings
        while_docked.set_quantity_popup()
        while_docked.look_for_items()
        while while_docked.not_enough_space_popup_var == 0 and while_docked.set_quantity_popup_var == 0\
                and while_docked.look_for_items_var == 1:  # if no warnings, keep moving items
            drag_items_to_cargo_hold()
            time.sleep(2)
            while_docked.not_enough_space_popup()
            while_docked.set_quantity_popup()
            while_docked.look_for_items()
        if while_docked.not_enough_space_popup_var == 0 and while_docked.set_quantity_popup_var == 0\
                and while_docked.look_for_items_var == 0:
            load_ship_individually_var = 2  # 2 indicating ship is full and hangar is completley empty
            print('done loading main hold')
            return
        elif (while_docked.not_enough_space_popup_var == 1 or while_docked.set_quantity_popup_var == 1)\
                and while_docked.look_for_items_var == 1:  # if warning appears, look for additional cargo hold
            while_docked.look_for_special_hold()
            if while_docked.look_for_special_hold_var == 1:
                drag_items_to_special_hold()
                time.sleep(2)
                while_docked.special_hold_warning()
                while_docked.set_quantity_popup()
                while_docked.not_enough_space_popup()
                while_docked.look_for_items()
                while while_docked.special_hold_warning_var == 0 and while_docked.set_quantity_popup_var == 0\
                        and while_docked.not_enough_space_popup_var == 0 and while_docked.look_for_items_var == 1:
                    drag_items_to_special_hold()  # if no warnings, keep moving items to special hold
                    time.sleep(2)
                    while_docked.special_hold_warning()
                    while_docked.set_quantity_popup()
                    while_docked.not_enough_space_popup()
                    while_docked.look_for_items()
                if while_docked.look_for_items_var == 0:
                    load_ship_individually_var = 2  # 2 indicating ship is full and hangar is completley empty
                    print('done loading special hold')
                    return
                elif while_docked.special_hold_warning_var == 1 or while_docked.set_quantity_popup_var == 1\
                        or while_docked.not_enough_space_popup_var == 1:
                    load_ship_individually_var = 1  # 1 indicating ship is full but more items remain in hangar
                    print('done loading special hold but more items remain in station')
                    return
        else:
            load_ship_individually_var = 1  # 1 indicating ship is full but more items remain in hangar
            print('done loading cargo hold but more items remain in station')
            return
    print('finished loading procedure')
    return


def load_ship():  # use both individual and bulk functions to load ship
    global load_ship_var
    load_ship_bulk()
    if load_ship_bulk_var == 2:  # if function returns 2, station is empty
        load_ship_var = 2 # 2 indicating ship is full and hangar is completley empty
        print('ship loaded entire hangar')
        return
    elif load_ship_bulk_var == 1:  # if function returns 2, station is empty
        load_ship_var = 1 # 2 indicating ship is full and hangar is completley empty
        print('ship is full but hangar has more items')
        return
    elif load_ship_bulk_var == 0:
        load_ship_individually()
        if load_ship_individually_var == 2:
            print('ship loaded entire hangar')
            load_ship_var = 2  # 2 indicating ship is full and hangar is completley empty
            return
        elif load_ship_individually_var == 1:
            print('ship full but more items remain')
            load_ship_var = 1  # 1 indicating ship is full but hangar still has more items
            return
