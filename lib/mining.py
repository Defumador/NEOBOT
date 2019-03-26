import time
import sys

import pyautogui as pag

from lib import navigation as nav
from lib import docked
from lib import unload_ship
from lib import main

sys.setrecursionlimit(9999999)

user32 = ctypes.windll.user32
screenwidth = user32.GetSystemMetrics(0)
screenheight = user32.GetSystemMetrics(1)
halfscreenwidth = (int(screenwidth / 2))
halfscreenheight = (int(screenheight / 2))

mining_lasers = 1

check_for_enemy_frigates = 1
check_for_enemy_destroyers = 1
check_for_enemy_cruisers = 1
check_for_enemy_battlecruisers = 1
check_for_enemy_battleships = 1

check_for_player_neutrals
check_for_player_suspects
check_for_player_war_targets
check_for_player_reds
check_for_player_yellows
check_for_player_greys

global atsite
atsite = 0

def miner():
	nav.docked_check()
	while nav.docked_check() == 0:
		travel_to_site()
		if travel_to_site() == 1:
			# once arrived at site, check for hostile npcs and players. if either exist, warp to next site
			# if no hostiles npcs or players, check for ore. if no ore, blacklist site and warp to next site
			check_for_hostiles()
			if check_for_hostiles() == 1:
				break
			check_for_players()
			if check_for_players() == 1:
				break
			check_for_ore()
			while check_for_ore() == 1:
				target_ore()
				activate_mining_laser()
				# if cargo isn't full, continue to mine ore and wait for popups or errors
				check_hold_popup()
				while check_hold_popup() == 0:
					check_asteroid_depleted_popup()
					if check_asteroid_depleted_popup() == 1:
						check_for_ore()
						if check_for_ore() == 0:
							nav.blacklist(site)
						elif check_for_ore() == 1:
							target_ore()
							activate_mining_laser()
							check_hold_popup()
							continue
					check_for_hostiles()
					if check_for_hostiles() == 1:
						miner()
					check_for_players()
					if check_for_players() == 1:
						miner()
					time.sleep(1)
					check_hold_popup()
				if check_hold_popup() == 1:
					# once cargo is full, dock at home station and unload
					nav.go_home()
					unload_cargo.unload_cargo()
					docked.undock()
					time.sleep(3)		
			if check_for_ore() == 0:
				nav.blacklist(site)
	if nav.docked_check() == 1:
		# if docked when script starts, undock
		docked.undock()
		miner()

def travel_to_site():
	# find a suitable asteroid field by warping to each bookmark in numerical order
	global gotosite
	gotosite = 1
	# try warping to bookmark 1 in system. if bookmark 1 not present or already there, increment bookmark number by 1 and look again
	nav.warp_to_defined_bookmark_in_system(gotosite)
	while nav.warp_to_defined_bookmark_in_system(gotosite) == 0 and gotosite <= 10:
		gotosite += 1
		nav.warp_to_defined_bookmark_in_system(gotosite)
	if nav.warp_to_defined_bookmark_in_system(gotosite) == 1 and gotosite <= 10:
		# save site number as a separate variable so script remembers not to try to warp there
		atsite = gotosite
		# wait for warp to complete
		nav.detect_warp()
		if nav.detect_warp() == 1:
			return 1
	else:
		print('travel_to_site error, ran out of sites to check for')
		nav.emergency_terminate()

