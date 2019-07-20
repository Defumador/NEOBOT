import random
import sys
import time
import logging

import pyautogui as pag

from src import mouse, keyboard, navigation as nav, locate as lo
from src.navigation import wait_for_dock
from src.vars import originx, originy, windowx, windowy, conf

logging.basicConfig(format='(%(levelno)s) %(asctime)s - %(funcName)s -- %('
                           'message)s', level=logging.DEBUG)

def set_dest():
    """Issue a 'set destination' command for the lowest-numbered bookmark that
    isn't blacklisted (starting with 1)."""
    target_dest = 1
    dest = lo.clocate('./img/dest/dest' + (str(target_dest)) + '.bmp', conf=0.98)

    while dest is None:
        target_dest += 1
        logging.debug('looking for dest ' + (str(target_dest)))
        dest = lo.clocate('./img/dest/dest' + (str(target_dest)) + '.bmp', conf=0.98)

    if dest is not None:
        logging.debug('setting destination waypoint')
        (x, y) = dest
        pag.moveTo((x + (random.randint(-1, 200))),
                   (y + (random.randint(-3, 3))),
                   mouse.duration(), mouse.path())
        mouse.click_right()
        pag.moveRel((0 + (random.randint(10, 80))),
                    (0 + (random.randint(20, 25))),
                    mouse.duration(), mouse.path())
        mouse.click()
        time.sleep(float(random.randint(1000, 2000)) / 1000)
        return


def is_home():
    """Check if the ship is at its home station by looking for a bookmark
    starting with '000'."""
    if lo.locate('./img/dest/at_dest0.bmp') is None:
        logging.debug('not at home station')
        return 0
    elif lo.locate('./img/dest/at_dest0.bmp') is not None:
        logging.debug('at home station')
        return 1


def set_home():
    """Set destination as the bookmark beginning with '000'."""
    home = lo.clocate('./img/dest/dest0.bmp')
    if home is not None:
        logging.debug('setting home waypoint')
        (x, y) = home
        pag.moveTo((x + (random.randint(-1, 200))),
                   (y + (random.randint(-3, 3))),
                   mouse.duration(), mouse.path())
        mouse.click_right()
        pag.moveRel((0 + (random.randint(10, 80))),
                    (0 + (random.randint(20, 25))),
                    mouse.duration(), mouse.path())
        mouse.click()
        return 1
    else:
        logging.error('could not find home waypoint!')
        return 0

    
def travel_to_bookmark(target_site_num):
    # TODO: rename to 'iterate_through_bookmarks' or something
    """Tries warping to the provided bookmark. If not possible, warps
    to the next numerical bookmark up.

    Ex: try warping to bookmark X in the system. If bookmark X doesn't exist,
    is not in the current system, or your ship is already there. Increment
    bookmark number by 1 and try again."""
    warping_to_bookmark = warp_to_local_bookmark(target_site_num)
    # logging.debug('warping_to_bookmark is ' + (str(warping_to_bookmark)))

    while warping_to_bookmark == 0 and target_site_num <= 10:
        target_site_num += 1
        warping_to_bookmark = warp_to_local_bookmark(target_site_num)
        # logging.debug('warping_to_bookmark is now ' + (str(
        #    warping_to_bookmark)))

        # TODO: change the '10' constant to equal total number of bookmarks set
    if warping_to_bookmark == 1 and target_site_num <= 10:
        # Once a valid site is found, remember the site number the ship is
        # warping to so script doesn't try warping there again.
        if nav.wait_for_warp_to_complete() == 1:
            return 1
    elif warping_to_bookmark == 0 and target_site_num > 10:
        logging.warning('ran out of sites to check for')
        return 0
   

