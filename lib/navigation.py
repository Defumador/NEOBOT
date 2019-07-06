import sys, time, random, traceback
import pyautogui as pag
from lib import mouse, keyboard
from lib.vars import originx, originy, windowx, windowy, conf, system_mining

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
    route_set_var = pag.locateCenterOnScreen('./img/indicators/route_set.bmp',
                                             confidence=0.85,
                                             region=(originx, originy,
                                                     windowx, windowy))
    if route_set_var is None:
        print('nav.route_set -- no route set!')
        sys.exit(0)
    else:
        return


def set_dest():
    # Issue a 'set destination' command for the lowest-numbered bookmark that
    # isn't blacklisted (starting with 1).
    set_dest_var = pag.locateCenterOnScreen(
        ('./img/dest/dest' + (destnum[1]) + '.bmp'),
        confidence=0.98,
        region=(originx, originy, windowx, windowy))

    target_dest = 1
    while set_dest_var is None:
        target_dest += 1
        set_dest_var = pag.locateCenterOnScreen(
            ('./img/dest/dest' + (destnum[target_dest]) + '.bmp'),
            confidence=0.98,
            region=(originx, originy, windowx, windowy))
        print('nav.set_dest -- looking for dest' + (destnum[target_dest]))

    if set_dest_var is not None:
        print('nav.set_dest -- setting destination waypoint')
        (next_destx), (next_desty) = set_dest_var
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
    at_home_check_var = pag.locateCenterOnScreen('./img/dest/at_dest0.bmp',
                                                 confidence=conf,
                                                 region=(originx, originy,
                                                         windowx, windowy))
    if at_home_check_var is None:
        return 0
    elif at_home_check_var is not None:
        print('nav.at_home_check -- at home station')
        return 1


def set_home():
    # Set destination as the bookmark beginning with '000'.
    print('nav.set_home -- setting home waypoint')
    set_home_var = pag.locateCenterOnScreen('./img/dest/dest0.bmp',
                                            confidence=conf,
                                            region=(originx, originy,
                                                    windowx, windowy))
    if set_home_var is not None:
        (homex, homey) = set_home_var
        pag.moveTo((homex + (random.randint(-1, 200))),
                   (homey + (random.randint(-3, 3))),
                   mouse.duration(), mouse.path())
        mouse.click_right()
        pag.moveRel((0 + (random.randint(10, 80))),
                    (0 + (random.randint(20, 25))),
                    mouse.duration(), mouse.path())
        mouse.click()
        return 1
    else:
        print("set_home -- couldn't find home waypoint")
        return 0

    # !! needs work to transition to windowx,windowy


def focus_overview():
    # Click on the overview window to focus the eve client window.
    print('nav.focus_overview -- called')
    pag.moveTo((windowx - (random.randint(10, 90))),
               (75 + (random.randint(0, (windowy - 10)))),
               mouse.duration(), mouse.path())
    time.sleep(float(random.randint(50, 500)) / 1000)
    mouse.click()
    return 1


def warp_to_waypoint():
    # Click on the current waypoint and use warp hotkey to warp to waypoint.
    # Currently supports warping to stargate and station waypoints.
    print('nav.warp_to_waypoint -- looking for waypoints')
    tries = 0
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
            print('nav.warp_to_waypoint -- looking for waypoints...',
                  tries)
            time.sleep(float(random.randint(400, 1200)) / 1000)
            continue
        elif station_waypoint is not None:
            print('nav.warp_to_waypoint -- found station waypoint')
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
        print('nav.warp_to_waypoint -- found stargate waypoint')
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
        print('nav.warp_to_waypoint -- no waypoints found')
        emergency_terminate()
        traceback.print_stack()
        sys.exit()

