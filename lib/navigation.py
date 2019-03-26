import sys
import time
import ctypes
import random
import traceback

import pyautogui as pag

from lib import mouse

pag.FAILSAFE = True
sys.setrecursionlimit(100000)
conf = 0.95
alignment_time = 6  # time required before ship begins warp, round up to the nearest second

# get monitor resolution, used to speed up image searching
user32 = ctypes.windll.user32
screenwidth = user32.GetSystemMetrics(0)
screenheight = user32.GetSystemMetrics(1)
halfscreenwidth = (int(screenwidth / 2))
halfscreenheight = (int(screenheight / 2))

destnum = {0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "10"}
bookmark_dict = {1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "10"}

def route_set():
	# check to see if a route has actually been set
	route = pag.locateCenterOnScreen('./img/route_set.bmp', confidence=0.9,
									 region=(0, 0, (int(screenwidth / 4)), screenheight))
	if route is None:
		sys.exit('no route set!')
	else:
		return


def focus_overview():
	# click on overview to focus EVE window
	pag.moveTo((screenwidth - (random.randint(10, 230))),
			   (75 + (random.randint(0, (screenheight - 10)))),
			   mouse.move_time(), mouse.mouse_path())
	time.sleep(float(random.randint(50, 500)) / 1000)
	mouse.click()
	return


def warp_to_waypoint():
	# click on current waypoint and hold down warp hotkey to warp to waypoint
	# look for station icon
	print('looking for waypoints')
	warp_to_waypoint_tries = 0
	# search right half of screen only for stargate icon
	stargate_waypoint = pag.locateCenterOnScreen('./img/stargate_waypoint.bmp', confidence=0.96,
												 region=(halfscreenwidth, 0, screenwidth, screenheight))
	# if stargate waypoint not found, look for station waypoint
	while stargate_waypoint is None and warp_to_waypoint_tries < 15:
		warp_to_waypoint_tries += 1
		station_waypoint = pag.locateCenterOnScreen('./img/station_waypoint.bmp', confidence=0.96,
													region=(halfscreenwidth, 0, screenwidth, screenheight))
		# if station waypoint not found, look for stargate waypoint again and restart loop
		if station_waypoint is None:
			stargate_waypoint = pag.locateCenterOnScreen('./img/stargate_waypoint.bmp', confidence=0.96,
														 region=(halfscreenwidth, 0, screenwidth, screenheight))
			print('looking for waypoints...', warp_to_waypoint_tries)
			time.sleep(float(random.randint(400, 1200)) / 1000)
			continue
		elif station_waypoint is not None:
			print('found station waypoint')
			(station_waypointx, station_waypointy) = station_waypoint  # separate x and y coordinates of location
			pag.moveTo((station_waypointx + (random.randint(-8, 8))),
					   (station_waypointy + (random.randint(-8, 8))),
					   mouse.move_time(), mouse.mouse_path())
			pag.keyDown('d')  # hotkey to hold down to warp when clicking on waypoint in overview
			time.sleep(float(random.randint(600, 1200)) / 1000)
			mouse.click()
			pag.keyUp('d')
			# move mouse away from button to prevent tooltips from blocking other buttons
			pag.moveTo((random.randint(0, (screenheight - 100))),
					   (random.randint(0, ((screenwidth - 100) / 2))),
					   mouse.move_time(), mouse.mouse_path())
			return 2
	# check if stargate waypoint was found before loop expired
	if stargate_waypoint is not None and warp_to_waypoint_tries < 15:
		print('found stargate waypoint')
		(stargate_waypointx, stargate_waypointy) = stargate_waypoint
		pag.moveTo((stargate_waypointx + (random.randint(-8, 8))),
				   (stargate_waypointy + (random.randint(-8, 8))),
				   mouse.move_time(), mouse.mouse_path())
		pag.keyDown('d')
		time.sleep(float(random.randint(600, 1200)) / 1000)
		mouse.click()
		pag.keyUp('d')
		pag.moveTo((random.randint(150, (int(screenheight - (screenheight / 4))))),
				   (random.randint(150, (int(screenwidth - (screenwidth / 4))))),
				   mouse.move_time(), mouse.mouse_path())
		return 1
	# if can't find any waypoints, dock at nearest station
	elif stargate_waypoint is None and warp_to_waypoint_tries > 15:
		print('error with warp_to_waypoint, no waypoints found')
		emergency_terminate()
		traceback.print_stack()
		sys.exit()


