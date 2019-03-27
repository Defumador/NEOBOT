import time
import sys
import ctypes

import pyautogui as pag

from lib import navigation as nav
from lib import docked
from lib import unload_ship
from lib import keyboard
from lib import mouse

sys.setrecursionlimit(9999999)

user32 = ctypes.windll.user32
screenwidth = user32.GetSystemMetrics(0)
screenheight = user32.GetSystemMetrics(1)
halfscreenwidth = (int(screenwidth / 2))
halfscreenheight = (int(screenheight / 2))

window_resolutionx = 1024
window_resolutiony = 768

# get coordinates of EVE client window and restrict image searching to within these boundaries
# search for EVE logo in top left of client window, this will be the origin of the coordinate system
origin = pag.locateCenterOnScreen('./img/origin.bmp', confidence=0.95, region=(0, 0, screenwidth, screenheight))
(originx, originy) = origin
windowx = originx + window_resolutionx
windowy = originy + window_resolutiony

mining_lasers = 1

check_for_enemy_frigates = 1
check_for_enemy_destroyers = 1
check_for_enemy_cruisers = 1
check_for_enemy_battlecruisers = 1
check_for_enemy_battleships = 1

#check_for_player_neutrals = 1
#check_for_player_suspects = 1
#check_for_player_war_targets = 1
#check_for_player_criminals = 1
#check_for_player_yellows = 1
#check_for_player_greys = 1

atsite = 0
gotosite = 0


def miner():
	while docked.docked_check() == 0:
		if travel_to_site() == 1:
			# once arrived at site, check for hostile npcs and players. if either exist, warp to next site
			# if no hostiles npcs or players, check for ore. if no ore, blacklist site and warp to next site
			if check_for_hostiles() == 1:
				break
			#if check_for_players() == 1:
			#	break
			while check_for_ore() == 1:
				target_ore()
				activate_mining_laser()
				# if cargo isn't full, continue to mine ore and wait for popups or errors
				while check_hold_popup() == 0:
					if check_asteroid_depleted_popup() == 1:
						if check_for_ore() == 0:
							nav.blacklist_site(atsite)
							miner()
						elif check_for_ore() == 1:
							target_ore()
							activate_mining_laser()
							check_hold_popup()
							continue
					if check_for_hostiles() == 1:
						miner()
					#check_for_players()
					#if check_for_players() == 1:
						#miner()
					time.sleep(1)
				if check_hold_popup() == 1:
					# once cargo is full, dock at home station and unload
					nav.go_home()
					unload_ship.unload_ship()
					docked.undock()
					time.sleep(3)
					miner()
			if check_for_ore() == 0:
				nav.blacklist_site(atsite)
		elif travel_to_site() == 0:
			nav.emergency_terminate()
			sys.exit(0)
	if docked.docked_check() == 1:
		# if docked when script starts, undock
		docked.undock()
		miner()


def travel_to_site():
	# find a suitable asteroid field by warping to each bookmark in numerical order
	global gotosite
	global atsite
	gotosite = 1
	# try warping to bookmark 1 in system. if bookmark 1 not present or already there, increment bookmark number by 1 and look again
	while nav.warp_to_defined_bookmark_in_system(gotosite) == 0 and gotosite <= 10:
		gotosite += 1
		continue
	if nav.warp_to_defined_bookmark_in_system(gotosite) == 1 and gotosite <= 10:
		# once a valid site is found, remember the site number the ship is warping to so script doesn't try warping there again
		atsite = gotosite
		# wait for warp to complete
		if nav.detect_warp() == 1:
			return 1
	else:
		print('travel_to_site -- ran out of sites to check for')
		return 0


def check_for_hostiles():
	# check entire screen for red ship hud icons, indicating hostile npcs
	# only avoid the hostile ship classes specified by the player
	# script will look for these icons on the default 'general' overview tab
	# script will keep the 'general' overview tab visible by default until finding another asteroid is needed
	print('check_for_hostiles called')
	if check_for_enemy_frigates == 1:
		enemy_frigate = pag.locateCenterOnScreen('./img/enemy_frigate.bmp', confidence=0.80,
												region=(0, 0, screenwidth, screenheight))
		if enemy_frigate is not None:
			print('check_for_hostiles -- found hostile frigate')
			return 1
	#elif check_for_enemy_destroyers == 1:
	#	enemy_destroyer = pag.locateCenterOnScreen('./img/enemy_destroyer.bmp', confidence=0.90,
	#												region=(0, 0, screenwidth, screenheight))
	#	if enemy_destroyer is not None:
	#		return 1
	#elif check_for_enemy_cruisers == 1:
	#	enemy_cruiser = pag.locateCenterOnScreen('./img/enemy_cruiser.bmp', confidence=0.90,
	#											region=(0, 0, screenwidth, screenheight))
	#	if enemy_cruiser is not None:
	#		return 1
	#elif check_for_enemy_battlecruisers == 1:
	#	enemy_battlecruiser = pag.locateCenterOnScreen('./img/enemy_battlecruiser.bmp', confidence=0.90,
	#													region=(0, 0, screenwidth, screenheight))
	#	if enemy_battlecruiser is not None:
	#		return 1
	#elif check_for_enemy_battleships == 1:
	#	enemy_battleship = pag.locateCenterOnScreen('./img/enemy_battleship.bmp', confidence=0.90,
	#												region=(0, 0, screenwidth, screenheight))
	#	if enemy_battleship is not None:
	#		return 1
	else:
		print('check_for_enemy_ships -- no hostile npcs to avoid')
		return 0


