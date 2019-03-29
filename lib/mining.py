import time
import sys
import ctypes
import random

import pyautogui as pag

from lib import navigation as nav
from lib import docked
from lib import unload_ship
from lib import keyboard
from lib import mouse

atsite = 0
gotosite = 0
sys.setrecursionlimit(9999999)

user32 = ctypes.windll.user32
screenx = user32.GetSystemMetrics(0)
screeny = user32.GetSystemMetrics(1)
halfscreenx = (int(screenx / 2))
halfscreeny = (int(screeny / 2))

###############################################################################
# User-specified variables.

mining_lasers = 1

check_for_enemy_frigates = 1
check_for_enemy_destroyers = 1
check_for_enemy_cruisers = 1
check_for_enemy_battlecruisers = 1
check_for_enemy_battleships = 1

# check_for_player_neutrals = 1
# check_for_player_suspects = 1
# check_for_player_war_targets = 1
# check_for_player_criminals = 1
# check_for_player_yellows = 1
# check_for_player_greys = 1

window_resolutionx = 1024
window_resolutiony = 768

###############################################################################

# get the coordinates of the eve client window and restrict image searching to
# within these boundaries.
# search for the eve neocom logo in top left corner of the eve client window.
# This will become the origin of the coordinate system.
origin = pag.locateCenterOnScreen('./img/origin.bmp', confidence = 0.95,
                                  region = (0, 0, screenx, screeny))
(originx, originy) = origin
windowx = originx + window_resolutionx
windowy = originy + window_resolutiony


def miner():
    while docked.docked_check() == 0:
        if travel_to_bookmark() == 1:
            # Once arrived at site, check for hostile npcs and human players.
            # If either exist, warp to a different site.
            # If no hostiles npcs or players are present, check for asteroids.
            # If no asteroids, blacklist site and warp to next site.
            if check_for_enemy_npcs() == 1:
                break
            # if check_for_players() == 1:
            #   break
            while check_for_asteroids() == 1:
                target_asteroid()
                activate_mining_laser()
                # If ship inventory isn't full, continue to mine ore and wait
                # for popups or errors.
                while inv_full_popup() == 0:
                    if asteroid_depleted_popup() == 1:
                        if check_for_asteroids() == 0:
                            nav.blacklist_bookmark(atsite)
                            miner()
                        elif check_for_asteroids() == 1:
                            target_asteroid()
                            activate_mining_laser()
                            inv_full_popup()
                            continue
                    if check_for_enemy_npcs() == 1:
                        miner()
                    # check_for_players()
                    # if check_for_players() == 1:
                    # miner()
                    time.sleep(1)
                if inv_full_popup() == 1:
                    # Once inventory is full, dock at home station and unload.
                    nav.go_home()
                    unload_ship.unload_ship()
                    docked.undock()
                    time.sleep(3)
                    miner()
            if check_for_asteroids() == 0:
                nav.blacklist_bookmark(atsite)
        elif travel_to_bookmark() == 0:
            nav.emergency_terminate()
            sys.exit(0)
    if docked.docked_check() == 1:
        # If docked when script starts, undock.
        docked.undock()
        miner()


def travel_to_bookmark():
    # Find a suitable asteroid field by warping to each bookmark in
    # numerical order.
    global gotosite
    global atsite
    gotosite = 1
    # Try warping to bookmark 1 in the system. If bookmark 1 doesn't exist,
    # is not in the current system, or your ship is already there, increment
    # bookmark number by 1 and try again.
    while nav.warp_to_specific_system_bookmark(
            gotosite) == 0 and gotosite <= 10:
        gotosite += 1
        continue
    if nav.warp_to_specific_system_bookmark(
            gotosite) == 1 and gotosite <= 10:
        # Once a valid site is found, remember the site number the ship is
        # warping to so script doesn't try warping there again.
        atsite = gotosite
        if nav.detect_warp() == 1:
            return 1
    else:
        print('travel_to_bookmark -- ran out of sites to check for')
        return 0