"""
# FROM MINING
def travel_to_bookmark(target_bookmark):
    # Find a suitable asteroid field by warping to each bookmark in
    # numerical order.
    # Currently only mining in a single system with at least one station is
    # supported

    # Try warping to bookmark 1 in the system. If bookmark 1 doesn't exist,
    # is not in the current system, or your ship is already there. Increment
    # bookmark number by 1 and try again.
    travel_to_bookmark_var = nav.warp_to_local_bookmark(
        target_bookmark)
    while travel_to_bookmark_var == 0 and target_bookmark <= 10:
        target_bookmark += 1
        travel_to_bookmark_var = nav.warp_to_local_bookmark(
            target_bookmark)
        continue
    if travel_to_bookmark_var == 1 and target_bookmark <= 10:
        # Once a valid site is found, remember the site number the ship is
        # warping to so script doesn't try warping there again.
        if nav.detect_warp() == 1:
            return 1
    else:
        print('nav.travel_to_bookmark -- ran out of sites to check for')
        return 0
"""

def warp_to_local_bookmark(target_site):
    # Try warping to a specific bookmark in the current system.
    # If the ship is already at the requested site, return function.
    # Confidence must be >0.95 because script will confuse 6 with 0
    specific_system_bookmark = pag.locateCenterOnScreen(
        ('./img/dest/at_dest' + (bookmark_dict[target_site]) + '.bmp'),
        confidence=0.98,
        region=(originx, originy, windowx, windowy))
    (specific_system_bookmarkx, specific_system_bookmarky) = \
        specific_system_bookmark

    # If the target site has been found, right click on the target to see if
    # the 'approach location' option is there. If so, return function
    # because ship is already at that location. If the option is not there,
    # check for a 'warp to' option, if it's present, warp to location.
    if specific_system_bookmark is not None:
        pag.moveTo((specific_system_bookmarkx + (random.randint(10, 200))),
                   (specific_system_bookmarky + (random.randint(-3, 3))),
                   mouse.duration(), mouse.path())
        mouse.click_right()

        at_target_site = pag.locateCenterOnScreen(
            './img/buttons/detect_warp_to_bookmark.bmp',
            confidence=0.90, region=(originx, originy, windowx, windowy))

        if at_target_site is not None:
            print('nav.warp_to_local_bookmark -- already at bookmark',
                  target_site)
            keyboard.keypress('esc')  # Close right-click menu.
            return 0

        elif at_target_site is None:
            warp_to_target = pag.locateCenterOnScreen(
                './img/buttons/warp_to_bookmark.bmp',
                confidence=0.90, region=(originx, originy, windowx, windowy))

            if warp_to_target is not None:
                print('nav.warp_to_local_bookmark -- warping to '
                      'bookmark', target_site)
                pag.moveRel((0 + (random.randint(10, 80))),
                            (0 + (random.randint(10, 15))),
                            mouse.duration(), mouse.path())
                mouse.click()
                time.sleep(2)
                return 1
            else:
                print('nav.warp_to_local_bookmark -- error')
                return 0


def dock_at_local_bookmark():
    # Dock at the first bookmark beginning with a '0'
    dock_at_station_bookmark_var = pag.locateCenterOnScreen(
        './img/dest/at_dest0.bmp',
        confidence=conf,
        region=(originx, originy,
                windowx, windowy))
    if dock_at_station_bookmark_var is not None:
        (homex, homey) = dock_at_station_bookmark_var
        pag.moveTo((homex + (random.randint(-1, 200))),
                   (homey + (random.randint(-3, 3))),
                   mouse.duration(), mouse.path())
        mouse.click_right()

        pag.moveRel((0 + (random.randint(10, 80))),
                    (0 + (random.randint(35, 40))),
                    mouse.duration(), mouse.path())
        mouse.click()
        detect_dock()


