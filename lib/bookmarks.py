import random
import time

import pyautogui as pag

from lib import mouse, keyboard, navigation as nav
from lib.navigation import detect_dock_loop
from lib.vars import originx, originy, windowx, windowy, conf

destnum = {0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7",
           8: "8", 9: "9", 10: "10"}
bookmark_dict = {1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7",
                 8: "8", 9: "9", 10: "10"}


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


def detect_at_home():
    # Check if the ship is at its home station by looking for a bookmark
    # starting with '000'.
    at_home_check_var = pag.locateCenterOnScreen('./img/dest/at_dest0.bmp',
                                                 confidence=conf,
                                                 region=(originx, originy,
                                                         windowx, windowy))
    if at_home_check_var is None:
        return 0
    elif at_home_check_var is not None:
        print('nav.detect_at_home -- at home station')
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
        detect_dock_loop()


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
        print('detect_bookmark_location -- looking if at destination'
              + (destnum[n]))
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


def blacklist_local_bookmark():
    # Determine which bookmark ship is at by looking at the right-click
    # menu. If a bookmark is on grid with the user's ship, blacklist the
    # bookmark by editing its name.
    print('blacklist_local_bookmark -- called')

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

            # Right-click on bookmark to check if an 'approach location'
            # option is available. If it is, blacklist bookmark. If it
            # isn't, try another bookmark.
            time.sleep(float(random.randint(1000, 2000)) / 1000)
            mouse.click_right()
            time.sleep(float(random.randint(1000, 2000)) / 1000)

            at_bookmark = pag.locateCenterOnScreen(
                './img/buttons/detect_warp_to_bookmark.bmp',
                confidence=0.90,
                region=(originx, originy, windowx, windowy))

            # If 'approach location' is present, blacklist that bookmark.
            if at_bookmark is not None:
                print('blacklist_local_bookmark -- blacklisting bookmark',
                      bookmark)
                time.sleep(float(random.randint(1000, 2000)) / 1000)
                keyboard.keypress('esc')
                mouse.click()
                # Click once to focus entry, then double-click the entry to
                # edit.
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
                # Add a 'b' to beginning of the name indicating site
                # is blacklisted.
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
                    'blacklist_local_bookmark -- not at bookmark', bookmark)
                keyboard.keypress('esc')
                bookmark += 1
                continue

        elif bookmark_to_blacklist is None:
            print('blacklist_local_bookmark -- out of bookmarks to look for')
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


def travel_to_bookmark(target_bookmark):
    # Find a suitable asteroid field by warping to each bookmark in
    # numerical order.
    # Currently only mining in a single system with at least one station is
    # supported

    # Try warping to bookmark 1 in the system. If bookmark 1 doesn't exist,
    # is not in the current system, or your ship is already there. Increment
    # bookmark number by 1 and try again.
    travel_to_bookmark_var = warp_to_local_bookmark(
        target_bookmark)
    while travel_to_bookmark_var == 0 and target_bookmark <= 10:
        target_bookmark += 1
        travel_to_bookmark_var = warp_to_local_bookmark(
            target_bookmark)
        continue
    if travel_to_bookmark_var == 1 and target_bookmark <= 10:
        # Once a valid site is found, remember the site number the ship is
        # warping to so script doesn't try warping there again.
        if nav.detect_warp_loop() == 1:
            return 1
    else:
        print('travel_to_bookmark -- ran out of sites to check for')
        return 0
