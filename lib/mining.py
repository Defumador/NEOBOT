import time

from lib import navigation as nav
from lib import docked
from lib import unload_ship
from lib import main


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

def check_for_hostiles()  # check entire screen for red ship icons, indicating hostile vessels

def check_for_players()  # check entire screen for other ship icons

def check_for_ore():
	# if the current site doesn't contain any ore, blacklist it
	ore =
	if ore is None
		nav.blacklist_site(site)
		return 0

def target_ore()  # target closest ore in overview, if no ore is found, warp to next bookmark

def check_hold()  # check cargohold to see if at capacity

def activate_mining_laser()  # turn on mining lasers to mine ore

