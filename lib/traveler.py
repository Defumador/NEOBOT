import sys
import traceback

import pyautogui

from lib import docked
from lib import navigation
from lib import load_ship
from lib import unload_ship

sys.setrecursionlimit(10000000)
pyautogui.FAILSAFE = True

'''
navigation.set_dest_dyn()
sys.exit()
'''


# begin script by checking if docked
def traveler():
    docked.docked_check()
    while docked.docked_check_var == 0:
        # if not docked, travel through waypoints
        navigation.select_waypoint()
        while navigation.select_waypoint_var == 1:
            # if found stargate waypoint (1 means stargate), warp and jump
            navigation.select_warp_button()
            navigation.detect_dock_or_jump()
            if navigation.detect_dock_or_jump_var == 1:
                # if jump detected, look for next waypoint and warp
                navigation.select_waypoint()
        if navigation.select_waypoint_var == 2:
            # if found station waypoint (2 means station), warp and dock
            navigation.select_warp_button()
            navigation.detect_dock_or_jump()
            if navigation.detect_dock_or_jump_var == 2:
                # if dock detected (2 means dock found), load ship
                docked.docked_check()
            else:
                print('error with at_dest_check_var and at_home_check_var')
                traceback.print_exc()
                traceback.print_stack()
                sys.exit()

    while docked.docked_check_var == 1:
        # if docked, check if at home station
        navigation.at_home_check()
        if navigation.at_home_check_var == 1:
            # if at home station, set destination waypoint and unload cargo from ship
            unload_ship.unload_ship()
            navigation.set_dest_dyn()
            docked.undock()
            traveler()
        elif navigation.at_home_check_var == 0:
            load_ship.load_ship()
            if load_ship.load_ship_var == 2:
                # if ship has loaded station, move to next station
                navigation.set_dest_dyn()
                navigation.blacklist_station()
                docked.undock()
                traveler()
            elif load_ship.load_ship_var == 1:
                # if ship is full, return home to unload
                navigation.set_home()
                docked.undock()
                traveler()
        else:
            print('error with at_home_check and at_dest_check')
            traceback.print_exc()
            traceback.print_stack()
            sys.exit()


traveler()
