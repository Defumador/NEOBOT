from lib import mouse, keyboard, traveler, unload_ship, navigation
import sys, pyautogui, os, time, random, ctypes

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 2.5
os.chdir('D:\OneDrive\Documents\Scripts\Python\PY-NEOBOT-GitHub\lib')


sys.setrecursionlimit(100000)
conf = 0.95


def drag_items_from_cargo_bay():
    # first select ship inventory
    os.chdir('c:/users/austin/desktop/icons')
    inventory_current_ship_icon = pyautogui.locateCenterOnScreen('inventory_current_ship_icon.png',
                                                                 confidence=conf)
    while inventory_current_ship_icon is None:
        print('cant find inventory_current_ship_icon')
        inventory_current_ship_icon = pyautogui.locateCenterOnScreen('inventory_current_ship_icon.png',
                                                                     confidence=conf)
    else:
        print('unloading cargo bay')
        (inventory_current_ship_iconx, inventory_current_ship_icony) = inventory_current_ship_icon
        # clicks the center of where the button was found
        pyautogui.moveTo((inventory_current_ship_iconx + (random.randint(-6, 6))),
                         (inventory_current_ship_icony + (random.randint(-6, 6))),
                         mouse.move_time(), mouse.mouse_path())

        mouse.click()
        while_docked.focus_inventory_window()
        keyboard.select_all()  # select all items in ship cargo bay

        # dragitems to station item hangar
        # look for 'name' column header at top of inventory window and offset mouse
        namefield_station_hangar_icon = pyautogui.locateCenterOnScreen('namefield_station_hangar_icon.png',
                                                                       confidence=conf)
        (namefield_station_hangar_iconx, namefield_station_hangar_icony) = namefield_station_hangar_icon
        pyautogui.moveTo((namefield_station_hangar_iconx + (random.randint(-5, 200))),
                         (namefield_station_hangar_icony + (random.randint(10, 20))),
                         mouse.move_time(), mouse.mouse_path())
        # wait up to 1 second before clicking, divide by 1000 to convert from miliseconds to seconds
        time.sleep((random.randint(0, 10) / 10))
        pyautogui.mouseDown()
        time.sleep((random.randint(0, 10) / 10))
        inventory_station_hangar_icon = pyautogui.locateCenterOnScreen('inventory_station_hangar_icon.png',
                                                                       confidence=conf)
        (inventory_station_hangar_iconx, inventory_station_hangar_icony) = inventory_station_hangar_icon
        pyautogui.moveTo((inventory_station_hangar_iconx + (random.randint(-15, 40))),
                         (inventory_station_hangar_icony + (random.randint(-10, 10))),
                         mouse.move_time(), mouse.mouse_path())
        time.sleep((random.randint(0, 10) / 10))
        pyautogui.mouseUp()
        time.sleep((random.randint(0, 10) / 10))
        # after unloading main cargo hold, look for special cargo hold
        drag_items_from_special_hold()


# drag items from inventory into ship special hold bay
def drag_items_from_special_hold():
    # check if ship has specialized bay that needs to be unloaded
    load_ship.look_for_special_hold()
    if load_ship.look_for_special_hold() == 1:
        print('unloading special hold')
        inventory_current_ship_icon = pyautogui.locateCenterOnScreen('inventory_current_ship_icon.png',
                                                                     confidence=conf)
        (inventory_current_ship_iconx, inventory_current_ship_icony) = inventory_current_ship_icon
        pyautogui.moveTo((inventory_current_ship_iconx + (random.randint(-10, 40))),
                         (inventory_current_ship_icony + (random.randint(14, 24))),
                         mouse.move_time(), mouse.mouse_path())

        mouse.click()
        while_docked.focus_inventory_window()
        keyboard.select_all()  # select all items in special bay

        namefield_station_hangar_icon = pyautogui.locateCenterOnScreen('namefield_station_hangar_icon.png',
                                                                       confidence=conf)
        (namefield_station_hangar_iconx, namefield_station_hangar_icony) = namefield_station_hangar_icon
        pyautogui.moveTo((namefield_station_hangar_iconx + (random.randint(-5, 200))),
                         (namefield_station_hangar_icony + (random.randint(10, 20))),
                         mouse.move_time(), mouse.mouse_path())
        # wait up to 1 second before clicking, divide by 1000 to convert from miliseconds to seconds
        time.sleep((random.randint(0, 10) / 10))
        pyautogui.mouseDown()
        time.sleep((random.randint(0, 10) / 10))
        inventory_station_hangar_icon = pyautogui.locateCenterOnScreen('inventory_station_hangar_icon.png',
                                                                       confidence=conf)
        (inventory_station_hangar_iconx, inventory_station_hangar_icony) = inventory_station_hangar_icon
        pyautogui.moveTo((inventory_station_hangar_iconx + (random.randint(-15, 40))),
                         (inventory_station_hangar_icony + (random.randint(-10, 10))),
                         mouse.move_time(), mouse.mouse_path())
        time.sleep((random.randint(0, 10) / 10))
        pyautogui.mouseUp()
        print('special hold unloaded')
        time.sleep((random.randint(0, 10) / 10))
        return
    else:
        return


def unload_ship():
    print('unloading ship')
    drag_items_from_cargo_bay()
    print('ship unloaded')
    while_docked.undock()
    return