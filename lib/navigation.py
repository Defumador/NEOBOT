import sys
import time
import ctypes
import random
import traceback

import pyautogui as pag

from lib import mouse
from lib import keyboard

global windowx
global windowy
global originx
global originy
global conf
global alignment_time
import ctypes



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
origin = pag.locateCenterOnScreen('./img/buttons/neocom.bmp', confidence=0.90)
(originx, originy) = origin

# move the origin up and to the left slightly to get it to the exact top
# left corner of the eve client window. This is necessary  because the image
# searching algorithm returns coordinates to the center of the image rather
# than its top right corner.
windowx = originx + window_resolutionx
windowy = originy + window_resolutiony



sys.setrecursionlimit(9999999)

# Create dictionary for concatenating an integer variable with a file name to
# match images related to that variable.
destnum = {0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7",
           8: "8", 9: "9", 10: "10"}
bookmark_dict = {1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7",
                 8: "8", 9: "9", 10: "10"}


def route_set():
    # Check the top-left corner of the hud to see if a route has actually been
    # set by the user.
    route = pag.locateCenterOnScreen('./img/indicators/route_set.bmp',
                                     confidence=0.85,
                                     region=(originx, originy,
                                             windowx, windowy))
    if route is None:
        print('route_set -- no route set!')
        sys.exit(0)
    else:
        return


def set_dest():
    # Issue a 'set destination' command for the lowest-numbered bookmark that
    # isn't blacklisted (starting with 1).
    next_dest = pag.locateCenterOnScreen(
        ('./img/dest/dest' + (destnum[1]) + '.bmp'),
        confidence=0.98,
        region=(originx, originy, windowx, windowy))

    next_dest_var = 1
    while next_dest is None:
        next_dest_var += 1
        next_dest = pag.locateCenterOnScreen(
            ('./img/dest/dest' + (destnum[next_dest_var]) + '.bmp'),
            confidence=0.98,
            region=(originx, originy, windowx, windowy))
        print('set_dest -- looking for dest' + (destnum[next_dest_var]))

    if next_dest is not None:
        print('set_dest -- setting destination waypoint')
        (next_destx), (next_desty) = next_dest
        pag.moveTo((next_destx + (random.randint(-1, 200))),
                   (next_desty + (random.randint(-3, 3))),
                   mouse.duration(), mouse.path())
        mouse.click_right()
        pag.moveRel((0 + (random.randint(10, 80))),
                    (0 + (random.randint(20, 25))),
                    mouse.duration(), mouse.path())
        mouse.click()
        time.sleep(2)
        return


def at_home_check():
    # Check if the ship is at its home station by looking for a bookmark
    # starting with '000'.
    at_home = pag.locateCenterOnScreen('./img/dest/at_dest0.bmp',
                                       confidence=conf,
                                       region=(originx, originy,
                                               windowx, windowy))
    if at_home is None:
        return 0
    elif at_home is not None:
        print('at_home_check -- at home station')
        return 1


def set_home():
    # Set destination as the bookmark beginning with '000'.
    print('set_home -- setting home waypoint')
    home = pag.locateCenterOnScreen('./img/dest/dest0.bmp',
                                    confidence=conf,
                                    region=(originx, originy,
                                            windowx, windowy))
    if home is not None:
        (homex, homey) = home
        pag.moveTo((homex + (random.randint(-1, 200))),
                   (homey + (random.randint(-3, 3))),
                   mouse.duration(), mouse.path())
        mouse.click_right()
        pag.moveRel((0 + (random.randint(10, 80))), (0 + (random.randint(20, 25))),
                    mouse.duration(), mouse.path())
        mouse.click()
        return 1
    else:
        print("set_home -- couldn't find home waypoint")
        return 0


    # !! needs work to transition to windowx,windowy
def focus_overview():
    # Click on the overview window to focus the eve client window.
    print('focus_overview -- called')
    pag.moveTo((windowx - (random.randint(10, 230))),
               (75 + (random.randint(0, (windowy - 10)))),
               mouse.duration(), mouse.path())
    time.sleep(float(random.randint(50, 500)) / 1000)
    mouse.click()
    return 1