def detect_warp():
    # Detect when a warp has been completed by waiting for the 'warping' text
    # to disappear from the spedometer. Wait for the ship to begin its warp
    # before checking though, otherwise the script will think the warp has
    # already been completed.
    warp_duration = 1
    warp_drive_active = pag.locateCenterOnScreen(
        './img/indicators/warping.bmp',
        confidence=0.95,
        region=(originx, originy, windowx,
                windowy))

    # Wait for warp to begin by waiting until the spedometer is full. Ship
    # might be stuck on something so this could take an variable amount of
    # time.
    while warp_drive_active is None and warp_duration <= 300:
        print('nav.detect_warp -- waiting for warp to start...',
              warp_duration)
        time.sleep(float(random.randint(1000, 3000)) / 1000)
        warp_duration += 1
        warp_drive_active = pag.locateCenterOnScreen(
            './img/indicators/warping.bmp',
            confidence=0.95,
            region=(originx, originy, windowx,
                    windowy))

    # Wait up to 300 seconds before concluding there was an error with the
    # function.
    while warp_drive_active is not None and warp_duration <= 150:
        print('warp icon found at', warp_drive_active)
        print('nav.detect_warp -- warping...', warp_duration)
        warp_duration += 1
        time.sleep(2)
        warp_drive_active = pag.locateCenterOnScreen(
            './img/indicators/warping.bmp',
            confidence=0.95,
            region=(originx, originy, windowx,
                    windowy))

    if warp_drive_active is None and warp_duration <= 150:
        time.sleep(float(random.randint(1000, 3000)) / 1000)
        print('nav.detect_warp -- warp completed')
        return 1
    else:
        print('nav.detect_warp -- timed out waiting for warp')
        emergency_terminate()
        return 0


def detect_jump():
    # Detect a jump by looking for the cyan session-change icon in top left
    # corner of the eve client window. If a jump hasn't been detected after
    # 50 checks, check if the 'low security system warning' window has appeared
    # and is preventing the ship from jumping.
    tries = 0
    detect_jump_var = pag.locateCenterOnScreen(
        './img/indicators/session_change_cloaked.bmp',
        # Confidence must be lower than normal since icon is partially
        # transparent.
        confidence=0.55, region=(originx, originy, windowx, windowy))

    while detect_jump_var is None and tries <= 180:
        tries += 1
        print('nav.detect_jump -- waiting for jump...', tries)
        time.sleep(1.5)
        detect_jump_var = pag.locateCenterOnScreen(
            './img/indicators/session_change_cloaked.bmp',
            confidence=0.55,
            region=(originx, originy, windowx, windowy))

        if detect_jump_var is not None and tries >= 50:
            low_sec_popup = pag.locateCenterOnScreen(
                './img/warnings/low_security_system.bmp',
                confidence=0.9,
                region=(originx, originy, windowx, windowy))

            if low_sec_popup is not None:
                keyboard.keypress('enter')
                continue
            else:
                continue

    if detect_jump_var is not None and tries <= 180:
        print('nav.detect_jump -- jump detected')
        time.sleep(float(random.randint(900, 2400)) / 1000)
        return 1

    else:
        print('nav.detect_jump -- timed out looking for jump')
        emergency_terminate()
        traceback.print_stack()
        sys.exit()


def detect_dock():
    # Detect a station dock by looking for undock icon on the right half of the
    # eve client window.
    tries = 0
    detect_dock_var = pag.locateCenterOnScreen('./img/buttons/undock.bmp',
                                               confidence=0.91,
                                               region=(originx, originy,
                                                       windowx, windowy))
    while detect_dock_var is None and tries <= 100:
        tries += 1
        print('nav.detect_dock -- waiting for dock...', tries)
        time.sleep(3)
        detect_dock_var = pag.locateCenterOnScreen('./img/buttons/undock.bmp',
                                                   confidence=0.91,
                                                   region=(originx, originy,
                                                           windowx, windowy))
    if detect_dock_var is not None and tries <= 100:
        print('nav.detect_dock -- detected dock')
        time.sleep(float(random.randint(2000, 5000)) / 1000)
        return 1
    else:
        print('nav.detect_dock -- timed out looking for dock')
        emergency_terminate()
        traceback.print_stack()
        sys.exit()


