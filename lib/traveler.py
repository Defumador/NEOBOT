import sys, pyautogui, os, time, random, ctypes
from lib import mouse, keyboard, load_ship, unload_ship, while_docked, navigation

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 2.5  # set default wait time
sys.setrecursionlimit(100000)


# begin script by checking if docked
def traveler():
    while_docked.docked_check()
    if while_docked.docked_check_var == 1:  # if docked, check if at home station
        navigation.at_home_check()
        if navigation.at_home_check_var == 1:  # if at home station, set destination waypoint and unload cargo from ship
            navigation.return_to_dest()
            unload_ship.unload_ship()
            while_docked.undock()  # undock from station and follow waypoints
            traveler()
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
                        while_docked.undock()
                        traveler()
                    elif navigation.at_home_check_var == 1:  # if at home, set dest as waypoint and unload ship
                        navigation.return_to_dest()
                        unload_ship.unload_ship()
                        while_docked.undock()
                        traveler()  # after undocking, rerun script
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
                    while_docked.undock()
                    traveler()
                elif navigation.at_home_check_var == 1:  # if at home, set dest as waypoint and unload ship
                    navigation.return_to_dest()
                    unload_ship.unload_ship()
                    while_docked.undock()
                    traveler()  # after undocking, rerun script

traveler()