def warp_to_waypoint():
    # Click on the current waypoint and use warp hotkey to warp to waypoint.
    # Currently supports warping to stargate and station waypoints.
    print('warp_to_waypoint -- looking for waypoints')
    tries = 1
    # Speed up image searching by checking right half of eve window only. This
    # obviously requires the user to place the overview on the right half of
    # the client window.
    stargate_waypoint = pag.locateCenterOnScreen(
        './img/overview/stargate_waypoint.bmp',
        confidence=0.96,
        region=(originx, originy, windowx, windowy))
    # If stargate waypoint not found, look for station waypoint.
    while stargate_waypoint is None and tries <= 15:
        tries += 1
        station_waypoint = pag.locateCenterOnScreen(
            './img/overview/station_waypoint.bmp',
            confidence=0.96,
            region=(originx, originy, windowx, windowy))
        # If station waypoint not found, look for stargate waypoint again
        # and restart loop.
        if station_waypoint is None:
            stargate_waypoint = pag.locateCenterOnScreen(
                './img/overview/stargate_waypoint.bmp',
                confidence=0.96,
                region=(originx, originy, windowx, windowy))
            print('warp_to_waypoint -- looking for waypoints...',
                  tries)
            time.sleep(float(random.randint(400, 1200)) / 1000)
            continue
        elif station_waypoint is not None:
            print(' warp_to_waypoint -- found station waypoint')
            (station_waypointx, station_waypointy) = station_waypoint
            pag.moveTo((station_waypointx + (random.randint(-8, 8))),
                       (station_waypointy + (random.randint(-8, 8))),
                       mouse.duration(), mouse.path())
            pag.keyDown('d')  # Warp hotkey.
            time.sleep(float(random.randint(600, 1200)) / 1000)
            mouse.click()
            pag.keyUp('d')
            # Move mouse away from overview to prevent tooltips from blocking
            # script from seeing the icons.
            pag.moveTo((random.randint(0, (windowy - 100))),
                       (random.randint(0, ((windowx - 100) / 2))),
                       mouse.duration(), mouse.path())
            return 2
    # Check if stargate waypoint was found before loop expired.
    if stargate_waypoint is not None and tries <= 15:
        print('warp_to_waypoint -- found stargate waypoint')
        (stargate_waypointx, stargate_waypointy) = stargate_waypoint
        pag.moveTo((stargate_waypointx + (random.randint(-8, 8))),
                   (stargate_waypointy + (random.randint(-8, 8))),
                   mouse.duration(), mouse.path())
        pag.keyDown('d')
        time.sleep(float(random.randint(600, 1200)) / 1000)
        mouse.click()
        pag.keyUp('d')
        pag.moveTo(
            (random.randint(150, (int(windowy - (windowy / 4))))),
            (random.randint(150, (int(windowx - (windowx / 4))))),
            mouse.duration(), mouse.path())
        return 1
    elif stargate_waypoint is None and tries > 15:
        print('warp_to_waypoint -- no waypoints found')
        emergency_terminate()
        traceback.print_stack()
        sys.exit()


def warp_to_specific_system_bookmark(gotosite):
    # Try warping to a specific bookmark in the current system
    # If the ship is already at the requested site, return function.
    global atsite
    if gotosite == atsite:
        print('warp_to_specific_system_bookmark -- already at bookmark',
              atsite)
        return 0
    else:
        specific_system_bookmark = pag.locateCenterOnScreen(
            ('./img/dest/at_dest' + (bookmark_dict[gotosite]) + '.bmp'),
            confidence=0.90, region=(originx, originy, windowx, windowy))
        while specific_system_bookmark is None:
            print('warp_to_specific_system_bookmark -- bookmark', gotosite,
                  'not found in system')
            return 0
        else:
            print('warp_to_specific_system_bookmark -- found bookmark',
                  gotosite)
            (specific_system_bookmarkx), (
                specific_system_bookmarky) = specific_system_bookmark
            pag.moveTo((specific_system_bookmarkx + (random.randint(-1, 200))),
                       (specific_system_bookmarky +
                        (random.randint(-3, 3))), mouse.duration(),
                       mouse.path())
            mouse.click_right()
            pag.moveRel((0 + (random.randint(10, 80))),
                        (0 + (random.randint(10, 15))),
                        mouse.duration(), mouse.path())
            mouse.click()
            time.sleep(2)
            return 1