def detect_bookmark_location():
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
        print('detect_bookmark_location -- looking if at destination' + (destnum[n]))
        if n == 9 and at_dest is None:
            print('out of destinations to look for')
            return -1
    if at_dest is not None:
        print('detect_bookmark_location -- at dest' + (destnum[n]))
        return n


def blacklist_station():
    # Blacklist the first green bookmark script identifies by editing its
    # bookmark name. This will prevent further trips to the blacklisted
    # station.
    at_dest = detect_bookmark_location()
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


def blacklist_current_bookmark():
    # Determine which bookmark ship is at by looking at the right-click
    # menu. If a bookmark is on grid with the user's ship, blacklist the
    # bookmark by editing its name.
    print('blacklist_current_bookmark -- called')

    # First check to see if the bookmark even exists.
    bookmark = 1
    bookmark_to_blacklist = pag.locateCenterOnScreen(
        ('./img/dest/at_dest' + (bookmark_dict[bookmark]) + '.bmp'),
        confidence=0.95,
        region=(originx, originy, windowx, windowy))

    # If bookmark exists, check right-click menu .
    while bookmark_to_blacklist is not None:

        bookmark_to_blacklist = pag.locateCenterOnScreen(
            ('./img/dest/at_dest' + (bookmark_dict[bookmark]) + '.bmp'),
            confidence=0.95,
            region=(originx, originy, windowx, windowy))

        if bookmark_to_blacklist is not None:

            (bookmark_to_blacklistx), (
                bookkmark_to_blacklisty) = bookmark_to_blacklist
            pag.moveTo((bookmark_to_blacklistx + (random.randint(-1, 200))),
                       (bookkmark_to_blacklisty + (random.randint(-3, 3))),
                       mouse.duration(), mouse.path())

            # Right-click on bookmark to check if an 'approach location' option is
            # available. If it is, blacklist bookmark. If it isn't, try another
            # bookmark.
            time.sleep(float(random.randint(1000, 2000)) / 1000)
            mouse.click_right()
            time.sleep(float(random.randint(1000, 2000)) / 1000)

            at_bookmark = pag.locateCenterOnScreen(
                './img/buttons/detect_warp_to_bookmark.bmp',
                confidence=0.90,
                region=(originx, originy, windowx, windowy))

            # If 'approach location' is present, blacklist that bookmark.
            if at_bookmark is not None:
                print('blacklist_current_bookmark -- blacklisting bookmark',
                      bookmark)
                time.sleep(float(random.randint(1000, 2000)) / 1000)
                keyboard.keypress('esc')
                mouse.click()
                # Click once to focus entry, then double-click the entry to edit.
                time.sleep(float(random.randint(1000, 2000)) / 1000)
                mouse.click()
                time.sleep(float(random.randint(50, 100)) / 1000)
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
                return 1

            # If 'approach location' is not present, 
            # close the right-click menu and check the next bookmark
            if at_bookmark is None:
                print(
                    'blacklist_current_bookmark -- not at bookmark', bookmark)
                keyboard.keypress('esc')
                bookmark += 1
                continue

        elif bookmark_to_blacklist is None:
            print('blacklist_current_bookmark -- out of bookmarks to look for')
            return 0