def warp_to_local_bookmark(target_site_num):
    """Tries warping to the provided bookmark, assuming the bookmark
    is in the current system. If the ship is already at the
    requested site, return the function."""
    # Confidence must be >0.95 because script will confuse 6 with 0.
    target_site_bookmark = lo.clocate('./img/dest/at_dest' + (str(target_site_num)) + '.bmp', conf=0.98)
   
    # If the target site has been found, right click on the target to see if
    # the 'approach location' option is there. If so, return function
    # because ship is already at that location. If the option is not there,
    # check for a 'warp to' option, if it's present, warp to location.
    if target_site_bookmark is not None:
        (x, y) = target_site_bookmark
        pag.moveTo((x + (random.randint(10, 200))),
                   (y + (random.randint(-3, 3))),
                   mouse.duration(), mouse.path())
        mouse.click_right()
        approach_location = lo.locate(
            './img/buttons/detect_warp_to_bookmark.bmp', conf=0.90)

        # If the 'approach location' option is found, return function.
        if approach_location is not None:
            logging.debug('already at bookmark ' + (str(target_site_bookmark)))
            keyboard.keypress('esc')  # Close right-click menu.
            return 0

        # Otherwise, warp to location.
        elif approach_location is None:
            warp_to_site = lo.clocate('./img/buttons/warp_to_bookmark.bmp', conf=0.90)

            if warp_to_site is not None:
                logging.info(
                    'warping to bookmark ' + (str(target_site_bookmark)))
                pag.moveRel((0 + (random.randint(10, 80))),
                            (0 + (random.randint(10, 15))),
                            mouse.duration(), mouse.path())
                mouse.click()
                time.sleep(float(random.randint(1500, 1800)) / 1000)
                return 1
            elif warp_to_site is None:
                logging.error('unable to warp to target site, is ship docked?')
                return 0


def dock_at_local_bookmark():
    """Dock at the first bookmark beginning with a '0' in its name, assuming it's
    in the same system as you."""
    dock = lo.clocate('./img/dest/at_dest0.bmp')
    if dock is not None:
        (x, y) = dock
        pag.moveTo((x + (random.randint(-1, 200))),
                   (y + (random.randint(-3, 3))),
                   mouse.duration(), mouse.path())
        mouse.click_right()

        pag.moveRel((0 + (random.randint(10, 80))),
                    (0 + (random.randint(35, 40))),
                    mouse.duration(), mouse.path())
        # Sleep used to fix possible bug in which script doesn't
        # clock on 'dock' after opening right-click menu.
        # (see video 2019-07-06_13-26-14 at 33m50s for bug).
        time.sleep(float(random.randint(500, 800)) / 1000)
        mouse.click()
        wait_for_dock()


def detect_bookmark_location():
    """Determine if any bookmarks are green, indicating that bookmark is in the
    ship's current system."""
    global n
    n = 0
    # Confidence must be higher than normal because script frequently
    # mistakes dest3 for dest2.
    at_dest = lo.locate('./img/dest/at_dest' + (str(n)) + '.bmp', conf=0.98)

    while at_dest is None:
        n += 1
        logging.debug('looking if at destination ' + (str(n)))
        at_dest = lo.locate('./img/dest/at_dest' + (str(n)) + '.bmp', conf=0.98)
           
        if n == 9 and at_dest is None:
            print('out of destinations to look for')
            return -1
    if at_dest is not None:
        logging.debug('at dest ' + (str(n)))
        return n


def blacklist_station():
    """Blacklist the first green bookmark script identifies by editing its
    bookmark name. This will prevent further trips to the blacklisted
    station."""
    at_dest = detect_bookmark_location()
    if at_dest is not None:
        logging.debug('blacklisting station')
        at_dest = pag.locateCenterOnScreen(
            ('./img/dest/at_dest' + (str(n)) + '.bmp'),
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
    """Determine which bookmark ship is at by looking at the right-click
    menu. If a bookmark is on grid with the user's ship, blacklist the
    bookmark by editing its name."""
    logging.debug('blacklisting local bookmark')

    # First check to see if the bookmark even exists.
    bookmark = 1
    bookmark_to_blacklist = pag.locateCenterOnScreen(
        ('./img/dest/at_dest' + (str(bookmark)) + '.bmp'),
        confidence=0.95,
        region=(originx, originy, windowx, windowy))

    # If bookmark exists, check right-click menu .
    while bookmark_to_blacklist is not None:

        bookmark_to_blacklist = pag.locateCenterOnScreen(
            ('./img/dest/at_dest' + (str(bookmark)) + '.bmp'),
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
                logging.debug('blacklisting bookmark ' + (str(bookmark)))
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
                logging.debug('not at bookmark ' + (str(bookmark)))
                keyboard.keypress('esc')
                bookmark += 1
                continue

        elif bookmark_to_blacklist is None:
            logging.warning('out of bookmarks to look for')
            return 0


def blacklist_set_bookmark(target_site):
    """Blacklist a specific bookmark by changing its name."""
    # TODO: possible blacklist bookmarks instead by deleting them, which
    # could lead to fewer bugs as sometimes the 'rename bookmark' window
    # does not behave as expected.
    logging.debug('blacklisting bookmark ' + (str(target_site)))
    bookmark_to_blacklist = pag.locateCenterOnScreen(
        ('./img/dest/at_dest' + (str(target_site)) + '.bmp'),
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