def detect_warp():
    # Detect when a warp has been completed by waiting for the 'warping' text
    # to disappear from the spedometer. Wait for the ship to begin its warp
    # before checking though, otherwise the script will think the warp has
    # already been completed.
    print('detect_warp -- waiting for warp to complete')
    time.sleep(alignment_time)
    warp_duration = 1
    warp_drive_active = pag.locateCenterOnScreen(
        './img/indicators/warping.bmp',
        confidence=0.90,
        region=(originx, originy, windowx, windowy))
    while warp_drive_active is not None and warp_duration <= 300:
        print('detect_warp -- warping...')
        warp_duration += 1
        time.sleep(1)
        warp_drive_active = pag.locateCenterOnScreen(
            './img/indicators/warping.bmp',
            confidence=0.90,
            region=(originx, originy, windowx, windowy))
    if warp_drive_active is None and warp_duration <= 300:
        time.sleep(float(random.randint(1000, 3000)) / 1000)
        print('detect_warp warp completed')
        return 1
    else:
        print('detect_warp -- timed out waiting for warp')
        emergency_terminate()
        return 0


def detect_jump():
    # Detect a jump by looking for the cyan session-change icon in top left
    # corner of the eve client window. If a jump hasn't been detected after
    # 50 checks, check if the 'low security system warning' window has appeared
    # and is preventing the ship from jumping.
    tries = 0
    session_change_cloaked = pag.locateCenterOnScreen(
        './img/indicators/session_change_cloaked.bmp',
        # Confidence must be lower than normal since icon is partially
        # transparent.
        confidence=0.55, region=(originx, originy, windowx, windowy))

    while session_change_cloaked is None and tries <= 180:
        tries += 1
        print('detect_jump -- waiting for jump...', tries)
        time.sleep(1.5)
        session_change_cloaked = pag.locateCenterOnScreen(
            './img/indicators/session_change_cloaked.bmp',
            confidence=0.55,
            region=(originx, originy, windowx, windowy))

        if session_change_cloaked is not None and tries >= 50:
            low_sec_popup = pag.locateCenterOnScreen(
                './img/warnings/low_security_system.bmp',
                confidence=0.9,
                region=(originx, originy, windowx, windowy))

            if low_sec_popup is not None:
                keyboard.keypress('enter')
                continue
            else:
                continue

    if session_change_cloaked is not None and tries <= 180:
        print('detect_jump -- jump detected')
        time.sleep(float(random.randint(900, 2400)) / 1000)
        return 1

    else:
        print('detect_jump -- timed out looking for jump')
        emergency_terminate()
        traceback.print_stack()
        sys.exit()


def detect_dock():
    # Detect a station dock by looking for undock icon on the right half of the
    # eve client window.
    tries = 0
    docked = pag.locateCenterOnScreen('./img/buttons/undock.bmp',
                                      confidence=0.91,
                                      region=(originx, originy,
                                              windowx, windowy))
    while docked is None and tries <= 100:
        tries += 1
        print('detect_dock -- waiting for dock...', tries)
        time.sleep(3)
        docked = pag.locateCenterOnScreen('./img/buttons/undock.bmp',
                                          confidence=0.91,
                                          region=(originx, originy,
                                                  windowx, windowy))
    if docked is not None and tries <= 100:
        print('detect_dock -- detected dock')
        time.sleep(float(random.randint(2000, 5000)) / 1000)
        return 1
    else:
        print('detect_dock -- timed out looking for dock')
        emergency_terminate()
        traceback.print_stack()
        sys.exit()


def at_dest_num():
    # Determine if any bookmarks are green, indicating that bookmark is in the
    # ship's current system.
    global n
    n = 0
    # Confidence must be higher than normal because script frequently
    # mistakes dest3 for dest2.
    at_dest = pag.locateCenterOnScreen(
        ('./img/dest/at_dest' + (destnum[n]) + '.bmp'),
        confidence=0.98,
        region=(originx, originy, windowx, windowy))

    while at_dest is None:
        n += 1
        at_dest = pag.locateCenterOnScreen(
            ('./img/dest/at_dest' + (destnum[n]) + '.bmp'),
            confidence=0.98,
            region=(originx, originy, windowx, windowy))
        print('at_dest_num -- looking if at destination' + (destnum[n]))
        if n == 9 and at_dest is None:
            print('out of destinations to look for')
            return -1
    if at_dest is not None:
        print('at_dest_num -- at dest' + (destnum[n]))
        return n


def blacklist_station():
    # Blacklist the first green bookmark script identifies by editing its
    # bookmark name. This will prevent further trips to the blacklisted
    # station.
    at_dest = at_dest_num()
    if at_dest is not None:
        print('blacklist_station -- blacklisting station')
        at_dest = pag.locateCenterOnScreen(
            ('./img/dest/at_dest' + (destnum[n]) + '.bmp'),
            confidence=conf,
            region=(originx, originy, windowx, windowy))

        (at_destx), (at_desty) = at_dest
        pag.moveTo((at_destx + (random.randint(-1, 200))),
                   (at_desty + (random.randint(-3, 3))),
                   mouse.duration(), mouse.path())

        time.sleep(float(random.randint(1000, 2000)) / 1000)
        mouse.click()
        # Click once to focus entry, then double-click the entry to edit.
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
        # Add a 'b' to beginning of the name indicating site is blacklisted.
        pag.keyUp('b')
        time.sleep(float(random.randint(0, 1000)) / 1000)
        pag.keyDown('enter')
        time.sleep((random.randint(0, 200)) / 100)
        pag.keyUp('enter')
        return
    else:
        return


