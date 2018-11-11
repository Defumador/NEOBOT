import os, time, random, sys
import pyautogui
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 2.5  # set default wait time
from lib import in_space, while_docked, keyboard
os.chdir('C:\\Program Files (x86)\\Python37-32\Lib\\site-packages\\')  # change directory in order
                                                                        # to locate pyautogui module
os.chdir('D:\OneDrive\Documents\Scripts\Python\PY-NEOBOT-GitHub\lib')
sys.setrecursionlimit(100000)
while_docked.docked_check()



"""
def traveler():
    # first check if ship is docked
    while_docked.docked_check()
    # if docked, undock
    if while_docked.docked_check() == 1:
        while_docked.undock()
    # if not docked, look for waypoint
    else:
        in_space.select_waypoint()
        # if waypoint found, warp
        if in_space.select_waypoint() == 1:
            in_space.select_warp_button()
            # after clicking warp button, check if ship has docked or jumped
            in_space.detect_dock_or_jump()
            # if jump detected, restart function
            if in_space.detect_dock_or_jump() == 'jumped':
                traveler()
            # if dock detected, check if at destination or home station
            if in_space.detect_dock_or_jump() == 'docked':
                # if at home, unload cargo and return to destination
                while_docked.at_home_check()
                while_docked.at_dest_check()
                if while_docked.at_home_check() == 1:
                    while_docked.focus_inventory_window()
                    while_docked.unload_ship()
                    while_docked.return_to_dest()
                # if at destination, load cargo from staion inventory into ship
                elif while_docked.at_dest_check() == 1:
                    while_docked.open_station_hangar()
                    while_docked.focus_inventory_window()
                    while_docked.look_for_special_hold()
                    # if ship has special hold, try loading station inventory into it
                    if while_docked.look_for_special_hold() == 1:
                        while_docked.drag_items_to_special_hold()
                        # if both special and standard cargo bays are full, return home
                        if while_docked.drag_items_to_cargo_bay() == 1:
                            while_docked.return_home()
                            while_docked.undock()
                            traveler()

traveler()
"""