def blacklist_specific_bookmark(target_site):
    # Blacklist a specific bookmark by changing its name.
    print('blacklist_specific_bookmark -- blacklisting bookmark', target_site)
    bookmark_to_blacklist = pag.locateCenterOnScreen(
        ('./img/dest/at_dest' + (bookmark_dict[target_site]) + '.bmp'),
        confidence=conf,
        region=(originx, originy, windowx, windowy))

    (bookmark_to_blacklistx), (bookmark_to_blacklisty) = bookmark_to_blacklist
    pag.moveTo((bookmark_to_blacklistx + (random.randint(-1, 200))),
               (bookmark_to_blacklisty + (random.randint(-3, 3))),
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
    # If a function breaks or times out while undocked, look for the nearest
    # station and dock immediately. Incrementally lower the confidence required
    # to match station icon each time the loop runs in order to guarantee a warp.
    # If a station cannot be found after 20 loops,
    # warp to the nearest celestial body and keep at a distance of >100 km. 
    # After warp completes, force an unsafe logout in space.
    print('!!! nav.emergency_terminate -- EMERGENCY TERMINATE CALLED !!!')
    tries = 0
    confidence = 0.99
    station_icon = pag.locateCenterOnScreen('./img/overview/station.bmp',
                                            confidence=confidence,
                                            region=(originx, originy,
                                                    windowx, windowy))
           
    # Look for a station to dock at until confidence is <0.85
    while station_icon is None and tries <= 15:
        print('!!! nav.emergency_terminate -- looking for station to dock at,'
            'confidence =',confidence)
        tries += 1
        time.sleep(float(random.randint(600, 1200)) / 1000)
        station_icon = pag.locateCenterOnScreen('./img/station_icon.bmp',
                                                confidence=confidence,
                                                region=(originx, originy,
                                                        windowx, windowy))
    if station_icon is not None and tries <= 15:
        print('!!! nav.emergency_terminate -- emergency docking')
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
        # Don't even try to detect a dock, since ship may have warped
        # to a non-station object by mistake
        time.sleep(float(random.randint(60000, 120000)) / 1000)
        emergency_logout()
        return 0

    # If confidence lowers below threshold, try warping to a planet or moon
    # instead.
    else:
        print(
            "!!! nav.emergency_terminate -- couldn't find station to emergency dock "
            "at, warping to celestial body instead")
        tries = 0
        confidence = 0.99
        celestial_icon = pag.locateCenterOnScreen(
            './img/overview/celestial.bmp',
            confidence=confidence,
            region=(originx, originy, windowx, windowy))
        while celestial_icon is None and tries <= 50:
            print('!!! nav.emergency_terminate -- looking for celestial body')
            tries += 1
            confidence -= 0.01
            time.sleep(float(random.randint(600, 1200)) / 1000)
            celestial_icon = pag.locateCenterOnScreen(
                './img/overview/celestial_icon.bmp',
                confidence=confidence,
                region=(originx, originy, windowx, windowy))
           
        if celestial_icon is not None and tries <= 50:
            print('!!! nav.emergency_terminate -- emergency warping to celestial body')
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
            return 0
        else:
            print('!!! nav.emergency_terminate -- out of celestial bodies to look for')
            emergency_logout()
        return 1


def emergency_logout():
    # use hotkey to forcefully kill client session, don't use the 'log off
    # safely' feature
    # ALT SHIFT Q
    print("!!! nav.emergency_logout -- called")
    time.sleep(float(random.randint(1000, 5000)) / 1000)
    pag.keyDown('alt')
    time.sleep(float(random.randint(500, 1000)) / 1000)
    pag.keyDown('shift')
    time.sleep(float(random.randint(500, 1000)) / 1000)
    pag.keyDown('q')
    time.sleep(float(random.randint(300, 1000)) / 1000)
    pag.keyUp('alt')
    time.sleep(float(random.randint(300, 1000)) / 1000)
    pag.keyUp('shift')
    time.sleep(float(random.randint(300, 1000)) / 1000)
    pag.keyUp('q')
    return 0


"""
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
        confidence=0.90,
        region=(originx, originy, windowx, windowy))
    while defined_bookmark_in_system is None:
        bnum += 1
        defined_bookmark_in_system = pag.locateCenterOnScreen(
            ('./img/dest/at_dest' + (bookmark_dict[bnum]) + '.bmp'),
            confidence=0.90,
            region=(originx, originy, windowx, windowy))
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
    checking if the
    bookmark
    's right-click
    # menu still has a 'warp to' option. if the option is not present, 
    ship
    has
    arrived
    at
    bookmark
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
        
        
# OLD WARP TP BOOKMARK FUNC
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
"""