def blacklist_bookmark(atsite):
    # Blacklist a specific bookmark instead of the first green one the script
    # happens to see.
    print('blacklist_bookmark -- blacklisting bookmark')
    bookmark_to_blacklist = pag.locateCenterOnScreen(
        ('./img/dest/at_dest' + (bookmark_dict[atsite]) + '.bmp'),
        confidence=conf,
        region=(originx, originy, windowx, windowy))

    (bookmark_to_blacklistx), (bookkmark_to_blacklisty) = bookmark_to_blacklist
    pag.moveTo((bookmark_to_blacklistx + (random.randint(-1, 200))),
               (bookkmark_to_blacklisty + (random.randint(-3, 3))),
               mouse.duration(), mouse.path())

    time.sleep(float(random.randint(1000, 2000)) / 1000)
    mouse.click()
    time.sleep(float(random.randint(1000, 2000)) / 1000)
    mouse.click()
    time.sleep(float(random.randint(5, 50)) / 1000)
    mouse.click()
    time.sleep(float(random.randint(3000, 4000)) / 1000)
    keyboard.keypress('home')
    keyboard.keypress('b')
    time.sleep(float(random.randint(0, 1000)) / 1000)
    keyboard.keypress('enter')
    return 1

def emergency_terminate():
    # If a function breaks or times out while undocked, look for nearest
    # station and dock immediately. Incrementally lower the confidence required
    # to match station icon each time the loop runs. If a station cannot be
    # found after 20 loops, warp to the nearest celestial body at 100+ km
    # instead and immediately force an unsafe logout in space.
    print('emergency_terminate -- emergency termination called!')
    tries = 1
    confidence = 0.99
    station_icon = pag.locateCenterOnScreen('./img/overview/station.bmp',
                                            confidence=confidence,
                                            region=(originx, originy,
                                                    windowx, windowy))
    while station_icon is None and tries <= 25:
        print(
            'emergency_terminate -- looking for station to emergency dock at')
        tries += 1
        confidence -= 0.01
        station_icon = pag.locateCenterOnScreen('./img/station_icon.bmp',
                                                confidence=confidence,
                                                region=(originx, originy,
                                                        windowx, windowy))
    if station_icon is not None and tries <= 25:
        print('emergency_terminate -- emergency docking')
        (station_iconx, station_icony) = station_icon
        pag.moveTo((station_iconx + (random.randint(-2, 50))),
                   (station_icony + (random.randint(-2, 2))),
                   mouse.duration(), mouse.path())
        mouse.click()
        time.sleep(float(random.randint(600, 1200)) / 1000)
        pag.keyDown('d')
        time.sleep(float(random.randint(600, 1200)) / 1000)
        pag.keyUp('d')
        pag.moveTo(
            (random.randint(150, (int(windowy - (windowy / 4))))),
            (random.randint(150, (int(windowx - (windowx / 4))))),
            mouse.duration(), mouse.path())
        detect_dock()
        emergency_logout()
        return 1
    else:
        print(
            "emergency_terminate -- couldn't find station to emergency dock "
            "at, warping to celestial instead")
        tries = 0
        confidence = 0.99
        celestial_icon = pag.locateCenterOnScreen(
            './img/overview/celestial.bmp',
            confidence=confidence,
            region=(originx, originy, windowx, windowy))
        while celestial_icon is None and tries <= 50:
            print('emergency_terminate -- looking for celestial')
            tries += 1
            confidence -= 0.01
            celestial_icon = pag.locateCenterOnScreen(
                './img/overview/celestial_icon.bmp',
                confidence=confidence,
                region=(originx, originy, windowx, windowy))
        if celestial_icon is not None and tries <= 50:
            print('emergency_terminate -- emergency warping to celestial')
            (celestial_iconx, celestial_icony) = celestial_icon
            pag.moveTo((celestial_iconx + (random.randint(-2, 50))),
                       (celestial_icony + (random.randint(-2, 2))),
                       mouse.duration(), mouse.path())
            mouse.click()
            time.sleep(float(random.randint(600, 1200)) / 1000)
            pag.keyDown('w')
            time.sleep(float(random.randint(600, 1200)) / 1000)
            pag.keyUp('w')
            pag.moveTo((random.randint(150, (
                int(windowy - (windowy / 4))))),
                       (random.randint(150, (
                           int(windowx - (windowx / 4))))),
                       mouse.duration(), mouse.path())
            detect_warp()
            emergency_logout()
        else:
            print('emergency_terminate -- out of celestials to look for')
            emergency_logout()
        return 0

