import sys, time, random
import pyautogui as pag
from lib import mouse, keyboard, docked
from lib.vars import originx, originy, windowx, windowy, conf

sys.setrecursionlimit(9999999)


def drag_items_from_ship_inv():
    # Click and drag all items from ship inventory to station inventory.
    namefield_station_inv_icon = pag.locateCenterOnScreen(
        './img/indicators/station_inv_name.bmp',
        confidence=conf,
        region=(originx, originy, windowx, windowy))

    (namefield_station_inv_iconx,
     namefield_station_inv_icony) = namefield_station_inv_icon
    pag.moveTo((namefield_station_inv_iconx + (random.randint(-5, 250))),
               (namefield_station_inv_icony + (random.randint(10, 25))),
               mouse.duration(), mouse.path())

    pag.mouseDown()
    station_inv = pag.locateCenterOnScreen('./img/buttons/station_inv.bmp',
                                           confidence=conf,
                                           region=(originx, originy,
                                                   windowx, windowy))
    (station_invx, station_invy) = station_inv
    pag.moveTo((station_invx + (random.randint(-15, 60))),
               (station_invy + (random.randint(-10, 10))),
               mouse.duration(), mouse.path())
    pag.mouseUp()
    print(
        'drag_items_from_ship_inv -- moved all item stacks from ship '
        'inventory')
    return


def unload_ship():
    print('unload_ship -- began unloading procedure')
    docked.open_ship_inv()
    specinv = docked.look_for_spec_inv()
    items = docked.look_for_items()

    if docked.look_for_items() == 0:
        docked.look_for_spec_inv()
        if specinv == 1:
            # Wait between 0 and 2s before actions for increased randomness.
            time.sleep(float(random.randint(0, 2000)) / 1000)
            docked.open_spec_inv_ore()
            items = docked.look_for_items()

            while items == 1:
                time.sleep(float(random.randint(0, 2000)) / 1000)
                docked.focus_inv_window()
                time.sleep(float(random.randint(0, 2000)) / 1000)
                keyboard.select_all()
                time.sleep(float(random.randint(0, 2000)) / 1000)
                drag_items_from_ship_inv()
                time.sleep(2)
                docked.look_for_items()
                print('unload_ship -- finished unloading procedure')
                return 1

            if items == 0:
                print('unload_ship -- finished unloading procedure')
                return 1

        elif specinv == 0:
            print('unload_ship -- nothing to unload')
            return 1

    while items == 1:
        docked.focus_inv_window()
        time.sleep(float(random.randint(0, 2000)) / 1000)
        keyboard.select_all()
        time.sleep(float(random.randint(0, 2000)) / 1000)
        drag_items_from_ship_inv()
        time.sleep(2)
        docked.look_for_spec_inv()
        items = docked.look_for_items()

    if specinv == 1:
        docked.open_spec_inv_ore()
        items = docked.look_for_items()

        while items == 1:
            docked.focus_inv_window()
            time.sleep(float(random.randint(0, 2000)) / 1000)
            keyboard.select_all()
            time.sleep(float(random.randint(0, 2000)) / 1000)
            drag_items_from_ship_inv()
            time.sleep(2)
            docked.look_for_items()
            print('unload_ship -- finished unloading procedure')
            return 1

    elif specinv == 0:
        print('unload_ship -- finished unloading procedure')
        return 1
