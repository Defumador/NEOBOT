import sys, pyautogui, os, time, random, ctypes
from lib import mouse, keyboard, load_ship, unload_ship, while_docked, navigation

sys.setrecursionlimit(100000)
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1



# begin script by checking if docked
def traveler():
    while_docked.docked_check()
    while while_docked.docked_check_var == 1:  # if docked, check if at home station
        navigation.at_home_check()
        if navigation.at_home_check_var == 1:  # if at home station, set destination waypoint and unload cargo from ship
            navigation.return_to_dest()
            unload_ship.unload_ship()
            while_docked.undock()  # undock from station and rerun 'while' loop
            while_docked.docked_check()
        elif navigation.at_dest_check_var == 1:  # if at destination, set home as waypoint and load ship
            navigation.return_home()
            load_ship.load_ship()
            while_docked.undock()
            while_docked.docked_check()  # undock from station and rerun 'while' loop
        else:
            print('error with at_home_check and at_dest_check')
            sys.exc_traceback
            sys.exc_info()
    while while_docked.docked_check_var == 0:  # if not docked, travel through waypoints
        navigation.select_waypoint()
        while navigation.select_waypoint_var == 1:  # if found stargate waypoint (1 means stargate), warp and jump
            navigation.select_warp_button()
            navigation.detect_dock_or_jump()
            if navigation.detect_dock_or_jump_var == 1:  # if jump detected, look for next waypoint and warp
                navigation.select_waypoint()
        if navigation.select_waypoint_var == 2:  # if found station waypoint (2 means station), warp and dock
            navigation.select_warp_button()
            navigation.detect_dock_or_jump()
            if navigation.detect_dock_or_jump_var == 2:  # if dock detected (2 means dock found), load ship
                navigation.at_dest_check()
                navigation.at_home_check()
                if navigation.at_dest_check_var == 1\
                        and navigation.at_home_check_var == 0:  # if at destination, set home as waypoint and load ship
                    navigation.return_home()
                    load_ship.load_ship()
                    if load_ship.load_ship_var == 0:
                        print('no items present')
                        sys.exit()
                    while_docked.undock()
                    while_docked.docked_check()
                elif navigation.at_home_check_var == 1\
                        and navigation.at_dest_check_var == 0:  # if at home, set dest as waypoint and unload ship
                    navigation.return_to_dest()
                    unload_ship.unload_ship()
                    while_docked.undock()
                    while_docked.docked_check()
                else:
                    print('error with at_dest_check_var and at_home_check_var')
                    sys.exit()


'''                             
                    traveler()  # after undocking, rerun script
                if navigation.detect_dock_or_jump_var == 1:
                    print('detected jump while waiting for dock')
                    sys.exit()
        elif navigation.at_home_check_var == 0:
            while_docked.undock()
            traveler()
    elif while_docked.docked_check_var == 0:
        navigation.select_waypoint()
        while navigation.select_waypoint_var == 1:  # if found stargate waypoint, warp and jump
            navigation.select_warp_button()
            navigation.detect_dock_or_jump()
            if navigation.detect_dock_or_jump_var == 1:  # if jump detected, look for next waypoint and warp
                navigation.select_waypoint()
        if navigation.select_waypoint_var == 2:  # if found station waypoint, warp and dock
            navigation.select_warp_button()
            navigation.detect_dock_or_jump()
            if navigation.detect_dock_or_jump_var == 2:  # if dock detected, load ship
                navigation.at_dest_check()
                navigation.at_home_check()
                if navigation.at_dest_check_var == 1:  # if at destination, set home as waypoint and load ship
                    navigation.return_home()
                    load_ship.load_ship()
                    if load_ship.load_ship_var == 0:
                        print('no items present')
                        sys.exit()
                    while_docked.undock()
                    traveler()
                elif navigation.at_home_check_var == 1:  # if at home, set dest as waypoint and unload ship
                    navigation.return_to_dest()
                    unload_ship.unload_ship()
                    while_docked.undock()
                    traveler()  # after undocking, rerun script
'''
traveler()