def check_for_players():
	# check screen for other ship icons
	#if check_for_player_war_targets == 1:
	#	player_war_target = pag.locateCenterOnScreen('./img/player_war_target.bmp', confidence=0.80,
	#											region=(0, 0, screenwidth, screenheight))
	#	if player_war_target is not None:
	#		print('check_for_players -- found war target')
	#		return 1
	#elif check_for_player_suspects == 1:
	#	player_war_target = pag.locateCenterOnScreen('./img/player_war_target.bmp', confidence=0.80,
	#											region=(0, 0, screenwidth, screenheight))
	#	if player_war_target is not None:
	#		print('check_for_players -- found war target')
	#		return 1
	#
	#elif check_for_player_criminals == 1:
	#	player_criminal = pag.locateCenterOnScreen('./img/player_criminal.bmp', confidence=0.80,
	#											region=(0, 0, screenwidth, screenheight))
	#	if player_criminal is not None:
	#		print('check_for_players -- found criminal')
	#		return 1
	#
	#elif check_for_player_neutrals == 1:
	#	player_neutral = pag.locateCenterOnScreen('./img/player_neutral.bmp', confidence=0.80,
	#											region=(0, 0, screenwidth, screenheight))
	#	if player_neutral is not None:
	#		print('check_for_players -- found neutral')
	#		return 1
	#
	#elif check_for_player_war_targets == 1:
	#	player_war_target = pag.locateCenterOnScreen('./img/player_war_target.bmp', confidence=0.80,
	#											region=(0, 0, screenwidth, screenheight))
	#	if player_war_target is not None:
	#		print('check_for_players -- found war target')
	#		return 1
	return 0


def check_for_ore():
	# switch overview to 'mining' tab, check for asteroids, then switch back to 'general' tab
	# prioritize larger asteroids
	#mining_overview_tab = pag.locateCenterOnScreen('./img/mining_overview_tab.bmp', confidence=0.90,
												#region=(0, 0, screenwidth, screenheight))
	#general_overview_tab = pag.locateCenterOnScreen('./img/general_overview_tab.bmp', confidence=0.90,
												#region=(0, 0, screenwidth, screenheight))
	global asteroid_small
	global asteroid_medium
	global asteroid_large
	asteroid_large = pag.locateCenterOnScreen('./img/asteroid_l.bmp', confidence=0.80,
												region=(0, 0, screenwidth, screenheight))
	if asteroid_large is not None:
		return 1
	asteroid_medium = pag.locateCenterOnScreen('./img/asteroid_m.bmp', confidence=0.80,
												region=(0, 0, screenwidth, screenheight))
	elif asteroid_medium is not None:
		return 1
	asteroid_small = pag.locateCenterOnScreen('./img/asteroid_s.bmp', confidence=0.80,
												region=(originx, originy, windowx, windowy))
	elif asteroid_small is not None:
		return 1
	else:
		print('check_for_ore -- no more asteroids found at site')
		return 0


def target_ore():
	# target closest large-sized asteroid in overview, assuming overview is sorted by distance with closest first
	# switch to mining tab, target asteroid, then switch back to general tab
	global asteroid_small
	global asteroid_medium
	global asteroid_large
	if asteroid_large is not None:
		(asteroid_largex, asteroid_largey) = asteroid_large
		pag.moveTo((asteroid_largex + (random.randint(-2, 200))),
		  		 (asteroid_largey + (random.randint(-3, 3))),
		  		 mouse.move_time(), mouse.mouse_path())
		mouse.click()
		keyboard.keypress('ctrl')
		return 1
	elif asteroid_medium is not None:
		(asteroid_mediumx, asteroid_mediumy) = asteroid_medium
		pag.moveTo((asteroid_mediumx + (random.randint(-2, 200))),
		  		 (asteroid_mediumy + (random.randint(-3, 3))),
		  		 mouse.move_time(), mouse.mouse_path())
		mouse.click()
		keyboard.keypress('ctrl')
		return 1
	elif asteroid_small is not None:
		(asteroid_smallx, asteroid_smally) = asteroid_small
		pag.moveTo((asteroid_smallx + (random.randint(-2, 200))),
		  		 (asteroid_smally + (random.randint(-3, 3))),
		  		 mouse.move_time(), mouse.mouse_path())
		mouse.click()
		keyboard.keypress('ctrl')
		time.sleep(float(random.randint(500, 1500)) / 1000)
		return 1
	else:
		print('target_ore -- no asteroids to target')
		return 0


def check_hold_popup():
	# check for popup indicating cargo hold is full
	# 'cargo hold full' popup lasts about 5 seconds, so check for this popup once every 3 seconds
	cargo_hold_full = pag.locateCenterOnScreen('./img/cargo_hold_full.bmp', confidence=0.90,
												region=(0, 0, screenwidth, screenheight))
	if cargo_hold_full is None:
		return 0
	elif cargo_hold_full is not None:
		print('cargo_hold_popup -- found popup')
		return 1


def check_asteroid_depleted_popup():
	# check for popup indicating asteroid has been depleted
	asteroid_depleted = pag.locateCenterOnScreen('./img/asteroid_depleted.bmp', confidence=0.90,
												region=(0, 0, screenwidth, screenheight))
	if asteroid_depleted is None:
		return 0
	elif asteroid_depleted is not None:
		print('asteroid_depleted_popup -- found popup')
		return 1


def activate_mining_laser():
	# turn on mining lasers to mine ore
	if mining_lasers == 1:
		keyboard.keypress('f1')
	elif mining_lasers == 2:
		keyboard.keypress('f1')
		keyboard.keypress('f2')
	elif mining_lasers == 3:
		keyboard.keypress('f1')
		keyboard.keypress('f2')
		keyboard.keypress('f3')
	elif mining_lasers == 4:
		keyboard.keypress('f1')
		keyboard.keypress('f2')
		keyboard.keypress('f3')
		keyboard.keypress('f4')
	print('activate_mining_laser -- activated lasers')
	return 1
