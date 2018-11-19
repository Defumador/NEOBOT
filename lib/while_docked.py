import sys, pyautogui, os, time, random, ctypes
from lib import mouse, keyboard, navigation

pyautogui.FAILSAFE = True
sys.setrecursionlimit(100000)
conf = 0.95


# check if ship is docked
def docked_check():
    print('checking if docked')
    global docked_check_var
    undock_icon = pyautogui.locateCenterOnScreen('undock.bmp', confidence=conf)
    if undock_icon is None:
        print('not docked')
        docked_check_var = 0
        return
    elif undock_icon is not None:
        print('docked')
        docked_check_var = 1
        return


def open_cargo_hold():  # click on ship cargo hold button in inventory window while docked
    print('opening cargo hold')
    cargo_hold = pyautogui.locateCenterOnScreen('cargo_hold.bmp',
                                                                 confidence=conf)
    while cargo_hold is None:
        print('cant find cargo hold')
        cargo_hold = pyautogui.locateCenterOnScreen('cargo_hold.bmp',
                                                                     confidence=conf)
    else:
        (cargo_holdx, cargo_holdy) = cargo_hold
        # clicks the center of where the button was found
        pyautogui.moveTo((cargo_holdx + (random.randint(-4, 50))),
                         (cargo_holdy + (random.randint(-6, 6))),
                         mouse.move_time(), mouse.mouse_path())

        mouse.click()
        return


def open_special_hold():
    print('opening special hold')
    special_hold = pyautogui.locateCenterOnScreen('special_hold.bmp',
                                                confidence=conf)
    while special_hold is None:
        print('cant find special hold')
        special_hold = pyautogui.locateCenterOnScreen('special_hold.bmp',
                                                    confidence=conf)
    else:
        (special_holdx, special_holdy) = special_hold
        # clicks the center of where the button was found
        pyautogui.moveTo((special_holdx + (random.randint(-4, 50))),
                         (special_holdy + (random.randint(15, 30))),
                         mouse.move_time(), mouse.mouse_path())

        mouse.click()
        return


def open_station_hangar():  # click on station hangar button in inventory window while docked
    print('opening station hangar')
    station_hangar = pyautogui.locateCenterOnScreen('station_hangar.bmp',
                                                         confidence=conf)
    while station_hangar is None:
        print('cant find inventory station hangar icon')
        station_hangar = pyautogui.locateCenterOnScreen('station_hangar.bmp',
                                                             confidence=conf)
    else:
        (station_hangarx, station_hangary) = station_hangar
        # clicks the center of where the button was found
        pyautogui.moveTo((station_hangarx + (random.randint(-6, 50))),
                         (station_hangary + (random.randint(-6, 6))),
                         mouse.move_time(), mouse.mouse_path())
        mouse.click()
        return


def focus_inventory_window():  # click inside the station inventory window to focus it before items are selected
    # look for sorting buttons in top right corner of inventory window and offset mouse
    print('focusing inventory window')
    sorting_station_hangar = pyautogui.locateCenterOnScreen('sorting_station_hangar.bmp',
                                                                 confidence=conf)
    while sorting_station_hangar is None:
        print('cant find sorting icon')
        sorting_station_hangar = pyautogui.locateCenterOnScreen('sorting_station_hangar.bmp',
                                                                     confidence=conf)
    else:
        (sorting_station_hangarx, sorting_station_hangary) = sorting_station_hangar
        # offset mouse from sorting button to click within inventory window to focus it
        pyautogui.moveTo((sorting_station_hangarx - (random.randint(0, 250))),
                         (sorting_station_hangary + (random.randint(50, 300))),
                         mouse.move_time(), mouse.mouse_path())
        mouse.click()
        return


#look for 'name' column header in inventory window to indicate presence of items
def look_for_items():
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


# if ship has a specialized hold for specific items, try dragging station hangar inventory into it first
def look_for_special_hold():
    # look for drop down arrow next to ship indicating it has a special hold
    print('looking for special hold')
    global look_for_special_hold_var
    special_hold = pyautogui.locateCenterOnScreen('special_hold.bmp', confidence=conf)
    if special_hold is None:
        print('no special hold')
        look_for_special_hold_var = 0
        return
    else:
        print('found special hold')
        look_for_special_hold_var = 1
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


def set_quantity_popup():
    # check if 'set quantity' popup appears indicating not enough space in cargo hold
    print('looking for set quantity popup')
    global set_quantity_popup_var
    set_quantity = \
        pyautogui.locateCenterOnScreen('set_quantity.bmp', confidence=conf)
    if set_quantity is None:
        print('no set quantity popup')
        set_quantity_popup_var = 0
        return
    else:
        print('found set quantity popup')
        keyboard.enter()  # confirm dialog box
        set_quantity_popup_var = 1
        return


def not_enough_space_popup():
    print('looking for not enough space popup')
    global not_enough_space_popup_var
    not_enough_space = pyautogui.locateCenterOnScreen('not_enough_space.bmp', confidence=conf)
    if not_enough_space is None:
        print("no 'not enough space' popup")
        not_enough_space_popup_var = 0
        return
    else:
        print('found not enough space popup')
        keyboard.enter()  # confirm dialog box
        not_enough_space_popup_var = 1
        return


def undock():
    print('began undocking procedure')
    undock = pyautogui.locateCenterOnScreen('undock.bmp', confidence=conf)
    while undock is None:
        print('cant find undock button')
        undock = pyautogui.locateCenterOnScreen('undock.bmp', confidence=conf)
    else:
        (undockx, undocky) = undock
        # clicks the center of where the button was found
        pyautogui.moveTo((undockx + (random.randint(-25, 25))),
                         (undocky + (random.randint(-15, 15))),
                         mouse.move_time(), mouse.mouse_path())
        mouse.click()
        pyautogui.moveRel((-1 * (random.randint(200, 1000))), (random.randint(-600, 600)),
                          mouse.move_time(), mouse.mouse_path())  # move mouse away from button
        time.sleep((random.randint(10, 250) / 10))  # wait for undock to complete
        print('finished undocking')
        return