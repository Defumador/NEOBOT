import sys
import traceback
import time

import pyautogui as pag

from lib import vars as v
from lib import docked
from lib import load_ship
from lib import mining
from lib import navigation as nav
from lib import unload_ship

sys.setrecursionlimit(9999999)

# TERMINOLOGY #######################

# A 'warning' is a persistent dialogue window that appears in the center of
# the screen and dims the rest of the screen. Warnings can only be dismissed
# with an explicit keystroke or button click from the user.

# A 'popup' is a partially transparent block of text that appears in the
# main play area for about five seconds.

#####################################

mining.target_asteroid()

def miner():
    while docked.docked_check() == 0:
        if mining.travel_to_bookmark() == 1:
            # Once arrived at site, check for hostile npcs and human players.
            # If either exist, warp to a different site.
            # If no hostiles npcs or players are present, check for asteroids.
            # If no asteroids, blacklist site and warp to next site.
            if mining.check_for_enemy_npcs() == 1:
                miner()
            # if check_for_players() == 1:
            #   break

            while mining.check_for_asteroids() == 1:
                mining.target_asteroid()
                mining.activate_mining_laser()
                # If ship inventory isn't full, continue to mine ore and wait
                # for popups or errors.
                while mining.inv_full_popup() == 0:
                    if mining.asteroid_depleted_popup() == 1:
                        if mining.check_for_asteroids() == 0:
                            nav.blacklist_bookmark(v.atsite)
                            miner()
                        elif mining.check_for_asteroids() == 1:
                            mining.target_asteroid()
                            mining.activate_mining_laser()
                            mining.inv_full_popup()
                            continue
                    if mining.check_for_enemy_npcs() == 1:
                        miner()
                    # check_for_players()
                    # if check_for_players() == 1:
                    # miner()
                    time.sleep(1)

                if mining.inv_full_popup() == 1:
                    # Once inventory is full, dock at home station and unload.
                    if nav.set_home() == 1:
                        if navigator() == 1:
                            unload_ship.unload_ship()
                            docked.undock()
                            time.sleep(3)
                            miner()

            if mining.check_for_asteroids() == 0:
                nav.blacklist_bookmark(v.atsite)
        elif mining.travel_to_bookmark() == 0:
            nav.emergency_terminate()
            sys.exit(0)
    if docked.docked_check() == 1:
        # If docked when script starts, undock.
        docked.undock()
        miner()


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


#miner()
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
