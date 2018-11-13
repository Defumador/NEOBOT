import sys, pyautogui, os, time, random, ctypes
from lib import mouse, keyboard, navigation

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 2.5
sys.setrecursionlimit(100000)
conf = 0.95


# check if ship is docked
def docked_check():
    undock_icon = pyautogui.locateCenterOnScreen('undock_icon.png', confidence=conf)
    if undock_icon is None:
        print('not docked')
        navigation.select_waypoint()
    elif undock_icon is not None:
        print('docked')
        navigation.at_home_check()


#def open_ship_cargo_bay():


def open_station_hangar():  # click on station hangar button in inventory window while docked
    os.chdir('c:/users/austin/desktop/icons')
    station_hangar_icon = pyautogui.locateCenterOnScreen('inventory_station_hangar_icon.png',
                                                         confidence=conf)
    while station_hangar_icon is None:
        print('cant find inventory_station_hangar_icon')
        station_hangar_icon = pyautogui.locateCenterOnScreen('inventory_station_hangar_icon.png',
                                                             confidence=conf)
    else:
        print('found inventory_station_hangar_icon')
        (station_hangar_iconx, station_hangar_icony) = station_hangar_icon
        # clicks the center of where the button was found
        pyautogui.moveTo((station_hangar_iconx + (random.randint(-6, 6))),
                         (station_hangar_icony + (random.randint(-6, 6))),
                         mouse.move_time(), mouse.mouse_path())
        mouse.click()
        return


def focus_inventory_window():  # click inside the station inventory window to focus it before items are selected
    # look for sorting buttons in top right corner of inventory window and offset mouse
    os.chdir('c:/users/austin/desktop/icons')
    sorting_station_hangar_icon = pyautogui.locateCenterOnScreen('sorting_station_hangar_icon.png',
                                                                 confidence=conf)
    while sorting_station_hangar_icon is None:
        print('cant find sorting_station_hangar_icon')
        sorting_station_hangar_icon = pyautogui.locateCenterOnScreen('sorting_station_hangar_icon.png',
                                                                     confidence=conf)
    else:
        print('found sorting_station_hangar_icon')
        (sorting_station_hangar_iconx, sorting_station_hangar_icony) = sorting_station_hangar_icon
        # offset mouse from sorting button to click within inventory window to focus it
        pyautogui.moveTo((sorting_station_hangar_iconx - (random.randint(40, 300))),
                         (sorting_station_hangar_icony + (random.randint(40, 300))),
                         mouse.move_time(), mouse.mouse_path())
        mouse.click()
        return


def undock():
    os.chdir('c:/users/austin/desktop/icons')
    undock_icon = pyautogui.locateCenterOnScreen('undock_icon.png', confidence=conf)
    while undock_icon is None:
        print('cant find undock button')
        undock_icon = pyautogui.locateCenterOnScreen('undock_icon.png', confidence=conf)
    else:
        print('undocking')
        (undock_iconx, undock_icony) = undock_icon
        # clicks the center of where the button was found
        pyautogui.moveTo((undock_iconx + (random.randint(-25, 25))),
                         (undock_icony + (random.randint(-15, 15))),
                         mouse.move_time(), mouse.mouse_path())
        mouse.click()
        pyautogui.moveRel((-1 * (random.randint(10, 1000))), (random.randint(40, 1000)),
                          mouse.move_time(), mouse.mouse_path())  # move mouse away from button
        time.sleep(10)  # wait for undock to complete
        navigation.select_waypoint()