def warp_to_first_bookmark_in_system():
	# warp to lowest-numbered bookmark in the system higher than 0
	# bookmark names must be preceded with a 1-digit number higher than 0 (ex: 1spot_in_system_A)
	# bookmark 0 is the home station
	bnum = 1
	global defined_bookmark_in_system
	# check if bookmark 1 is in the current system. if so, warp to it. if not, increment by 1 and try again
	defined_bookmark_in_system = pag.locateCenterOnScreen(('./img/dest/at_dest' + (bookmark_dict[bnum]) + '.bmp'),
														  confidence=0.98,
														  region=(0, 0, halfscreenwidth, screenheight))
	while defined_bookmark_in_system is None:
		bnum = bnum + 1
		defined_bookmark_in_system = pag.locateCenterOnScreen(('./img/dest/at_dest' + (bookmark_dict[bnum]) + '.bmp'),
															  confidence=0.98,
															  region=(0, 0, halfscreenwidth, screenheight))
		if bnum == 9 and defined_bookmark_in_system is None:
			print('out of bookmarks in system to look for')
			return 0
	if defined_bookmark_in_system is not None:
		print('found bookmark' + (bookmark_dict[bnum]))
		(bookmark_in_systemx), (bookmark_in_systemy) = defined_bookmark_in_system
		pag.moveTo((bookmark_in_systemx + (random.randint(-1, 200))), (bookmark_in_systemy +
										(random.randint(-3, 3))), mouse.move_time(), mouse.mouse_path())
		mouse.click_right()
		pag.moveRel((0 + (random.randint(10, 80))), (0 + (random.randint(20, 25))),
					mouse.move_time(), mouse.mouse_path())
		mouse.click()
		time.sleep(2)
		return 1


def warp_to_defined_bookmark_in_system(gotosite):
	# warp to a predefined bookmark number in the current system
	# if ship is already at the requested site, return function
	if gotosite = atsite:
		print('already at bookmark',atsite)
		return 0
	else:
		defined_bookmark_in_system = pag.locateCenterOnScreen(('./img/dest/at_dest' + (bookmark_dict[gotosite]) + '.bmp'),
																confidence=0.95,
																region=(0, 0, halfscreenwidth, screenheight))
		# if cant find the site number, return function
		while defined_bookmark_in_system is None:
			print('bookmark',gotosite,'not found in system')
			return 0
		if defined_bookmark_in_system is not None:
				print('found bookmark',gotosite)
				(bookmark_in_systemx), (bookmark_in_systemy) = defined_bookmark_in_system
				pag.moveTo((bookmark_in_systemx + (random.randint(-1, 200))), (bookmark_in_systemy +
													(random.randint(-3, 3))), mouse.move_time(), mouse.mouse_path())
				mouse.click_right()
				pag.moveRel((0 + (random.randint(10, 80))), (0 + (random.randint(10, 15))),
									mouse.move_time(), mouse.mouse_path())
				mouse.click()
				time.sleep(2)
				return 1