def check_for_enemy_ships():
	# check entire screen for red ship hud icons, indicating hostile npcs
	# only avoid the hostile ship classes specified by the player
	# script will look for these icons on the default 'general' overview tab
	# script will keep the 'general' overview tab visible by default until finding another asteroid is needed
	if check_for_enemy_frigates == 1:
		enemy_frigate = pag.locateCenterOnScreen('./img/enemy_frigate.bmp', confidence=0.90,
												region=(0, 0, screenwidth, screenheight))
		if enemy_frigate is not None:
			return 1
	if check_for_enemy_destroyers == 1:
		enemy_destroyer = pag.locateCenterOnScreen('./img/enemy_destroyer.bmp', confidence=0.90,
													region=(0, 0, screenwidth, screenheight))
		if enemy_destroyer is not None:
			return 1
	if check_for_enemy_cruisers == 1:
		enemy_cruiser = pag.locateCenterOnScreen('./img/enemy_cruiser.bmp', confidence=0.90,
												region=(0, 0, screenwidth, screenheight))
		if enemy_cruiser is not None:
			return 1
	if check_for_enemy_battlecruisers == 1:
		enemy_battlecruiser = pag.locateCenterOnScreen('./img/enemy_battlecruiser.bmp', confidence=0.90,
														region=(0, 0, screenwidth, screenheight))
		if enemy_battlecruiser is not None:
			return 1
	if check_for_enemy_battleships == 1:
		enemy_battleship = pag.locateCenterOnScreen('./img/enemy_battleship.bmp', confidence=0.90,
													region=(0, 0, screenwidth, screenheight))
		if enemy_battleship is not None:
			return 1
	else:
		print('check_for_enemy_ships no hostile npcs to avoid')
		return 0

def check_for_players():
	# check screen for other ship icons


def check_for_ore():
	# switch overview to 'mining' tab, check for asteroids, then switch back to 'general' tab
	mining_overview_tab =
	general_overview_tab =
	asteroid_small = pag.locateCenterOnScreen('./img/asteroid_s.bmp', confidence=0.90,
												region=(0, 0, screenwidth, screenheight))
	asteroid_medium = pag.locateCenterOnScreen('./img/asteroid_m.bmp', confidence=0.90,
												region=(0, 0, screenwidth, screenheight))
	asteroid_large = pag.locateCenterOnScreen('./img/asteroid_l.bmp', confidence=0.90,
												region=(0, 0, screenwidth, screenheight))
	if asteroid_small is None and asteroid_medium is None and asteroid_large is None:
		print('check_for_ore no more asteroids found in field')
		return 0
	elif asteroid_small is not None or asteroid_medium is not None or asteroid_large is not None:
		return 1


#def target_ore()
	# target closest ore in overview
	# switch to mining tab, target asteroid, then switch back to general tab

def check_hold_popup():
	# check for popup indicating cargo hold is full
	# 'cargo hold full' popup lasts about 5 seconds, so check for this popup once every 3 seconds
	cargo_hold_full = pag.locateCenterOnScreen('./img/cargo_hold_full.bmp', confidence=0.90,
												region=(0, 0, screenwidth, screenheight))
												region = (0, 0, screenwidth, screenheight))
	if cargo_hold_full is None
		return 0
	elif cargo_hold_full is not None
		print('cargo_hold_popup found popup')
		return 1
		
def check_asteroid_depleted_popup():
	# check for popup indicating asteroid has been depleted
	asteroid_depleted = pag.locateCenterOnScreen('./img/asteroid_depleted.bmp', confidence=0.90,
												region=(0, 0, screenwidth, screenheight))
												region = (0, 0, screenwidth, screenheight))
	if asteroid_depleted is None
		return 0
	elif asteroid_depleted is not None
		print('asteroid_depleted_popup found popup')
		return 1
	

def activate_mining_laser():  # turn on mining lasers to mine ore
	if mining_lasers == 1:
		keyboard.keydown('F1')
	if mining_lasers == 2:
		keyboard.keydown('F1')
		keyboard.keydown('F2')
	if mining_lasers == 3:
		keyboard.keydown('F1')
		keyboard.keydown('F2')
		keyboard.keydown('F3')
	if mining_lasers == 4:
		keyboard.keydown('F1')
		keyboard.keydown('F2')
		keyboard.keydown('F3')
		keyboard.keydown('F4')
	print('activate_mining_laser activated lasers')
	return 1
		
	
	
	