def emergency_logout():
    # use hotkey to forcefully kill client session, don't use the 'log off
    # safely' feature
    return


'''
##### old functions #####

def warp_to_first_bookmark_in_system():
    # warp to lowest-numbered bookmark in the system higher than 0
    # bookmark names must be preceded with a 1-digit number higher than 0 (
    # ex: 1spot_in_system_A)
    # bookmark 0 is the home station
    bnum = 1
    global defined_bookmark_in_system
    # check if bookmark 1 is in the current system. if so, warp to it. if
    # not, increment by 1 and try again
    defined_bookmark_in_system = pag.locateCenterOnScreen(
        ('./img/dest/at_dest' + (bookmark_dict[bnum]) + '.bmp'),
        confidence = 0.90,
        region = (originx, originy, windowx, windowy))
    while defined_bookmark_in_system is None:
        bnum += 1
        defined_bookmark_in_system = pag.locateCenterOnScreen(
            ('./img/dest/at_dest' + (bookmark_dict[bnum]) + '.bmp'),
            confidence = 0.90,
            region = (originx, originy, windowx, windowy))
        if bnum == 9 and defined_bookmark_in_system is None:
            print(
                'warp_to_first_bookmark_in_system -- out of bookmarks in '
                'system to look for')
            return 0
    if defined_bookmark_in_system is not None:
        print('warp_to_first_bookmark_in_system -- found bookmark' + (
            bookmark_dict[bnum]))
        (bookmark_in_systemx), (
            bookmark_in_systemy) = defined_bookmark_in_system
        pag.moveTo((bookmark_in_systemx + (random.randint(-1, 200))),
                   (bookmark_in_systemy +
                    (random.randint(-3, 3))), mouse.duration(),
                   mouse.path())
        mouse.click_right()
        pag.moveRel((0 + (random.randint(10, 80))),
                    (0 + (random.randint(20, 25))),
                    mouse.duration(), mouse.path())
        mouse.click()
        time.sleep(2)
        return 1


def detect_warp_to_bookmark_in_system():
	# detect when warp to a bookmark has been completed to a bookmark by 
	checking if the bookmark's right-click
	# menu still has a 'warp to' option. if the option is not present, 
	ship has arrived at bookmark
	(defined_bookmark_in_systemx), (defined_bookmark_in_systemy) = 
	defined_bookmark_in_system
	tries = 0
	pag.moveTo((defined_bookmark_in_systemx + (random.randint(-1, 200))), 
	(defined_bookmark_in_systemy +
												(random.randint(-3, 3))), 
												mouse.duration(), 
												mouse.path())
	mouse.click_right()
	print('detect_warp_to_bookmark_in_system -- waiting for warp')
	at_bookmark_in_system = pag.locateCenterOnScreen(
	'./img/detect_warp_to_bookmark.bmp',
													confidence=0.85,
													region=(originx, originy, 
													screenwidth, 
													screenheight))
	while at_bookmark_in_system is None and tries <= 50:
		time.sleep(float(random.randint(1000, 3000)) / 1000)
		focus_overview()
		time.sleep(float(random.randint(5000, 10000)) / 1000)
		warp_to_bookmark_tries += 1
		pag.moveTo((defined_bookmark_in_systemx + (random.randint(-1, 200))), 
		(defined_bookmark_in_systemy +
										(random.randint(-3, 3))), 
										mouse.duration(), mouse.path())
		mouse.click_right()
		at_bookmark_in_system = pag.locateCenterOnScreen(
		'./img/detect_warp_to_bookmark.bmp',
														 confidence=0.98,
														 region=(originx, 
														 originy, 
														 halfscreenwidth, 
														 screenheight))
	if at_bookmark_in_system is None and warp_to_bookmark_tries >= 50:
		emergency_terminate()
		return 0
	if at_bookmark_in_system is not None and warp_to_bookmark_tries < 50:
		print('detect_warp_to_bookmark_in_system -- warp completed')
		return 1

'''