def check_for_enemy_npcs():
    # Check entire window for red ship hud icons, indicating hostile npcs.
    # Only avoid the hostile ship classes specified by the user in the
    # global variables above. Script will try looking for these icons on the
    # default 'general' overview tab. Script will keep the 'general' overview
    # tab visible by default until switching tabs in required to locate another
    # asteroid.
    print('check_for_enemy_npcs called')
    if check_for_enemy_frigates == 1:
        enemy_frigate = pag.locateCenterOnScreen('./img/enemy_frigate.bmp',
                                                 confidence = 0.80,
                                                 region = (
                                                     0, 0, screenx,
                                                     screeny))
        if enemy_frigate is not None:
            print('check_for_enemy_npcs -- found hostile npc frigate')
            return 1
    # elif check_for_enemy_destroyers == 1:
    #	enemy_destroyer = pag.locateCenterOnScreen(
    #	'./img/enemy_destroyer.bmp',
    #	confidence=0.90,
    #												region=(0, 0, screenwidth,
    #												screenheight))
    #	if enemy_destroyer is not None:
    #		return 1
    # elif check_for_enemy_cruisers == 1:
    #	enemy_cruiser = pag.locateCenterOnScreen('./img/enemy_cruiser.bmp',
    #	confidence=0.90,
    #											region=(0, 0, screenwidth,
    #											screenheight))
    #	if enemy_cruiser is not None:
    #		return 1
    # elif check_for_enemy_battlecruisers == 1:
    #	enemy_battlecruiser = pag.locateCenterOnScreen(
    #	'./img/enemy_battlecruiser.bmp', confidence=0.90,
    #													region=(0, 0,
    #													screenwidth,
    #													screenheight))
    #	if enemy_battlecruiser is not None:
    #		return 1
    # elif check_for_enemy_battleships == 1:
    #	enemy_battleship = pag.locateCenterOnScreen(
    #	'./img/enemy_battleship.bmp',
    #	confidence=0.90,
    #												region=(0, 0, screenwidth,
    #												screenheight))
    #	if enemy_battleship is not None:
    #		return 1
    else:
        print('check_for_enemy_ships -- no hostile npcs to avoid')
        return 0


def check_for_players():
    # Same as check_for_enemy_npcs function, except check for certain
    # classes of
    # human players as specified by the user.
    # if check_for_player_war_targets == 1:
    #	player_war_target = pag.locateCenterOnScreen(
    #	'./img/player_war_target.bmp',
    #	confidence=0.80,
    #											region=(0, 0, screenwidth,
    #											screenheight))
    #	if player_war_target is not None:
    #		print('check_for_players -- found war target')
    #		return 1
    # elif check_for_player_suspects == 1:
    #	player_war_target = pag.locateCenterOnScreen(
    #	'./img/player_war_target.bmp',
    #	confidence=0.80,
    #											region=(0, 0, screenwidth,
    #											screenheight))
    #	if player_war_target is not None:
    #		print('check_for_players -- found war target')
    #		return 1
    #
    # elif check_for_player_criminals == 1:
    #	player_criminal = pag.locateCenterOnScreen(
    #	'./img/player_criminal.bmp',
    #	confidence=0.80,
    #											region=(0, 0, screenwidth,
    #											screenheight))
    #	if player_criminal is not None:
    #		print('check_for_players -- found criminal')
    #		return 1
    #
    # elif check_for_player_neutrals == 1:
    #	player_neutral = pag.locateCenterOnScreen('./img/player_neutral.bmp',
    #	confidence=0.80,
    #											region=(0, 0, screenwidth,
    #											screenheight))
    #	if player_neutral is not None:
    #		print('check_for_players -- found neutral')
    #		return 1
    #
    # elif check_for_player_war_targets == 1:
    #	player_war_target = pag.locateCenterOnScreen(
    #	'./img/player_war_target.bmp',
    #	confidence=0.80,
    #											region=(0, 0, screenwidth,
    #											screenheight))
    #	if player_war_target is not None:
    #		print('check_for_players -- found war target')
    #		return 1
    return 0


