import sys
import traceback
import time
import ctypes

import pyautogui as pag

from lib import docked
from lib import load_ship
from lib import navigation as nav
from lib import unload_ship

atsite = 0
gotosite = 0
sys.setrecursionlimit(9999999)  # set high recursion limit for functions that
# call themselves.

conf = 0.95
alignment_time = 6  # Seconds (rounded up) current ship takes to begin a warp.

user32 = ctypes.windll.user32
screenx = user32.GetSystemMetrics(0)
screeny = user32.GetSystemMetrics(1)
halfscreenx = (int(screenx / 2))
halfscreeny = (int(screeny / 2))

window_resolutionx = 1024
window_resolutiony = 768

# get the coordinates of the eve client window and restrict image searching to
# within these boundaries.
# search for the eve neocom logo in top left corner of the eve client window.
# This will become the origin of the coordinate system.
origin = pag.locateCenterOnScreen('./img/origin.bmp', confidence=0.95,
                                  region=(0, 0, screenx, screeny))
(originx, originy) = origin
windowx = originx + window_resolutionx
windowy = originy + window_resolutiony


def navigator():
    # A standard warp-to-zero autopilot script. Warp to the destination, then
    # terminate.
    print('navigator -- running navigator')
    nav.route_set()
    dockedcheck = docked.docked_check()

    while dockedcheck == 0:
        nav.focus_overview()
        selectwaypoint = nav.warp_to_waypoint()
        while selectwaypoint == 1:  # Value of 1 indicates stargate waypoint.
            time.sleep(5)  # Wait for jump to begin.
            detectjump = nav.detect_jump()
            if detectjump == 1:
                nav.focus_overview()
                selectwaypoint = nav.warp_to_waypoint()
            else:
                nav.emergency_terminate()
                traceback.print_exc()
                traceback.print_stack()
                sys.exit('navigator -- error detecting jump')

        while selectwaypoint == 2:  # Value of 2 indicates a station waypoint.
            time.sleep(5)
            detectdock = nav.detect_dock()
            if detectdock == 1:
                print('navigator -- arrived at destination')
                return 1
        else:
            print('navigator -- likely at destination')
            return 1

    while dockedcheck == 1:
        docked.undock()
        time.sleep(5)
        navigator()


def collector():
    # Haul all items from a predetermined list of stations to a single 'home'
    # station, as specified by the user. The home station is identified by a
    # station bookmark beginning with '000', while the remote stations are any
    # station bookmark beginning with the numbers 1-9. This means up to 10
    # remote stations are supported.
    print('collector -- running collector')
    dockedcheck = docked.docked_check()
    while dockedcheck == 0:
        nav.focus_overview()
        selectwaypoint = nav.warp_to_waypoint()

        while selectwaypoint == 1:
            time.sleep(3)  # Wait for warp to start.
            detectjump = nav.detect_jump()
            if detectjump == 1:
                nav.focus_overview()
                selectwaypoint = nav.warp_to_waypoint()
        while selectwaypoint == 2:
            time.sleep(3)
            detectdock = nav.detect_dock()
            if detectdock == 1:
                collector()
        else:
            print(
                'collector -- error with at_dest_check_var and '
                'at_home_check_var')
            traceback.print_exc()
            traceback.print_stack()
            sys.exit()

    while dockedcheck == 1:
        athomecheck = nav.at_home_check()
        # If docked at home station, set a destination waypoint to a remote
        # station and unload cargo from ship into home station inventory.
        if athomecheck == 1:
            unload_ship.unload_ship()
            nav.set_dest()
            docked.undock()
            collector()
        elif athomecheck == 0:
            print('collector -- not at home')
            loadship = load_ship.load_ship_full()
            print('collector -- loadship is', loadship)

            if loadship == 2 or loadship == 0 or loadship is None:
                atdestnum = nav.at_dest_num()
                if atdestnum == -1:
                    docked.undock()
                    collector()
                else:
                    nav.set_dest()
                    nav.blacklist_station()
                    docked.undock()
                    collector()
            elif loadship == 1:  # Value of 1 indicates ship is full.
                nav.set_home()
                docked.undock()
                collector()

        else:
            print('collector -- error with at_home_check and at_dest_check')
            traceback.print_exc()
            traceback.print_stack()
            sys.exit()
    if dockedcheck is None:
        collector()


# Method for determining which script to run, as yet to be implemented by gui.
# selectscript = 2
#
# if selectscript == 1:
#	navigator()
# elif selectscript == 2:
#	nav.route_set()
#	collector()


'''
##### old original miner script #####
def miner():  # mine ore from a predetermined set of asteroid fields
	print('running miner')
	dockedcheck = docked.docked_check()
	while dockedcheck == 0:  # if not docked, check cargohold capacity
		cargohold = check_cargohold()
		if cargohold == 1:  # if cargohold over 90%, dock and unload at home 
		station, then rerun function
			nav.set_home()
		elif cargohold == 0:  # if cargohold less than 90%, go to first 
		asteroid field
			nav.set_dest()
			navigator()

	while dockedcheck == 1:  # if docked, check if at home station
		athomecheck = nav.at_home_check()
		if athomecheck == 1:  # if at home station, set destination waypoint 
		and unload ore from ship
			unload_ship.unload_ship()
			nav.set_dest()
			docked.undock()
			miner()
		elif athomecheck == 0:  # if not at home station, go to home station 
		to unload ore
			print('not at home')
			nav.set_home()
			docked.undock()
			miner()
		else:
			print('error with at_home_check and at_dest_check')
			traceback.print_exc()
			traceback.print_stack()
			sys.exit()
	if dockedcheck is None:
		miner()


if docked.docked_check == 1:
	print('good')
if docked.docked_check == 0:
	print('not docked')
    value = docked.docked_check()
    print(value)
    sys.exit()

'''