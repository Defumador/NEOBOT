import sys, pyautogui, os, time, random, ctypes
from lib import mouse, keyboard, navigation

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 2.5
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


#def open_ship_cargo_hold():


def open_station_hangar():  # click on station hangar button in inventory window while docked
    print('opening station hangar')
    station_hangar_icon = pyautogui.locateCenterOnScreen('station_hangar.bmp',
                                                         confidence=conf)
    while station_hangar_icon is None:
        print('cant find inventory station hangar icon')
        station_hangar_icon = pyautogui.locateCenterOnScreen('station_hangar.bmp',
                                                             confidence=conf)
    else:
        (station_hangar_iconx, station_hangar_icony) = station_hangar_icon
        # clicks the center of where the button was found
        pyautogui.moveTo((station_hangar_iconx + (random.randint(-6, 50))),
                         (station_hangar_icony + (random.randint(-6, 6))),
                         mouse.move_time(), mouse.mouse_path())
        mouse.click()
        return


def focus_inventory_window():  # click inside the station inventory window to focus it before items are selected
    # look for sorting buttons in top right corner of inventory window and offset mouse
    print('focusing inventory window')
    sorting_station_hangar_icon = pyautogui.locateCenterOnScreen('sorting_station_hangar.bmp',
                                                                 confidence=conf)
    while sorting_station_hangar_icon is None:
        print('cant find sorting icon')
        sorting_station_hangar_icon = pyautogui.locateCenterOnScreen('sorting_station_hangar.bmp',
                                                                     confidence=conf)
    else:
        (sorting_station_hangar_iconx, sorting_station_hangar_icony) = sorting_station_hangar_icon
        # offset mouse from sorting button to click within inventory window to focus it
        pyautogui.moveTo((sorting_station_hangar_iconx - (random.randint(0, 250))),
                         (sorting_station_hangar_icony + (random.randint(50, 300))),
                         mouse.move_time(), mouse.mouse_path())
        mouse.click()
        return


def undock():
    print('began undocking procedure')
    undock_icon = pyautogui.locateCenterOnScreen('undock.bmp', confidence=conf)
    while undock_icon is None:
        print('cant find undock button')
        undock_icon = pyautogui.locateCenterOnScreen('undock.bmp', confidence=conf)
    else:
        (undock_iconx, undock_icony) = undock_icon
        # clicks the center of where the button was found
        pyautogui.moveTo((undock_iconx + (random.randint(-25, 25))),
                         (undock_icony + (random.randint(-15, 15))),
                         mouse.move_time(), mouse.mouse_path())
        mouse.click()
        pyautogui.moveRel((-1 * (random.randint(10, 1000))), (random.randint(40, 1000)),
                          mouse.move_time(), mouse.mouse_path())  # move mouse away from button
        time.sleep(10)  # wait for undock to complete
        print('finished undocking')
        return