def emergency_terminate():
	# if a certain function breaks or times out while undocked, look for nearest station and dock immediately
	# incrementally lower confidence required to match station icon each time loop runs
	# if station cannot be found after 20 loops, warp to nearest celestial instead and immediately logout
	print('emergency termination called!')
	tries = 0
	confidence = 0.99
	station_icon = pag.locateCenterOnScreen('./img/station_icon.bmp', confidence=confidence,
											region=(0, 0, screenwidth, screenheight))
	while station_icon is None and tries <= 20:
		print('looking for station to emergency dock at')
		tries += 1
		confidence -= 0.01
		station_icon = pag.locateCenterOnScreen('./img/station_icon.bmp', confidence=confidence,
												region=(0, 0, screenwidth, screenheight))
	if station_icon is not None and tries <= 20:
		print('emergency docking')
		(station_iconx, station_icony) = station_icon
		pag.moveTo((station_iconx + (random.randint(-2, 50))),
					(station_icony + (random.randint(-2, 2))),
					mouse.move_time(), mouse.mouse_path())
		mouse.click()
		time.sleep(float(random.randint(600, 1200)) / 1000)
		pag.keyDown('d')
		time.sleep(float(random.randint(600, 1200)) / 1000)
		pag.keyUp('d')
		pag.moveTo((random.randint(150, (int(screenheight - (screenheight / 4))))),
					(random.randint(150, (int(screenwidth - (screenwidth / 4))))),
					mouse.move_time(), mouse.mouse_path())
		time.sleep(180)
		emergency_logout()
		return 1
	else:
		print("couldn't find station to emergency dock at, warping to celestial instead")
		tries = 0
		confidence = 0.99
		celestial_icon = pag.locateCenterOnScreen('./img/celestial_icon.bmp', confidence=confidence,
													region=(0, 0, screenwidth, screenheight))
		while celestial_icon is None and tries <= 40:
			print('looking for celestial')
			tries += 1
			confidence -= 0.01
			celestial_icon = pag.locateCenterOnScreen('./img/celestial_icon.bmp', confidence=confidence,
														region=(0, 0, screenwidth, screenheight))
		if celestial_icon is not None and tries <= 40:
			print('emergency warping to celestial')
			(celestial_iconx, celestial_icony) = celestial_icon
			pag.moveTo((celestial_iconx + (random.randint(-2, 50))),
						(celestial_icony + (random.randint(-2, 2))),
						mouse.move_time(), mouse.mouse_path())
			mouse.click()
			time.sleep(float(random.randint(600, 1200)) / 1000)
			pag.keyDown('w')
			time.sleep(float(random.randint(600, 1200)) / 1000)
			pag.keyUp('w')
			pag.moveTo((random.randint(150, (int(screenheight - (screenheight / 4))))),
						(random.randint(150, (int(screenwidth - (screenwidth / 4))))),
						mouse.move_time(), mouse.mouse_path())
			time.sleep(180)
			emergency_logout()
		else:
			print('error with emergency_terminate function, out of celestials to look for')
			emergency_logout()
		return 0


def emergency_logout():
	return

def detect_warp():
	# detect when warp to a bookmark has been completed to a bookmark by checking if the bookmark's right-click
	# wait for ship to begin warp before checking for 'warping' image, otherwise it will get confused
	print('waiting for warp to complete')
	time.sleep(alignment_time)
	warp_time = 1
	warp_drive_active = pag.locateCenterOnScreen('./img/warping.bmp',
												 confidence=0.90,
												 region=(0, 0, screenwidth, screenheight))
	while warp_drive_active is not None and warp_time < 300:
		print('warping...')
		warp_time += 1
		time.sleep(float(random.randint(1000, 3000)) / 1000)
		warp_drive_active = pag.locateCenterOnScreen('./img/warping.bmp',
													 confidence = 0.90,
													 region = (0, 0, screenwidth, screenheight))
	if warp_drive_active is None and warp_time < 300:
		time.sleep(float(random.randint(1000, 3000)) / 1000)
		print('warp completed')
		return 1
	if warp_drive_active is None and warp_time >= 300:
		print('error with detect_warp, timed out waiting for warp')
		emergency_terminate()
		return 0


def detect_warp_to_bookmark_in_system():
	# detect when warp to a bookmark has been completed to a bookmark by checking if the bookmark's right-click
	# menu still has a 'warp to' option. if the option is not present, ship has arrived at bookmark
	(defined_bookmark_in_systemx), (defined_bookmark_in_systemy) = defined_bookmark_in_system
	warp_to_bookmark_tries = 0
	pag.moveTo((defined_bookmark_in_systemx + (random.randint(-1, 200))), (defined_bookmark_in_systemy +
												(random.randint(-3, 3))), mouse.move_time(), mouse.mouse_path())
	mouse.click_right()
	print('waiting for warp')
	at_bookmark_in_system = pag.locateCenterOnScreen('./img/detect_warp_to_bookmark.bmp',
													confidence=0.85,
													region=(0, 0, screenwidth, screenheight))
	while at_bookmark_in_system is None and warp_to_bookmark_tries < 50:
		time.sleep(float(random.randint(1000, 3000)) / 1000)
		focus_overview()
		time.sleep(float(random.randint(5000, 10000)) / 1000)
		warp_to_bookmark_tries += 1
		pag.moveTo((defined_bookmark_in_systemx + (random.randint(-1, 200))), (defined_bookmark_in_systemy +
										(random.randint(-3, 3))), mouse.move_time(), mouse.mouse_path())
		mouse.click_right()
		at_bookmark_in_system = pag.locateCenterOnScreen('./img/detect_warp_to_bookmark.bmp',
														 confidence=0.98,
														 region=(0, 0, halfscreenwidth, screenheight))
	if at_bookmark_in_system is None and warp_to_bookmark_tries >= 50:
		emergency_terminate()
		return 0
	if at_bookmark_in_system is not None and warp_to_bookmark_tries < 50:
		print('warp completed')
		return 1


