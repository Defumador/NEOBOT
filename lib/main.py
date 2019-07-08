import sys
import time
import traceback

import lib.bookmarks
import lib.drones
import lib.navigation
import lib.overview
from lib import docked, load_ship, navigation as nav, unload_ship, mining
from lib.vars import system_mining, originx, originy, windowx, windowy

sys.setrecursionlimit(9999999)
playerfound = 0

# TERMINOLOGY #################################################################

# A 'warning' is a persistent dialogue window that appears in the center of
# the screen and dims the rest of the screen. Warnings can only be dismissed
# with an explicit keystroke or button click from the user.

# A 'popup' is a partially transparent block of text that appears in the
# main play area for about five seconds.

# A function with the word 'loop' in its name will not return until a certain
# condition has been met or it times out.

###############################################################################

# These variables are for the mining script only ------------------------------
# Script begins at location 0, assumed to be your home station.
site = 7
# Total number of saved bookmark locations. This variable is set by the user.
total_sites = 10
# Number of 'runs' completed for mining script
runs = 0
# -----------------------------------------------------------------------------


def miner():
    global playerfound
    global site
    global runs
    runs += 1
    timer_var = 0
    print('beginning run', runs)
    while docked.docked_check() == 0:
        if lib.drones.detect_drones_launched() == 1:
            lib.overview.focus_client()
            lib.drones.recall_drones_loop()
        # Increment desired mining site by one as this is the next location
        # ship will warp to.
        site += 1
        # If there aren't any more sites left, loop back around to site 1.
        if site > total_sites:
            site = 1
        if lib.bookmarks.travel_to_bookmark(site) == 1:
            # Once arrived at site, check for hostile npcs and human players.
            # If either exist, warp to the next site.
            # If no hostiles npcs or players are present, check for asteroids.
            # If no asteroids, blacklist site and warp to next site.
            if lib.overview.detect_npcs_var == 1:
                if lib.overview.focus_overview_tab('general') == 1:
                    if lib.overview.detect_npcs() == 1:
                        miner()
            if lib.overview.detect_pcs_var == 1:
                if lib.overview.detect_pcs() == 1:
                    playerfound += 1
                    miner()

            lib.overview.focus_overview_tab('mining')
            while mining.detect_ore() == 1:
                lib.drones.launch_drones_loop()
                if mining.target_ore() == 0:
                    miner()
                mining.activate_miner()
                # If ship inventory isn't full, continue to mine ore and wait
                # for popups or errors.
                # Switch back to the general tab for easier ship detection
                lib.overview.focus_overview_tab('general')
                while mining.inv_full_popup() == 0:
                    if mining.asteroid_depleted_popup() == 1:
                        if mining.detect_ore() == 0:
                            #nav.blacklist_local_bookmark()
                            miner()
                        elif mining.detect_ore() == 1:
                            if mining.target_ore() == 0:
                                miner()
                            mining.activate_miner()
                            mining.inv_full_popup()
                            print('finishing run', runs)
                            continue
                    if lib.overview.detect_npcs() == 1:
                        lib.drones.recall_drones_loop()
                        miner()
                    if lib.overview.detect_pcs() == 1:
                        lib.drones.recall_drones_loop()
                        miner()
                    timer_var += 1
                    if mining.timer(timer_var) == 1:
                        lib.drones.recall_drones_loop()
                        miner()
                    time.sleep(2)

                if mining.inv_full_popup() == 1:
                    # Once inventory is full, dock at home station and unload.
                    lib.drones.recall_drones_loop()
                    print('finishing run', runs)
                    if system_mining == 0:
                        if lib.bookmarks.set_home() == 1:
                            if navigator() == 1:
                                unload_ship.unload_ship()
                                docked.undock_loop()
                                playerfound = 0
                                time.sleep(3)
                                miner()
                    # If ship is mining in the same system it will dock in,
                    # a different set of functions is required.
                    elif system_mining == 1:
                        lib.bookmarks.dock_at_local_bookmark()
                        unload_ship.unload_ship()
                        docked.undock_loop()
                        playerfound = 0
                        time.sleep(3)
                        miner()

                if mining.detect_ore() == 0:
                    lib.bookmarks.blacklist_local_bookmark()
        elif lib.bookmarks.travel_to_bookmark(site) == 0:
            nav.emergency_terminate()
            sys.exit(0)
    if docked.docked_check() == 1:
        # If docked when script starts, undock_loop.
        lib.overview.focus_client()
        docked.undock_loop()
        miner()



