import sys
import time
import ctypes
import random

import pyautogui as pag

from lib import mouse
from lib import keyboard

pag.FAILSAFE = True  # force script to stop if move mouse into top left corner of screen
sys.setrecursionlimit(100000)  # set high recursion limit for repeating functions
conf = 0.95  # set default confidence value for imagesearch  

# obtain screen dimensions
user32 = ctypes.windll.user32
screenwidth = user32.GetSystemMetrics(0)
screenheight = user32.GetSystemMetrics(1)
halfscreenwidth = (int(screenwidth / 2))
halfscreenheight = (int(screenheight / 2))


def docked_check():
	# check if ship is docked
	undock_icon = pag.locateCenterOnScreen('./img/undock.bmp', confidence=conf)
	if undock_icon is None:
		print('not docked')
		return 0
	elif undock_icon is not None:
		print('docked')
		return 1


def open_cargo_hold():
	# click on ship cargo hold button in inventory window while docked
	print('opening cargo hold')
	cargo_hold = pag.locateCenterOnScreen('./img/cargo_hold.bmp', confidence=conf)
	while cargo_hold is None:
		print('cant find cargo hold')
		cargo_hold = pag.locateCenterOnScreen('./img/cargo_hold.bmp', confidence=conf)
		time.sleep(1)
	else:
		(cargo_holdx, cargo_holdy) = cargo_hold
		pag.moveTo((cargo_holdx + (random.randint(-4, 50))),
					(cargo_holdy + (random.randint(-6, 6))),
					mouse.move_time(), mouse.mouse_path())
		mouse.click()
		return


def open_special_hold():
	# if a special hold was found, click on it in inventory window while docked
	print('opening special hold')
	special_hold = pag.locateCenterOnScreen('./img/special_hold.bmp', confidence=conf)
	while special_hold is None:
		print('cant find special hold')
		special_hold = pag.locateCenterOnScreen('./img/special_hold.bmp', confidence=conf)
		time.sleep(1)
	else:
		(special_holdx, special_holdy) = special_hold
		pag.moveTo((special_holdx + (random.randint(-4, 50))),
					(special_holdy + (random.randint(15, 30))),
					mouse.move_time(), mouse.mouse_path())
		mouse.click()
		return


def open_station_hangar():
	# click on station hangar button in inventory window while docked
	print('opening station hangar')
	station_hangar = pag.locateCenterOnScreen('./img/station_hangar.bmp', confidence=conf)
	while station_hangar is None:
		print('cant find inventory station hangar icon')
		station_hangar = pag.locateCenterOnScreen('./img/station_hangar.bmp', confidence=conf)
		time.sleep(1)
	else:
		(station_hangarx, station_hangary) = station_hangar
		pag.moveTo((station_hangarx + (random.randint(-6, 50))),
					(station_hangary + (random.randint(-6, 6))),
					mouse.move_time(), mouse.mouse_path())
		mouse.click()
		return


def focus_inventory_window():
	# click inside the station inventory window to focus it before any items are selected
	# look for sorting buttons in top right corner of inventory window and offset mouse
	sorting_station_hangar = pag.locateCenterOnScreen('./img/sorting_station_hangar.bmp', confidence=conf)
	while sorting_station_hangar is None:
		print('cant find sorting icon')
		sorting_station_hangar = pag.locateCenterOnScreen('./img/sorting_station_hangar.bmp', confidence=conf)
		time.sleep(1)
	else:
		(sorting_station_hangarx, sorting_station_hangary) = sorting_station_hangar
		# offset mouse from sorting button to click within inventory window to focus it
		pag.moveTo((sorting_station_hangarx - (random.randint(0, 250))),
					(sorting_station_hangary + (random.randint(50, 300))),
					mouse.move_time(), mouse.mouse_path())
		mouse.click()
		return


def look_for_items():
	# look at the bottom-right corner of station inventory window to determine if '0 items found' appears
	global no_items_station_hangar  # var must be global since it's used in other functions
	global namefield_station_hangar
	no_items_station_hangar = pag.locateCenterOnScreen('./img/no_items_station_hangar.bmp',
														confidence=.99)
	if no_items_station_hangar is None:
		namefield_station_hangar = pag.locateCenterOnScreen('./img/namefield_station_hangar.bmp',
															confidence=conf)
		return 1
	elif no_items_station_hangar is not None:
		print('no more items')
		return 0


def look_for_special_hold():
	# look for drop-down arrow next to ship icon in station inventory window to determine if
	# ship has special hold
	special_hold = pag.locateCenterOnScreen('./img/special_hold.bmp', confidence=conf)
	no_additional_bays = pag.locateCenterOnScreen('./img/no_additional_bays.bmp', confidence=conf)
	if special_hold is not None and no_additional_bays is None:
		print('found special hold')
		return 1
	else:
		return 0


def special_hold_warning():
	# look for warning indicating selected items aren't compatible with ship's special hold
	# special hold warning is partially transparent so confidence rating must be slightly lower than normal
	special_hold_warning_popup = pag.locateCenterOnScreen('./img/special_hold_warning.bmp', confidence=0.8)
	if special_hold_warning_popup is None:
		return 0
	else:
		print('detected special hold warning')
		return 1


def set_quantity_popup():
	# check if 'set quantity' popup appears indicating not enough space in cargo hold for full item stack
	set_quantity = pag.locateCenterOnScreen('./img/set_quantity.bmp', confidence=conf)
	if set_quantity is None:
		return 0
	else:
		print('found set quantity popup')
		keyboard.enter()
		return 1


def not_enough_space_popup():
	# check if 'not enough space' popup appears indicating not all item stacks will
	# fit into hold or hold is already full
	not_enough_space = pag.locateCenterOnScreen('./img/not_enough_space.bmp', confidence=conf)
	if not_enough_space is None:
		return 0
	else:
		print('found not enough space popup')
		keyboard.enter()
		return 1


def undock():
	# undock from station, look for undock button in right half of screen only
	print('undocking')
	pag.keyDown('alt')  # alt+u is default undock hotkey
	time.sleep(float(random.randint(200, 1200)) / 1000)
	pag.keyDown('u')
	time.sleep(float(random.randint(200, 1200)) / 1000)
	pag.keyUp('u')
	time.sleep(float(random.randint(200, 1200)) / 1000)
	pag.keyUp('alt')
	# look for cyan ship icon in top left corner with ring around it indicating session change
	time.sleep(int((random.randint(5000, 10000) / 1000)))
	undocked = pag.locateCenterOnScreen('./img/session_change_undocked.bmp', confidence=0.55,
										region=(0, 0, (int(screenwidth / 5)), screenheight))
	while undocked is None:
		time.sleep(int((random.randint(3000, 10000) / 1000)))
		print('trying undocking second time')
		pag.keyDown('alt')  # alt+u is default undock hotkey
		time.sleep(float(random.randint(200, 1200)) / 1000)
		pag.keyDown('u')
		time.sleep(float(random.randint(200, 1200)) / 1000)
		pag.keyUp('u')
		time.sleep(float(random.randint(200, 1200)) / 1000)
		pag.keyUp('alt')
		time.sleep(int((random.randint(5000, 10000) / 1000)))
		undocked = pag.locateCenterOnScreen('./img/session_change_undocked.bmp', confidence=0.55,
											region=(0, 0, (int(screenwidth / 5)), screenheight))
	if undocked is not None:
		time.sleep(int((random.randint(2000, 3000) / 1000)))
		return