def detect_jump():
	# detect jump by looking for cyan session change icon in top left corner
	detect_jump_loop_num = 0
	session_change_cloaked = pag.locateCenterOnScreen('./img/session_change_cloaked.bmp', confidence=0.55,
													  region=(0, 0, (int(screenwidth / 5)), screenheight))
	while session_change_cloaked is None and detect_jump_loop_num < 180:
		detect_jump_loop_num += 1
		print('waiting for jump...', detect_jump_loop_num)
		time.sleep(1.5)
		# search right fifth of screen only
		session_change_cloaked = pag.locateCenterOnScreen('./img/session_change_cloaked.bmp', confidence=0.55,
														  region=(0, 0, (int(screenwidth / 5)), screenheight))
		# after 50 checks, look for 'low sec system' popup
		if session_change_cloaked is not None and detect_jump_loop_num > 50:
			low_sec_popup = pag.locateCenterOnScreen('./img/low_security_system.bmp', confidence=0.9,
													 region=(0, 0, screenwidth, screenheight))
			if low_sec_popup is not None:
				pag.keyDown('enter')
				time.sleep(float(random.randint(20, 700)) / 1000)
				pag.keyDown('enter')
				continue
			else:
				continue
	if session_change_cloaked is not None and detect_jump_loop_num < 180:
		print('jump detected')
		time.sleep(float(random.randint(900, 2400)) / 1000)
		return 1
	else:
		print('error with detect_jump, timed out looking for jump')
		emergency_terminate()
		traceback.print_stack()
		sys.exit()


def detect_dock():
	# detect dock by looking for undock icon
	detect_dock_loop_num = 0
	docked = pag.locateCenterOnScreen('./img/undock.bmp', confidence=0.91,
									  region=(halfscreenwidth, 0, screenwidth, screenheight))
	while docked is None and detect_dock_loop_num < 100:
		detect_dock_loop_num += 1
		print('waiting for dock...', detect_dock_loop_num)
		time.sleep(3)
		# search right half of screen only
		docked = pag.locateCenterOnScreen('./img/undock.bmp', confidence=0.91,
										  region=(halfscreenwidth, 0, screenwidth, screenheight))
	if docked is not None and detect_dock_loop_num < 100:
		print('detected dock')
		time.sleep(float(random.randint(2000, 5000)) / 1000)
		return 1
	else:
		print('error with detect_dock, timed out looking for dock')
		emergency_terminate()
		traceback.print_stack()
		sys.exit()


def at_dest_num():
	# figure out which bookmark the ship is at
	global at_dest_num_var
	n = 0
	# confidence must be higher than normal because script frequently mistakes dest3 for dest2
	at_dest = pag.locateCenterOnScreen(('./img/dest/at_dest' + (destnum[n]) + '.bmp'), confidence=0.98,
									   region=(0, 0, halfscreenwidth, screenheight))
	while at_dest is None:
		n = n + 1
		at_dest = pag.locateCenterOnScreen(('./img/dest/at_dest' + (destnum[n]) + '.bmp'), confidence=0.98,
										   region=(0, 0, halfscreenwidth, screenheight))
		print('looking if at destination' + (destnum[n]))
		if n == 9 and at_dest is None:
			print('out of destinations to look for')
			return -1  # if not at a recognizable station, undock and continue route
	if at_dest is not None:
		print('at dest' + (destnum[n]))
		at_dest_num_var = n
		return at_dest_num_var  # return number of station ship is docked in


def blacklist_station():
	# determine which station the ship is in and blacklist the station by editing its bookmark name
	# this will prevent further trips to the blacklisted station
	at_dest = at_dest_num()
	if at_dest is not None:
		print('blacklisting station')
		at_dest = pag.locateCenterOnScreen(('./img/dest/at_dest' + (destnum[at_dest_num_var]) + '.bmp'),
										   confidence=conf,
										   region=(0, 0, halfscreenwidth, screenheight))
		(at_destx), (at_desty) = at_dest
		pag.moveTo((at_destx + (random.randint(-1, 200))), (at_desty + (random.randint(-3, 3))),
				   mouse.move_time(), mouse.mouse_path())
		time.sleep(float(random.randint(1000, 2000)) / 1000)
		mouse.click()  # click once to focus entry, then double-click entry to open edit menu
		time.sleep(float(random.randint(1000, 2000)) / 1000)
		mouse.click()
		time.sleep(float(random.randint(5, 50)) / 1000)
		mouse.click()
		time.sleep(float(random.randint(3000, 4000)) / 1000)
		pag.keyDown('home')
		time.sleep(float(random.randint(0, 500)) / 1000)
		pag.keyUp('home')
		time.sleep(float(random.randint(0, 1000)) / 1000)
		pag.keyDown('b')  # add a 'b' to beginning of name indicating station is blacklisted
		pag.keyUp('b')
		time.sleep(float(random.randint(0, 1000)) / 1000)
		pag.keyDown('enter')
		time.sleep((random.randint(0, 200)) / 100)
		pag.keyUp('enter')
		return
	else:
		return