def check_for_asteroids():
    # Switch overview to 'mining' tab, check for asteroids, then switch back to
    # the 'general' tab. Prioritize larger asteroids by searching for them
    # first.
    # mining_overview_tab = pag.locateCenterOnScreen(
    # './img/mining_overview_tab.bmp',
    # confidence=0.90,
    # region=(0, 0, screenwidth, screenheight))
    # general_overview_tab = pag.locateCenterOnScreen(
    # './img/general_overview_tab.bmp', confidence=0.90,
    # region=(0, 0, screenwidth, screenheight))
    global asteroid_s
    global asteroid_m
    global asteroid_l
    asteroid_l = pag.locateCenterOnScreen('./img/asteroid_l.bmp',
                                          confidence = 0.80,
                                          region = (
                                              0, 0, screenx,
                                              screeny))
    if asteroid_l is not None:
        return 1
    asteroid_m = pag.locateCenterOnScreen('./img/asteroid_m.bmp',
                                          confidence = 0.80,
                                          region = (
                                              0, 0, screenx,
                                              screeny))
    if asteroid_m is not None:
        return 1
    asteroid_s = pag.locateCenterOnScreen('./img/asteroid_s.bmp',
                                          confidence = 0.80,
                                          region = (
                                              originx, originy, windowx,
                                              windowy))
    if asteroid_s is not None:
        return 1
    else:
        print('check_for_asteroids -- no more asteroids found at site')
    return 0


def target_asteroid():
    # Target the closest large-sized asteroid in overview, assuming overview is
    # sorted by distance, with closest objects at the top.
    # Switch to mining tab, target asteroid, then switch back to general tab.
    global asteroid_s
    global asteroid_m
    global asteroid_l
    if asteroid_l is not None:
        (asteroid_largex, asteroid_largey) = asteroid_l
        pag.moveTo((asteroid_largex + (random.randint(-2, 200))),
                   (asteroid_largey + (random.randint(-3, 3))),
                   mouse.move_time(), mouse.mouse_path())
        mouse.click()
        keyboard.keypress('ctrl')
        return 1
    elif asteroid_m is not None:
        (asteroid_mediumx, asteroid_mediumy) = asteroid_m
        pag.moveTo((asteroid_mediumx + (random.randint(-2, 200))),
                   (asteroid_mediumy + (random.randint(-3, 3))),
                   mouse.move_time(), mouse.mouse_path())
        mouse.click()
        keyboard.keypress('ctrl')
        return 1
    elif asteroid_s is not None:
        (asteroid_smallx, asteroid_smally) = asteroid_s
        pag.moveTo((asteroid_smallx + (random.randint(-2, 200))),
                   (asteroid_smally + (random.randint(-3, 3))),
                   mouse.move_time(), mouse.mouse_path())
        mouse.click()
        keyboard.keypress('ctrl')
        time.sleep(float(random.randint(500, 1500)) / 1000)
        return 1
    else:
        print('target_asteroid -- no asteroids to target')
        return 0


def inv_full_popup():
    # Check for momentary popup indicating cargo/ore hold is full.
    # This popup lasts about 5 seconds.
    inv_full_popup = pag.locateCenterOnScreen('./img/cargo_hold_full.bmp',
                                              confidence = 0.90,
                                              region = (
                                                  0, 0, screenx,
                                                  screeny))
    if inv_full_popup is None:
        return 0
    elif inv_full_popup is not None:
        print('inv_full_popup -- detected')
        return 1


def asteroid_depleted_popup():
    # Check for popup indicating the asteroid currently being mined has been
    # depleted.
    asteroid_depleted = pag.locateCenterOnScreen('./img/asteroid_depleted.bmp',
                                                 confidence = 0.90,
                                                 region = (
                                                     0, 0, screenx,
                                                     screeny))
    if asteroid_depleted is None:
        return 0
    elif asteroid_depleted is not None:
        print('asteroid_depleted_popup -- detected')
        return 1


def activate_mining_laser():
    # Activate mining lasers in sequential order.
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
    print('activate_mining_laser -- called')
    return 1
