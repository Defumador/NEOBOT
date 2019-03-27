import sys
import traceback
import time
import win32

import pyautogui as pag

from lib import docked
from lib import load_ship
from lib import mining
from lib import navigation as nav
from lib import unload_ship

sys.setrecursionlimit(10000000)
pag.FAILSAFE = True

'''
if docked.docked_check == 1:
	print('good')
if docked.docked_check == 0:
	print('not docked')
value = docked.docked_check()
print(value)
sys.exit()
'''
def navigator():  # warp-to-zero autopilot, no fancy frills
	print('navigator -- running navigator')
	nav.route_set()
	dockedcheck = docked.docked_check()
	while dockedcheck == 0:  # if not docked, travel through waypoints
		nav.focus_overview()
		selectwaypoint = nav.warp_to_waypoint()
		while selectwaypoint == 1:  # 1 indicating stargate waypoint
			time.sleep(5)  # wait for warp to start
			detectjump = nav.detect_jump()
			if detectjump == 1:  # if jump detected, look for next waypoint and warp
				nav.focus_overview()
				selectwaypoint = nav.warp_to_waypoint()
			else:
				nav.emergency_terminate()
				traceback.print_exc()
				traceback.print_stack()
				sys.exit('navigator -- error detecting jump')
		while selectwaypoint == 2:  # 2 indicating station waypoint
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


def collector():  # haul cargo from a predetermined list of stations to a single 'home' station
	print('collector -- running collector')
	dockedcheck = docked.docked_check()
	while dockedcheck == 0:  # if not docked, travel through waypoints
		nav.focus_overview()
		selectwaypoint = nav.warp_to_waypoint()
		while selectwaypoint == 1:
			time.sleep(3)  # wait for warp to start
			detectjump = nav.detect_jump()
			if detectjump == 1:  # if jump detected, look for next waypoint and warp
				nav.focus_overview()
				selectwaypoint = nav.warp_to_waypoint()
		while selectwaypoint == 2:
			time.sleep(3)
			detectdock = nav.detect_dock()
			if detectdock == 1:  # if dock detected (2 means dock found), load ship (rerun 'while' loop)
				collector()
		else:
			print('collector -- error with at_dest_check_var and at_home_check_var')
			traceback.print_exc()
			traceback.print_stack()
			sys.exit()

	while dockedcheck == 1:  # if docked, check if at home station
		athomecheck = nav.at_home_check()
		if athomecheck == 1:  # if at home station, set destination waypoint and unload cargo from ship
			unload_ship.unload_ship()
			nav.set_dest()
			docked.undock()
			collector()
		elif athomecheck == 0:
			print('collector -- not at home')
			loadship = load_ship.load_ship()
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
			elif loadship == 1:  # if ship is full, return home to unload
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

'''
def miner():  # mine ore from a predetermined set of asteroid fields
	print('running miner')
	dockedcheck = docked.docked_check()
	while dockedcheck == 0:  # if not docked, check cargohold capacity
		cargohold = check_cargohold()
		if cargohold == 1:  # if cargohold over 90%, dock and unload at home station, then rerun function
			nav.set_home()
		elif cargohold == 0:  # if cargohold less than 90%, go to first asteroid field
			nav.set_dest()
			navigator()
					
	while dockedcheck == 1:  # if docked, check if at home station
		athomecheck = nav.at_home_check()
		if athomecheck == 1:  # if at home station, set destination waypoint and unload ore from ship
			unload_ship.unload_ship()
			nav.set_dest()
			docked.undock()
			miner()
		elif athomecheck == 0:  # if not at home station, go to home station to unload ore
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
'''


win32.findwindow()



#selectscript = 2
#
#if selectscript == 1:
#	navigator()
#elif selectscript == 2:
#	nav.route_set()
#	collector()