def blacklist_site(atsite):
	# blacklist the specified bookmark by editing its bookmark name
	# this will prevent further trips to the blacklisted site
	print('blacklisting site')
	site_to_blacklist = pag.locateCenterOnScreen(('./img/dest/at_dest' + site + '.bmp'),
												confidence=conf,
												region=(0, 0, halfscreenwidth, screenheight))
	(site_to_blacklistx), (site_to_blacklisty) = site_to_blacklist
	pag.moveTo((site_to_blacklistx + (random.randint(-1, 200))),
				(site_to_blacklisty + (random.randint(-3, 3))),
				mouse.move_time(), mouse.mouse_path())
	time.sleep(float(random.randint(1000, 2000)) / 1000)
	mouse.click()  # click once to focus entry, then double-click entry to open edit menu
	time.sleep(float(random.randint(1000, 2000)) / 1000)
	mouse.click()
	time.sleep(float(random.randint(5, 50)) / 1000)
	mouse.click()
	time.sleep(float(random.randint(3000, 4000)) / 1000)
	pag.keyDown('home')
	time.sleep(float(random.randint(0, 500)) / 1000)
	pag.keyUp('home')
	time.sleep(float(random.randint(0, 1000)) / 1000)
	pag.keyDown('b')
	pag.keyUp('b')
	time.sleep(float(random.randint(0, 1000)) / 1000)
	pag.keyDown('enter')
	time.sleep((random.randint(0, 200)) / 100)
	pag.keyUp('enter')
	return 1


def set_dest():
	# set next destination to the lowest-numbered destination that isnt blacklisted (starting with 1)
	next_dest = pag.locateCenterOnScreen(('./img/dest/dest' + (destnum[1]) + '.bmp'),
										 confidence=0.98,
										 region=(0, 0, halfscreenwidth, screenheight))
	next_dest_var = 1
	while next_dest is None:
		next_dest_var = next_dest_var + 1
		next_dest = pag.locateCenterOnScreen(('./img/dest/dest' + (destnum[next_dest_var]) + '.bmp'),
											 confidence=0.98,
											 region=(0, 0, halfscreenwidth, screenheight))
		print('looking for dest' + (destnum[next_dest_var]))
	if next_dest is not None:
		print('setting destination waypoint')
		(next_destx), (next_desty) = next_dest
		pag.moveTo((next_destx + (random.randint(-1, 200))), (next_desty + (random.randint(-3, 3))),
				   mouse.move_time(), mouse.mouse_path())
		mouse.click_right()
		pag.moveRel((0 + (random.randint(10, 80))), (0 + (random.randint(20, 25))),
					mouse.move_time(), mouse.mouse_path())
		mouse.click()
		time.sleep(2)
		return


def at_home_check():
	# check if ship has arrived back at its home station by looking for an entry in 'people and places'
	# starting with 3 0's
	at_home = pag.locateCenterOnScreen('./img/dest/at_dest0.bmp', confidence=conf,
									   region=(0, 0, halfscreenwidth, screenheight))
	if at_home is None:
		return 0
	elif at_home is not None:
		print('at home station')
		return 1


def set_home():
	# return to home station (the home station has 000 in front of name in 'people and places')
	print('setting home waypoint')
	home = pag.locateCenterOnScreen('./img/dest/dest0.bmp', confidence=conf,
									region=(0, 0, halfscreenwidth, screenheight))
	(homex, homey) = home
	pag.moveTo((homex + (random.randint(-1, 200))), (homey + (random.randint(-3, 3))),
				mouse.move_time(), mouse.mouse_path())
	mouse.click_right()
	pag.moveRel((0 + (random.randint(10, 80))), (0 + (random.randint(20, 25))),
				mouse.move_time(), mouse.mouse_path())
	mouse.click()
	return
