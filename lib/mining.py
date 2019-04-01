import time
import sys
import ctypes
import random
import ctypes

import pyautogui as pag

from lib import navigation as nav
from lib import docked
from lib import unload_ship
from lib import keyboard
from lib import mouse

global screenx
global screeny
global halfscreenx
global halfscreeny
global windowx
global windowy
global originx
global originy
global conf
global alignment_time


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

###############################################################################



def travel_to_bookmark():
    # Find a suitable asteroid field by warping to each bookmark in
    # numerical order.
    # Currently only mining in a single system with at least one station is
    # supported
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
        enemy_frigate = pag.locateCenterOnScreen(
            './img/overview/enemy_frigate.bmp',
            confidence=0.80,  # Lower confidence than normal so script will
            # detect icon in both overview and on grid.
            region=(originx, originy, windowx, windowy))
        if enemy_frigate is not None:
            print('check_for_enemy_npcs -- found hostile npc frigate')
            return 1
    # elif check_for_enemy_destroyers == 1:
    #	enemy_destroyer = pag.locateCenterOnScreen(
    #	'./img/overview/enemy_destroyer.bmp',
    #	confidence=0.90,
    #												region=(originx, originy,
    #												screenwidth,
    #												screenheight))
    #	if enemy_destroyer is not None:
    #		return 1
    # elif check_for_enemy_cruisers == 1:
    #	enemy_cruiser = pag.locateCenterOnScreen('./img/overview/enemy_cruiser.bmp',
    #	confidence=0.90,
    #											region=(originx, originy,
    #											screenwidth,
    #											screenheight))
    #	if enemy_cruiser is not None:
    #		return 1
    # elif check_for_enemy_battlecruisers == 1:
    #	enemy_battlecruiser = pag.locateCenterOnScreen(
    #	'./img/overview/enemy_battlecruiser.bmp', confidence=0.90,
    #													region=(originx,
    #													originy,
    #													screenwidth,
    #													screenheight))
    #	if enemy_battlecruiser is not None:
    #		return 1
    # elif check_for_enemy_battleships == 1:
    #	enemy_battleship = pag.locateCenterOnScreen(
    #	'./img/overview/enemy_battleship.bmp',
    #	confidence=0.90,
    #												region=(originx, originy,
    #												screenwidth,
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
    #	'./img/overview/player_war_target.bmp',
    #	confidence=0.80,
    #											region=(originx, originy,
    #											screenwidth,
    #											screenheight))
    #	if player_war_target is not None:
    #		print('check_for_players -- found war target')
    #		return 1
    # elif check_for_player_suspects == 1:
    #	player_war_target = pag.locateCenterOnScreen(
    #	'./img/player_war_target.bmp',
    #	confidence=0.80,
    #											region=(originx, originy,
    #											screenwidth,
    #											screenheight))
    #	if player_war_target is not None:
    #		print('check_for_players -- found war target')
    #		return 1
    #
    # elif check_for_player_criminals == 1:
    #	player_criminal = pag.locateCenterOnScreen(
    #	'./img/player_criminal.bmp',
    #	confidence=0.80,
    #											region=(originx, originy,
    #											screenwidth,
    #											screenheight))
    #	if player_criminal is not None:
    #		print('check_for_players -- found criminal')
    #		return 1
    #
    # elif check_for_player_neutrals == 1:
    #	player_neutral = pag.locateCenterOnScreen('./img/player_neutral.bmp',
    #	confidence=0.80,
    #											region=(originx, originy,
    #											screenwidth,
    #											screenheight))
    #	if player_neutral is not None:
    #		print('check_for_players -- found neutral')
    #		return 1
    #
    # elif check_for_player_war_targets == 1:
    #	player_war_target = pag.locateCenterOnScreen(
    #	'./img/player_war_target.bmp',
    #	confidence=0.80,
    #											region=(originx, originy,
    #											screenwidth,
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
    # region=(originx, originy, screenwidth, screenheight))
    # general_overview_tab = pag.locateCenterOnScreen(
    # './img/general_overview_tab.bmp', confidence=0.90,
    # region=(originx, originy, screenwidth, screenheight))
    global asteroid_s
    global asteroid_m
    global asteroid_l
    asteroid_l = pag.locateCenterOnScreen('./img/overview/asteroid_l.bmp',
                                          confidence=0.80,
                                          region=(originx, originy,
                                                  windowx, windowy))
    if asteroid_l is not None:
        return 1
    asteroid_m = pag.locateCenterOnScreen('./img/overview/asteroid_m.bmp',
                                          confidence=0.80,
                                          region=(originx, originy,
                                                  windowx, windowy))
    if asteroid_m is not None:
        return 1
    asteroid_s = pag.locateCenterOnScreen('./img/overview/asteroid_s.bmp',
                                          confidence=0.80,
                                          region=(originx, originy,
                                                  windowx, windowy))
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
                   mouse.duration(), mouse.path())
        mouse.click()
        keyboard.keypress('ctrl')
        return 1
    elif asteroid_m is not None:
        (asteroid_mediumx, asteroid_mediumy) = asteroid_m
        pag.moveTo((asteroid_mediumx + (random.randint(-2, 200))),
                   (asteroid_mediumy + (random.randint(-3, 3))),
                   mouse.duration(), mouse.path())
        mouse.click()
        keyboard.keypress('ctrl')
        return 1
    elif asteroid_s is not None:
        (asteroid_smallx, asteroid_smally) = asteroid_s
        pag.moveTo((asteroid_smallx + (random.randint(-2, 200))),
                   (asteroid_smally + (random.randint(-3, 3))),
                   mouse.duration(), mouse.path())
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
    inv_full_popup = pag.locateCenterOnScreen(
        './img/popups/ship_inv_full.bmp',
        confidence=0.90, region=(originx, originy, windowx, windowy))
    if inv_full_popup is None:
        return 0
    elif inv_full_popup is not None:
        print('inv_full_popup -- detected')
        return 1


def asteroid_depleted_popup():
    # Check for popup indicating the asteroid currently being mined has been
    # depleted.
    asteroid_depleted = pag.locateCenterOnScreen(
        './img/overview/asteroid_depleted.bmp',
        confidence=0.90,
        region=(originx, originy, windowx, windowy))
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