def navigator():
    # A standard warp-to-zero autopilot script. Warp to the destination, then
    # terminate.
    print('navigator -- running navigator')
    nav.detect_route()
    dockedcheck = docked.docked_check()

    while dockedcheck == 0:
        lib.overview.focus_client()
        selectwaypoint = nav.warp_to_waypoint()
        while selectwaypoint == 1:  # Value of 1 indicates stargate waypoint.
            time.sleep(5)  # Wait for jump to begin.
            detectjump = nav.detect_jump_loop()
            if detectjump == 1:
                lib.overview.focus_client()
                selectwaypoint = nav.warp_to_waypoint()
            else:
                nav.emergency_terminate()
                traceback.print_exc()
                traceback.print_stack()
                sys.exit('navigator -- error detecting jump')

        while selectwaypoint == 2:  # Value of 2 indicates a station waypoint.
            time.sleep(5)
            detectdock = nav.detect_dock_loop()
            if detectdock == 1:
                print('navigator -- arrived at destination')
                return 1
        else:
            print('navigator -- likely at destination')
            return 1

    while dockedcheck == 1:
        docked.undock_loop()
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
        lib.overview.focus_client()
        selectwaypoint = nav.warp_to_waypoint()

        while selectwaypoint == 1:
            time.sleep(3)  # Wait for warp to start.
            detectjump = nav.detect_jump_loop()
            if detectjump == 1:
                lib.overview.focus_client()
                selectwaypoint = nav.warp_to_waypoint()
        while selectwaypoint == 2:
            time.sleep(3)
            detectdock = nav.detect_dock_loop()
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
        athomecheck = lib.bookmarks.detect_at_home()
        # If docked at home station, set a destination waypoint to a remote
        # station and unload cargo from ship into home station inventory.
        if athomecheck == 1:
            unload_ship.unload_ship()
            lib.bookmarks.set_dest()
            docked.undock_loop()
            collector()
        elif athomecheck == 0:
            print('collector -- not at home')
            loadship = load_ship.load_ship_full()
            print('collector -- loadship is', loadship)

            if loadship == 2 or loadship == 0 or loadship is None:
                atdestnum = lib.bookmarks.detect_bookmark_location()
                if atdestnum == -1:
                    docked.undock_loop()
                    collector()
                else:
                    lib.bookmarks.set_dest()
                    lib.bookmarks.blacklist_station()
                    docked.undock_loop()
                    collector()
            elif loadship == 1:  # Value of 1 indicates ship is full.
                lib.bookmarks.set_home()
                docked.undock_loop()
                collector()

        else:
            print('collector -- error with detect_at_home and at_dest_check')
            traceback.print_exc()
            traceback.print_stack()
            sys.exit()
    if dockedcheck is None:
        collector()


print("originx =", originx)
print("originy =", originy)
print("windowx =", windowx)
print("windowy =", windowy)

miner()
# lib.overview.focus_overview_tab('warpto')
# nav.emergency_terminate()
#mining.detect_ore()
#mining.target_ore()
#mining.activate_miner()
# lib.overview.detect_pcs()
#mining.detect_asteroids()
#mining.target_asteroid()
#mining.focus_mining_tab()
#mining.check_for_enemies()
#time.sleep(2)
#lib.overview.focus_client()
#mining.recall_drones_loop()
#mining.launch_drones_loop()
#cProfile.run('mining.detect_pcs()')
# Method for determining which script to run, as yet to be implemented by gui.
# selectscript = 2
#
# if selectscript == 1:
#	navigator()
# elif selectscript == 2:
#	nav.detect_route()
#	collector()
'''
# unit tests
while mining.inv_full_popup() == 0:
    if mining.asteroid_depleted_popup() == 1:
        if mining.detect_asteroids() == 0:
            # nav.blacklist_local_bookmark()
            miner()
        elif mining.detect_asteroids() == 1:
            mining.target_asteroid()
            mining.activate_miner()
            mining.inv_full_popup()
            continue
    if threading.Thread(target=mining.detect_pcs()).start() == 1:
        mining.recall_drones_loop()
        miner()
    if threading.Thread(target=mining.detect_pcs()).start() == 1:
        mining.recall_drones_loop()
        miner()
    time.sleep(2)
'''

'''
sample threading implementation

import threading
import time

stop = 0
lock = threading.Lock()

def shield_check():
    global stop
    for i in range(1, 15):
        time.sleep(1)
        print('shield_check', i)
        if stop == 1:
            print('shield check stopping!')
            break
        elif i >= 4:
            print('shield check warping out!')
            stop = 1
            warpout()

def npc_check():
    global stop
    for i in range(1, 21):
        time.sleep(2)
        print('npc_check', i)
        if stop == 1:
            print('npc_check stopping!')
            break
        elif i >= 2:
            print('npc_check warping out!')
            stop = 1
            warpout()

def warpout():
    lock.acquire()
    for i in range(1, 5):
        time.sleep(3)
        print('warping out!', i)
    lock.release()
'''
