import time

import pyautogui as pag

from lib import navigation as nav
from lib import docked
from lib import unload_ship
from lib import main


user32 = ctypes.windll.user32
screenwidth = user32.GetSystemMetrics(0)
screenheight = user32.GetSystemMetrics(1)
halfscreenwidth = (int(screenwidth / 2))
halfscreenheight = (int(screenheight / 2))


def miner():
	check_hold()
	if check_hold() == 1:
		travel_to_site()
		if travel_to_site() == 1:
			check_for_ore()
			check_for_hostiles()
			check_for_players()
			# if ore is not present, hostiles are present, or other players are present, find another site
			if check_for_ore() == 0 or check_for_hostiles() == 0 or check_for_players() == 0:
				miner()
			else:
				target_ore()
	elif check_hold() == 0:
		nav.set_home()
		main.navigator()
		if main.navigator() == 1:
			unload_ship.unload_ship()
			if unload_ship.unload_ship() == 1:
				docked.undock()
				miner()

def travel_to_site():
	# find a suitable asteroid field
	global site
	site = 1
	nav.warp_to_defined_bookmark_in_system(site)
	# warp to the first available bookmark in the system
	while nav.warp_to_defined_bookmark_in_system(site) == 0:
		site = site + 1
		nav.warp_to_defined_bookmark_in_system(site)
	if nav.warp_to_defined_bookmark_in_system(site) == 1:
		nav.detect_warp_to_bookmark_in_system()
		# wait for warp to complete
		while nav.detect_warp_to_bookmark_in_system() == 0:
			time.sleep(1)
			nav.detect_warp_to_bookmark_in_system()
		if nav.detect_warp_to_bookmark_in_system() == 1:
			return 1

#def check_for_hostiles()  # check entire screen for red ship icons, indicating hostile vessels

#def check_for_players()  # check entire screen for other ship icons


def check_for_ore():
	# if the current site doesn't contain any ore, blacklist it and warp to next site
	asteroid_small = pag.locateCenterOnScreen('./img/asteroid_s.bmp', confidence=0.90,
										region=(0, 0, screenwidth, screenheight))
	asteroid_medium = pag.locateCenterOnScreen('./img/asteroid_m.bmp', confidence=0.90,
										region=(0, 0, screenwidth, screenheight))
	asteroid_large = pag.locateCenterOnScreen('./img/asteroid_l.bmp', confidence=0.90,
										region=(0, 0, screenwidth, screenheight))
	if asteroid_small is None and asteroid_medium is None and asteroid_large is None:
		nav.blacklist_site(site)
		return 0
	elif asteroid_small is not None or asteroid_medium is not None or asteroid_large is not None:
		return 1


#def target_ore()  # target closest ore in overview, if no ore is found, warp to next bookmark

def check_hold():  # check cargohold to see if at capacity
	# 'cargo hold full' popup lasts about 5 seconds, so check for this popup once every three seconds
	cargo_hold_check = 1
	cargo_hold_full = pag.locateCenterOnScreen('./img/cargo_hold_full.bmp', confidence=0.90,
												region=(0, 0, screenwidth, screenheight))
	while cargo_hold_full is None and cargo_hold_check < 600:
		time.sleep(3)
		cargo_hold_check += 1
		cargo_hold_full = pag.locateCenterOnScreen('./img/cargo_hold_full.bmp', confidence = 0.90,
													region = (0, 0, screenwidth, screenheight))
	if cargo_hold_full is not None and cargo_hold_check <= 600:
		return 1
	else:
		print('error with cargohold checking')

#def activate_mining_laser()  # turn on mining lasers to mine ore