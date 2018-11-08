import sys  # import module to allow for Random command in ahk
from lib.mouse import *

pyautogui.PAUSE = 2.5
os.chdir('D:\OneDrive\Documents\Scripts\Python\PY-NEOBOT-GitHub\lib')


def open_station_hangar():  # click on station hangar button in inventory window while docked
    station_hangar_icon = pyautogui.locateCenterOnScreen('inventory_station_hangar_icon.png')
    if station_hangar_icon is None:
        print('cant find inventory_station_hangar_icon')
        sys.exit()
    else:
        (station_hangar_iconx, station_hangar_icony) = station_hangar_icon
        pyautogui.moveTo(station_hangar_iconx, station_hangar_icony, move_time(), mouse_path())  # clicks the center of where the button was found
        click()
        return


def focus_inventory_window():  # click inside the station inventory window to focus it before items are selected
    sorting_station_hangar_icon = pyautogui.locateCenterOnScreen(
        'sorting_station_hangar_icon.png')  # look for sorting buttons in top right corner of inventory window and offset mouse
    if sorting_station_hangar_icon is None:
        print('cant find sorting_station_hangar_icon')
        sys.exit()
    else:
        (sorting_station_hangar_iconx, sorting_station_hangar_icony) = sorting_station_hangar_icon
        pyautogui.moveTo((sorting_station_hangar_iconx - (random.randint(10, 100))), (sorting_station_hangar_icony + (random.randint(10, 100))), move_time(), mouse_path())  # clicks the center of where the button was found
        click()
        return


def drag_items_to_cargo_bay():  # drag items from inventory into ship cargo bay
    namefield_station_hangar_icon = pyautogui.locateCenterOnScreen('namefield_station_hangar_icon.png')  # look for 'name' column header at top of inventory window and offset mouse
    if namefield_station_hangar_icon is None:
        print('cant find namefield_station_hangar_icon')
        sys.exit()
    else:
        inventory_current_ship_icon = pyautogui.locateCenterOnScreen('inventory_current_ship_icon.png')  # if icon found, look for ship cargo bay icon in inventory sidebar
        if inventory_current_ship_icon is None:
            print('cant find inventory_current_ship_icon')
            sys.exit()
        else:  # if found icons, click on first item in station hangar and drag mouse to ship cargo bay
            (namefield_station_hangar_iconx, namefield_station_hangar_icony) = namefield_station_hangar_icon
            (inventory_current_ship_iconx, inventory_current_ship_icony) = inventory_current_ship_icon
            pyautogui.moveTo(namefield_station_hangar_iconx, namefield_station_hangar_icony, move_time(), mouse_path())
            pyautogui.PAUSE = (random.randint(0, 1000) / 1000)  # wait up to 1 second before clicking, divide by 1000 to convert from miliseconds to seconds
            pyautogui.mouseDown()
            pyautogui.PAUSE = (random.randint(0, 1000) / 1000)
            pyautogui.moveTo(inventory_current_ship_iconx, inventory_current_ship_icony, move_time(), mouse_path())
            pyautogui.PAUSE = (random.randint(0, 1000) / 1000)
            pyautogui.mouseUp()
            pyautogui.PAUSE = (random.randint(0, 1000) / 1000)
            return


def undock():
    undock_icon = pyautogui.locateCenterOnScreen('undock_icon.png')
    if undock_icon is None:
        print('cant find undock_icon')
        sys.exit()
    else:
        print('undocking')
        (undock_iconx, undock_icony) = undock_icon
        pyautogui.moveTo(undock_iconx, undock_icony, move_time(), mouse_path())  # clicks the center of where the button was found
        click()
        return
