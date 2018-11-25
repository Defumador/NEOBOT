import sys
import traceback
import time

import pyautogui

from lib import docked
from lib import navigation
from lib import load_ship
from lib import unload_ship

sys.setrecursionlimit(10000000)
pyautogui.FAILSAFE = True

'''
if docked.docked_check == 1:
    print('good')
if docked.docked_check == 0:
    print('not docked')
value = docked.docked_check()
print(value)
sys.exit()
'''


def wtz_autopilot():  # warp-to-zero autopilot, no fancy loading/unloading behaviors
    dockedcheck = docked.docked_check()
    while dockedcheck == 0:  # if not docked, travel through waypoints
        selectwaypoint = navigation.select_waypoint_warp_hotkey()
        while selectwaypoint == 1:  # 1 indicating stargate waypoint
            time.sleep(5)  # wait for warp to start
            detectjump = navigation.detect_jump()
            if detectjump == 1:  # if jump detected, look for next waypoint and warp
                selectwaypoint = navigation.select_waypoint_warp_hotkey()
            else:
                traceback.print_exc()
                traceback.print_stack()
                sys.exit('error detecting jump')
        while selectwaypoint == 2:  # 2 indicating station waypoint
            time.sleep(5)
            detectdock = navigation.detect_dock()
            if detectdock == 1:
                print('arrived at destination')
                sys.exit()
        else:
            traceback.print_exc()
            traceback.print_stack()
            sys.exit('error with selectwaypoint')
    while dockedcheck == 1:
        docked.undock()
        time.sleep(5)
        dockedcheck = docked.docked_check()


def traveler():  # begin script by checking if docked
    dockedcheck = docked.docked_check()
    while dockedcheck == 0:  # if not docked, travel through waypoints
        selectwaypoint = navigation.select_waypoint_warp_hotkey()
        while selectwaypoint == 1:
            time.sleep(5)  # wait for warp to start
            detectjump = navigation.detect_jump()
            if detectjump == 1:  # if jump detected, look for next waypoint and warp
                selectwaypoint = navigation.select_waypoint_warp_hotkey()
        while selectwaypoint == 2:
            time.sleep(5)
            detectdock = navigation.detect_dock()
            if detectdock == 1:  # if dock detected (2 means dock found), load ship (rerun 'while' loop)
                selectwaypoint = navigation.select_waypoint_warp_hotkey()
        else:
            print('error with at_dest_check_var and at_home_check_var')
            traceback.print_exc()
            traceback.print_stack()
            sys.exit()

    while dockedcheck == 1:  # if docked, check if at home station
        athomecheck = navigation.at_home_check()
        if athomecheck == 1:  # if at home station, set destination waypoint and unload cargo from ship
            unload_ship.unload_ship()
            navigation.set_dest()
            docked.undock()
            traveler()
        elif athomecheck == 0:
            print('not at home')
            loadship = load_ship.load_ship()
            print('loadship is', loadship)
            if loadship == 2 or loadship == 0 or loadship is None:
                atdestnum = navigation.at_dest_num()
                if atdestnum == -1:
                    docked.undock()
                    traveler()
                else:
                    navigation.set_dest()
                    navigation.blacklist_station()
                    docked.undock()
                    traveler()
            elif loadship == 1:  # if ship is full, return home to unload
                navigation.set_home()
                docked.undock()
                traveler()
        else:
            print('error with at_home_check and at_dest_check')
            traceback.print_exc()
            traceback.print_stack()
            sys.exit()


selectscript = 1

if selectscript == 1:
    wtz_autopilot()
elif selectscript == 2:
    traveler()














