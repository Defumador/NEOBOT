import time
import sys
import random

import pyautogui as pag

from lib import navigation as nav, keyboard, mouse
from lib.vars import originx, originy, windowx, windowy, target_lock_time

sys.setrecursionlimit(9999999)

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

    target_bookmark = 1
    # Try warping to bookmark 1 in the system. If bookmark 1 doesn't exist,
    # is not in the current system, or your ship is already there, increment
    # bookmark number by 1 and try again.
    travel_to_bookmark_var = nav.warp_to_specific_system_bookmark(
        target_bookmark)
    while travel_to_bookmark_var == 0 and target_bookmark <= 10:
        target_bookmark += 1
        travel_to_bookmark_var = nav.warp_to_specific_system_bookmark(
            target_bookmark)
        continue
    if travel_to_bookmark_var == 1 and target_bookmark <= 10:
        # Once a valid site is found, remember the site number the ship is
        # warping to so script doesn't try warping there again.
        if nav.wait_for_warp_to_complete() == 1:
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
    print('check_for_enemy_npcs -- called')
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
            print('check_for_enemy_ships -- all clear')
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
                                          confidence=0.90,
                                          region=(originx, originy,
                                                  windowx, windowy))
    if asteroid_l is not None:
        return 1
    asteroid_m = pag.locateCenterOnScreen('./img/overview/asteroid_m.bmp',
                                          confidence=0.90,
                                          region=(originx, originy,
                                                  windowx, windowy))
    if asteroid_m is not None:
        return 1
    asteroid_s = pag.locateCenterOnScreen('./img/overview/asteroid_s.bmp',
                                          confidence=0.90,
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
        time.sleep(float(random.randint(1000, 2000)) / 1000)
        while target_out_of_range_popup() == 1:
            keyboard.keypress('w')
            print('target_asteroid -- getting closer to target')
            time.sleep(float(random.randint(10000, 40000)) / 1000)
            keyboard.keypress('ctrl')
            time.sleep(float(random.randint(1000, 2000)) / 1000)
        if target_out_of_range_popup() == 0:
            print('target_asteroid -- locking target')
            time.sleep(target_lock_time)
            time.sleep(float(random.randint(1000, 3000)) / 1000)  # Wait for
            # a lock to be achieved.
            print('target_asteroid -- target locked, orbiting')
            keyboard.keypress('w')
        return 1

    elif asteroid_m is not None:
        (asteroid_mediumx, asteroid_mediumy) = asteroid_m
        pag.moveTo((asteroid_mediumx + (random.randint(-2, 200))),
                   (asteroid_mediumy + (random.randint(-3, 3))),
                   mouse.duration(), mouse.path())
        mouse.click()
        keyboard.keypress('ctrl')
        time.sleep(float(random.randint(1000, 2000)) / 1000)
        while target_out_of_range_popup() == 1:
            keyboard.keypress('w')
            print('target_asteroid -- getting closer to target')
            time.sleep(float(random.randint(10000, 40000)) / 1000)
            keyboard.keypress('ctrl')
            time.sleep(float(random.randint(1000, 2000)) / 1000)
        if target_out_of_range_popup() == 0:
            print('target_asteroid -- locking target')
            time.sleep(target_lock_time)
            time.sleep(float(random.randint(1000, 3000)) / 1000)
            print('target_asteroid -- target locked, orbiting')
            keyboard.keypress('w')
        return 1

    elif asteroid_s is not None:
        (asteroid_smallx, asteroid_smally) = asteroid_s
        pag.moveTo((asteroid_smallx + (random.randint(-2, 200))),
                   (asteroid_smally + (random.randint(-3, 3))),
                   mouse.duration(), mouse.path())
        mouse.click()
        keyboard.keypress('ctrl')
        time.sleep(float(random.randint(1000, 2000)) / 1000)
        while target_out_of_range_popup() == 1:
            keyboard.keypress('w')
            print('target_asteroid -- getting closer to target')
            time.sleep(float(random.randint(10000, 40000)) / 1000)
            keyboard.keypress('ctrl')
            time.sleep(float(random.randint(1000, 2000)) / 1000)
        if target_out_of_range_popup() == 0:
            print('target_asteroid -- locking target')
            time.sleep(target_lock_time)
            time.sleep(float(random.randint(1000, 3000)) / 1000)
            print('target_asteroid -- target locked, orbiting')
            keyboard.keypress('w')
        return 1
    else:
        print('target_asteroid -- no asteroids to target')
        return 0


def inv_full_popup():
    # Check for momentary popup indicating cargo/ore hold is full.
    # This popup lasts about 5 seconds.
    inv_full_popup_var = pag.locateCenterOnScreen(
        './img/popups/ship_inv_full.bmp',
        confidence=0.90, region=(originx, originy, windowx, windowy))
    if inv_full_popup_var is None:
        print('inv_full_popup -- not detected')
        return 0
    elif inv_full_popup_var is not None:
        print('inv_full_popup -- detected')
        return 1


def asteroid_depleted_popup():
    # Check for popup indicating the asteroid currently being mined has been
    # depleted.
    print('asteroid_depleted_popup -- not detected')
    return 0
    '''
    asteroid_depleted_popup_var = pag.locateCenterOnScreen(
        './img/overview/asteroid_depleted.bmp',
        confidence=0.90,
        region=(originx, originy, windowx, windowy))
    if asteroid_depleted_popup_var is None:
        return 0
    elif asteroid_depleted_popup_var is not None:
        print('asteroid_depleted_popup -- detected')
        return 1
    '''


def activate_miner():
    # Activate mining lasers in sequential order.
    if mining_lasers == 1:
        keyboard.keypress('f1')
        while miner_out_of_range_popup() == 1:
            time.sleep(float(random.randint(15000, 40000)) / 1000)
            activate_miner()
        if miner_out_of_range_popup() == 0:
            return 1

    elif mining_lasers == 2:
        keyboard.keypress('f1')
        while miner_out_of_range_popup() == 1:
            time.sleep(float(random.randint(15000, 40000)) / 1000)
            activate_miner()
        if miner_out_of_range_popup() == 0:
            keyboard.keypress('f2')
            return 1

    elif mining_lasers == 3:
        keyboard.keypress('f1')
        while miner_out_of_range_popup() == 1:
            time.sleep(float(random.randint(15000, 40000)) / 1000)
            activate_miner()
        if miner_out_of_range_popup() == 0:
            keyboard.keypress('f2')
            keyboard.keypress('f3')
            return 1

    elif mining_lasers == 4:
        keyboard.keypress('f1')
        while miner_out_of_range_popup() == 1:
            time.sleep(float(random.randint(15000, 40000)) / 1000)
            activate_miner()
        if miner_out_of_range_popup() == 0:
            keyboard.keypress('f2')
            keyboard.keypress('f3')
            keyboard.keypress('f4')
            return 1
    print('activate_mining_laser -- called')
    return 1


def miner_out_of_range_popup():
    # Check if the ship's mining laser is out of range. If it is,
    # orbit the asteroid at a specified distance and try activating the
    # mining laser again in a few seconds.
    miner_out_of_range = pag.locateCenterOnScreen(
        './img/popups/miner_out_of_range.bmp',
        confidence=0.90,
        region=(originx, originy, windowx, windowy))
    while miner_out_of_range is not None:
        print('miner_out_of_range_popup -- out of module range')
        return 1
    if miner_out_of_range is None:
        print('miner_out_of_range_popup -- in module range')
        return 0


def target_out_of_range_popup():
    # Check if ship is too far from the desired object in order to get a
    # target lock on it.
    target_out_of_range = pag.locateCenterOnScreen(
        './img/popups/target_too_far.bmp',
        confidence=0.90,
        region=(originx, originy, windowx, windowy))
    while target_out_of_range is not None:
        print('target_out_of_range -- out of targeting range')
        return 1
    if target_out_of_range is None:
        print('target_out_of_range -- in targeting range')
        return 0
