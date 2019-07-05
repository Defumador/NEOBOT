import time
import sys
import random
import traceback

import pyautogui as pag

from lib import navigation as nav, keyboard, mouse
from lib.vars import originx, originy, windowx, windowy, target_lock_time

sys.setrecursionlimit(9999999)

###############################################################################
#  User-specified variables
###############################################################################

mining_lasers = 2
# Attack drones only, mining drones are not yet supported.
drones = 1

# -----------------------------------------------------------------------------

detect_npcs_var = 1

detect_npc_frigate_and_destroyer = 0
detect_npc_cruiser_and_battlecruiser = 1
detect_npc_battleship = 1

# -----------------------------------------------------------------------------

detect_pcs_var = 1

detect_pc_mining_barge_and_industrial = 1
detect_pc_frigate_and_destroyer = 1
detect_pc_capital_industrial_and_freighter = 1
detect_pc_cruiser_and_battlecruiser = 1

detect_pc_battleship = 1
detect_pc_rookie_ship = 1
detect_pc_capsule = 1

###############################################################################

# Move most of these functions into an "overview" file.


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
        print('travel_to_bookmark -- ran out of sites to check for')
        return 0


def detect_asteroids():
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

    asteroid_m = pag.locateCenterOnScreen('./img/overview/asteroid_m.bmp',
                                          confidence=0.90,
                                          region=(originx, originy,
                                                  windowx, windowy))
    if asteroid_m is not None:
        return 1
    asteroid_l = pag.locateCenterOnScreen('./img/overview/asteroid_l.bmp',
                                          confidence=0.90,
                                          region=(originx, originy,
                                                  windowx, windowy))
    if asteroid_l is not None:
        return 1
    asteroid_s = pag.locateCenterOnScreen('./img/overview/asteroid_s.bmp',
                                          confidence=0.90,
                                          region=(originx, originy,
                                                  windowx, windowy))
    if asteroid_s is not None:
        return 1
    else:
        print('detect_asteroids -- no more asteroids found at site')
    return 0


def target_asteroid():
    # Target the closest large-sized asteroid in overview, assuming overview is
    # sorted by distance, with closest objects at the top.
    # Switch to mining tab, target asteroid, then switch back to general tab.
    global asteroid_s
    global asteroid_m
    global asteroid_l

    if asteroid_m is not None:
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

    elif asteroid_l is not None:
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


def focus_general_tab():
    # Switch to the default 'General' tab of the overview to check for other
    # ships.
    print('focus_general_tab -- called')
    general_tab_selected = pag.locateCenterOnScreen(
        './img/overview/general_overview_tab_selected.bmp',
        # Requires very high confidence since the button looks only slightly
        # different when it's selected.
        confidence=0.992,
        region=(originx, originy,
                windowx, windowy))
    if general_tab_selected is not None:
        print('focus_general_tab -- already selected')
        return 1
    else:
        general_tab_unselected = pag.locateCenterOnScreen(
            './img/overview/general_overview_tab.bmp',
            confidence=0.95,
            region=(originx, originy,
                    windowx, windowy))

        if general_tab_unselected is not None:
            (x, y) = general_tab_unselected
            pag.moveTo((x + (random.randint(-14, 14))),
                       (y + (random.randint(-7, 7))),
                       mouse.duration(), mouse.path())
            mouse.click()
            return 1
        else:
            return 0


def focus_mining_tab():
    # Switch to the default 'Mining' tab of the overview to check for
    # asteroids.
    print('focus_mining_tab -- called')
    mining_tab_selected = pag.locateCenterOnScreen(
        './img/overview/mining_overview_tab_selected.bmp',
        # Requires very high confidence because the button looks slightly
        # different when it's selected.
        confidence=0.992,
        region=(originx, originy,
                windowx, windowy))
    if mining_tab_selected is not None:
        print('focus_mining_tab -- already selected')
    else:
        mining_tab_unselected = pag.locateCenterOnScreen(
            './img/overview/mining_overview_tab.bmp',
            confidence=0.95,
            region=(originx, originy,
                    windowx, windowy))

        if mining_tab_unselected is not None:
            (x, y) = mining_tab_unselected
            pag.moveTo((x + (random.randint(-10, 10))),
                       (y + (random.randint(-7, 7))),
                       mouse.duration(), mouse.path())
            mouse.click()
            return 1
        else:
            return 0


def inv_full_popup():
    # Check for momentary popup indicating cargo/ore hold is full.
    # This popup lasts about 5 seconds.
    inv_full_popup_var = pag.locateCenterOnScreen(
        './img/popups/ship_inv_full.bmp',
        confidence=0.9,
        region=(originx, originy,
                windowx, windowy))
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


def launch_drones():
    # User must custom-set the "launch drones" hotkey to be Shift-l
    if drones != 0:
        time.sleep(float(random.randint(10, 800)) / 1000)
        pag.keyDown('shift')
        time.sleep(float(random.randint(10, 800)) / 1000)
        pag.keyDown('l')
        time.sleep(float(random.randint(10, 800)) / 1000)
        pag.keyUp('shift')
        time.sleep(float(random.randint(10, 800)) / 1000)
        pag.keyUp('l')
        time.sleep(float(random.randint(2000, 5000)) / 1000)
        print('launch drones -- drones launched')
        return 1
    else:
        return 1


drones_dict = {1: "1", 2: "2", 3: "3", 4: "4", 5: "5"}


def recall_drones():
    if drones != 0:
        time.sleep(float(random.randint(10, 800)) / 1000)
        pag.keyDown('shift')
        time.sleep(float(random.randint(10, 800)) / 1000)
        pag.keyDown('r')
        time.sleep(float(random.randint(10, 800)) / 1000)
        pag.keyUp('shift')
        time.sleep(float(random.randint(10, 800)) / 1000)
        pag.keyUp('r')

        # Wait for all drones to return to drone bay.
        drones_recalled = pag.locateOnScreen('./img/indicators/drones/' + (
            drones_dict[drones]) + '_drone_in_bay.bmp')
        tries = 1
        while drones_recalled is None and tries <= 25:
            time.sleep(float(random.randint(1000, 2000)) / 1000)
            drones_recalled = pag.locateOnScreen('./img/indicators/drones/' + (
                drones_dict[drones]) + '_drone_in_bay.bmp')
            tries += 1
        if drones_recalled is not None and tries <= 25:
            print('recall_drones -- drones returned to bay')
            return 1
        else:
            print('recall_drones -- timed out waiting for drones to return')
            return 1
    else:
        return 0


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


def detect_npcs():
    # Check for hostile non-player characters by looking for red ship icons in
    # the overview.
    #print('detect_npcs -- called')
    conf = 0.98
    if detect_npcs_var == 1:

        # Search within the rightmost third of the client. Bot assumes
        # overview is on the right half of the screen. This is about
        # twice as fast as searching the entire 1024x768 client.
        overview = pag.screenshot(
            region=((originx + (windowx - (int(windowx / 2)))),
                    originy, (int(windowx / 2)), windowy))

        # Create an empty list to be filled with player icon paths
        npc_list = []

        # Populate pc_list with only the player icons that the user wishes to
        # check for, as specified by the variables at the top of this file.
        if detect_npc_frigate_and_destroyer == 1:
            npc_list.append(
                './img/overview/npc_ship_icons/npc_hostile_frigate.bmp')
        if detect_npc_cruiser_and_battlecruiser == 1:
            npc_list.append(
                './img/overview/npc_ship_icons/npc_hostile_cruiser.bmp')
        #if detect_npc_battleship == 1:
        #    npc_list.append(
        #        './img/overview/npc_ship_icons/npc_hostile_battleship.bmp')

        # Scan the 'overview' screenshot for each player icon in the list.
        for npc_icon in npc_list:
            hostile_npc_found = pag.locate(npc_icon, overview, confidence=conf)

            if hostile_npc_found is not None:
                print('detect_npcs -- found ship at', hostile_npc_found)
                print('located icon', npc_icon)
                # Break up the tuple so mouse can point at icon for debugging.
                (x, y, t, w) = hostile_npc_found
                # Coordinates must compensate for the altered coordinate-space
                # of the screenshot.
                pag.moveTo((x + (originx + (windowx - (int(windowx / 2))))),
                           (y + originy),
                           0, mouse.path())
                return 1
        print('detect npcs -- no hostile NPCs found')
        return 0
    else:
        return 0


def detect_pcs():
    # Check for player characters by looking for player ship icons in the
    # overview.
    #print('detect_pcs -- called')
    conf = 0.98
    if detect_pcs_var == 1:

        # Search within the rightmost third of the client. Bot assumes
        # overview is on the right half of the screen. This is about
        # twice as fast as searching the entire 1024x768 client.
        overview = pag.screenshot(
            region=((originx + (windowx - (int(windowx / 2)))),
                    originy, (int(windowx / 2)), windowy))

        # Create an empty list to be filled with player icon paths
        pc_list = []

        # Populate pc_list with only the player icons that the user wishes to
        # check for, as specified by the variables at the top of this file.
        if detect_pc_mining_barge_and_industrial == 1:
            pc_list.append(
                './img/overview/player_ship_icons/archetype_icons'
                '/player_mining_barge_and_industrial.bmp')
        if detect_pc_frigate_and_destroyer == 1:
            pc_list.append(
                './img/overview/player_ship_icons'
                '/archetype_icons/player_frigate_and_destroyer.bmp')
        if detect_pc_cruiser_and_battlecruiser == 1:
            pc_list.append(
                './img/overview/player_ship_icons'
                '/archetype_icons/player_cruiser_and_battlecruiser.bmp')
        if detect_pc_battleship == 1:
            pc_list.append(
                './img/overview/player_ship_icons/archetype_icons'
                '/player_battleship.bmp')
        if detect_pc_capital_industrial_and_freighter == 1:
            pc_list.append(
                './img/overview/player_ship_icons/archetype_icons'
                '/player_capital_industrial_and_freighter.bmp')
        if detect_pc_rookie_ship == 1:
            pc_list.append(
                './img/overview/player_ship_icons/archetype_icons'
                '/player_rookie_ship.bmp')
        if detect_pc_capsule == 1:
            pc_list.append(
                './img/overview/player_ship_icons/archetype_icons'
                '/player_capsule.bmp')

        # Scan the 'overview' screenshot for each player icon in the list.
        for pc_icon in pc_list:
            player_found = pag.locate(pc_icon, overview, confidence=conf)

            if player_found is not None:
                print('detect_pcs -- found player at', player_found)
                print('located icon', pc_icon)
                # Break up the tuple so mouse can point at icon for debugging.
                (x, y, t, w) = player_found
                # Coordinates must compensate for the altered coordinate-space
                # of the screenshot.
                pag.moveTo((x + (originx + (windowx - (int(windowx / 2))))),
                           (y + originy),
                           0, mouse.path())
                return 1
        print('detect pcs -- no players found')
        return 0
    else:
        return 0


'''
def detect_pcs():
    # Same as check_for_enemies function, except check for certain
    # classes of
    # human players as specified by the user. Search for most common ship
    # types first
    print('detect_pcs -- called')
    conf = 0.96
    if check_for_players_var == 1:
        if check_for_player_type_barge_and_industrial == 1:
################ No need for locateCenterOnScreen            
            mining_barge_and_industrial = pag.locateOnScreen(
                './img/overview/player_ship_icons/archetype_icons'
                '/player_mining_barge_and_industrial.bmp', confidence=conf,
################ Search right quarter of screen only. This is a tuple (left,top,width,height), NOT coordinates!! ( (x1, y1), (x2, y2) )
                region=((windowx - (int(windowx / 4))), originy,
                        (int(windowx / 4)), windowy))
            if mining_barge_and_industrial is not None:
                print('detect_pcs -- found mining_barge_and_industrial',
                      mining_barge_and_industrial)
                print(mining_barge_and_industrial)
                #(x, y) = mining_barge_and_industrial
                #pag.moveTo(x, y,  # Move mouse over
                           # icon for debugging purposes
                           #.5, mouse.path())
                return 1

        if check_for_player_type_frigate_and_destroyer == 1:
            frigate_and_destroyer = pag.locateOnScreen(
                './img/overview/player_ship_icons'
                '/archetype_icons/player_frigate_and_destroyer.bmp',
                confidence=conf,
                region=((windowx - (int(windowx / 4))), originy,
                        (int(windowx / 4)), windowy))
            if frigate_and_destroyer is not None:
                print('detect_pcs -- found frigate_and_destroyer',
                      frigate_and_destroyer)
                #(x, y) = frigate_and_destroyer
                #pag.moveTo(x, y,  # Move mouse over
                           # icon for debugging purposes
                #           .5, mouse.path())
                return 1

        if check_for_player_type_capital_industrial_and_freighter == 1:
            capital_industrial_and_freighter = pag.locateOnScreen(
                './img/overview/player_ship_icons'
                '/archetype_icons/player_capital_industrial_and_freighter.bmp',
                confidence=conf,
                region=((windowx - (int(windowx / 4))), originy,
                        (int(windowx / 4)), windowy))
            if capital_industrial_and_freighter is not None:
                print('detect_pcs --'
                      'found capital_industrial_and_freighter'
                      , capital_industrial_and_freighter)
                #(x, y) = capital_industrial_and_freighter
                #pag.moveTo(x, y,  # Move mouse over
                #           # icon for debugging purposes
                #           .5, mouse.path())
                return 1

        if check_for_player_type_cruiser_and_battlecruiser == 1:
            cruiser_and_battlecruiser = pag.locateOnScreen(
                './img/overview/player_ship_icons'
                '/archetype_icons/player_cruiser_and_battlecruiser.bmp',
                confidence=conf,
                region=((windowx - (int(windowx / 4))), originy,
                        (int(windowx / 4)), windowy))
            if cruiser_and_battlecruiser is not None:
                print('detect_pcs -- found cruiser_and_battlecruiser',
                      cruiser_and_battlecruiser)
                #(x, y) = cruiser_and_battlecruiser
                #pag.moveTo(x, y,  # Move mouse over
                           # icon for debugging purposes
                #           .5, mouse.path())
                return 1

        if check_for_player_type_battleship == 1:
            battleship = pag.locateOnScreen(
                './img/overview/player_ship_icons'
                '/archetype_icons/player_battleship.bmp',
                confidence=conf,
                region=((windowx - (int(windowx / 4))), originy,
                        (int(windowx / 4)), windowy))
            if battleship is not None:
                print('detect_pcs -- found battleship',
                      battleship)
                #(x, y) = battleship
                #pag.moveTo(x, y,  # Move mouse over
                           # icon for debugging purposes
                #           .5, mouse.path())
                return 1

        if check_for_player_type_rookie_ship == 1:
            rookie_ship = pag.locateOnScreen(
                './img/overview/player_ship_icons'
                '/archetype_icons/player_rookie_ship.bmp',
                confidence=conf,
                region=((windowx - (int(windowx / 4))), originy,
                        (int(windowx / 4)), windowy))
            if rookie_ship is not None:
                print('detect_pcs -- found rookie_ship',
                      rookie_ship)
                #(x, y) = rookie_ship
                #pag.moveTo(x, y,  # Move mouse over
                           # icon for debugging purposes
                #           .5, mouse.path())
                return 1

        if check_for_player_type_capsule == 1:
            capsule = pag.locateOnScreen(
                './img/overview/player_ship_icons'
                '/archetype_icons/player_capsule.bmp',
                confidence=conf,
                region=((windowx - (int(windowx / 4))), originy,
                        (int(windowx / 4)), windowy))
            if capsule is not None:
                print('detect_pcs -- found capsule',
                      capsule)
                #(x, y) = capsule
                #pag.moveTo(x, y,  # Move mouse over
                           # icon for debugging purposes
                 #          .5, mouse.path())
                return 1

            else:
                print('detect_pcs -- all clear')
                return 0
        else:
            return 0
    else:
        return 0

                
# Old check for player function in which player standing was checked rather 
than simply ship icons. The entire function takes around 4 seconds on a 1024x768 client. 

check_for_player_type_alliancemate = 1
check_for_player_type_ally = 1
check_for_player_type_bad_standing = 1
check_for_player_type_corpmate = 1
check_for_player_type_criminal = 1
check_for_player_type_engagement = 1
check_for_player_type_excellent_standing = 1
check_for_player_type_fleetmate = 1
check_for_player_type_good_standing = 1
check_for_player_type_has_bounty = 1
check_for_player_type_has_killright = 1
check_for_player_type_militia_ally = 1
check_for_player_type_neg5_sec = 1
check_for_player_type_neutral_standing = 1
check_for_player_type_suspect = 1
check_for_player_type_terrible_standing = 1
check_for_player_type_war_target = 1
check_for_player_type_war_target_militia = 1
check_for_player_type_zero_sec = 1

def detect_pcs():
    # Same as check_for_enemies function, except check for certain
    # classes of
    # human players as specified by the user.
    print('detect_pcs -- called')
    conf = 0.96

    if check_for_player_type_alliancemate == 1:
        alliancemate = pag.locateCenterOnScreen(
            './img/overview/player_type_alliancemate.bmp',
            confidence=conf,
            region=(originx, originy,
                    windowx, windowy))
        if alliancemate is not None:
            print('detect_pcs -- found alliancemate', alliancemate)
            return 1

    if check_for_player_type_ally == 1:
        ally = pag.locateCenterOnScreen(
            './img/overview/player_type_ally.bmp',
            confidence=conf,
            region=(originx, originy,
                    windowx, windowy))
        if ally is not None:
            print('detect_pcs -- found ally')
            return 1

    if check_for_player_type_bad_standing == 1:
        bad_standing = pag.locateCenterOnScreen(
            './img/overview/player_type_bad_standing.bmp',
            confidence=conf,
            region=(originx, originy,
                    windowx, windowy))
        if bad_standing is not None:
            print('detect_pcs -- found player with bad standing')
            return 1

    if check_for_player_type_corpmate == 1:
        corpmate = pag.locateCenterOnScreen(
            './img/overview/player_type_corpmate.bmp',
            confidence=conf,
            region=(originx, originy,
                    windowx, windowy))
        if corpmate is not None:
            print('detect_pcs -- found corpmate')
            return 1

    if check_for_player_type_criminal == 1:
        criminal = pag.locateCenterOnScreen(
            './img/overview/player_type_criminal.bmp',
            confidence=conf,
            region=(originx, originy,
                    windowx, windowy))
        if criminal is not None:
            print('detect_pcs -- found criminal')
            return 1

    if check_for_player_type_engagement == 1:
        engagement = pag.locateCenterOnScreen(
            './img/overview/player_type_engagement.bmp',
            confidence=conf,
            region=(originx, originy,
                    windowx, windowy))
        if engagement is not None:
            print('detect_pcs -- found player with limited engagement')
            return 1

    if check_for_player_type_excellent_standing == 1:
        excellent_standing = pag.locateCenterOnScreen(
            './img/overview/player_type_excellent_standing.bmp',
            confidence=conf,
            region=(originx, originy,
                    windowx, windowy))
        if excellent_standing is not None:
            print('detect_pcs -- found player with excellent standing')
            return 1

    if check_for_player_type_fleetmate == 1:
        fleetmate = pag.locateCenterOnScreen(
            './img/overview/player_type_fleetmate.bmp',
            confidence=conf,
            region=(originx, originy,
                    windowx, windowy))
        if fleetmate is not None:
            print('detect_pcs -- found fleetmate')
            return 1

    if check_for_player_type_good_standing == 1:
        good_standing = pag.locateCenterOnScreen(
            './img/overview/player_type_good_standing.bmp',
            confidence=conf,
            region=(originx, originy,
                    windowx, windowy))
        if good_standing is not None:
            print('detect_pcs -- found player with good standing')
            return 1

    if check_for_player_type_has_bounty == 1:
        has_bounty = pag.locateCenterOnScreen(
            './img/overview/player_type_has_bounty.bmp',
            confidence=conf,
            region=(originx, originy,
                    windowx, windowy))
        if has_bounty is not None:
            print('detect_pcs -- found player with a bounty')
            return 1

    if check_for_player_type_has_killright == 1:
        has_killright = pag.locateCenterOnScreen(
            './img/overview/player_type_has_killright.bmp',
            confidence=conf,
            region=(originx, originy,
                    windowx, windowy))
        if has_killright is not None:
            print('detect_pcs -- found player with a killright')
            return 1

    if check_for_player_type_militia_ally == 1:
        militia_ally = pag.locateCenterOnScreen(
            './img/overview/player_type_militia_ally.bmp',
            confidence=conf,
            region=(originx, originy,
                    windowx, windowy))
        if militia_ally is not None:
            print('detect_pcs -- found militia ally')
            return 1

    if check_for_player_type_neg5_sec == 1:
        neg5_sec = pag.locateCenterOnScreen(
            './img/overview/player_type_neg5_sec.bmp',
            confidence=conf,
            region=(originx, originy,
                    windowx, windowy))
        if neg5_sec is not None:
            print('detect_pcs -- found player with under -5 security')
            return 1

    if check_for_player_type_neutral_standing == 1:
        neutral_standing = pag.locateCenterOnScreen(
            './img/overview/player_type_neutral_standing.bmp',
            confidence=conf,
            region=(originx, originy,
                    windowx, windowy))
        if neutral_standing is not None:
            print('detect_pcs -- found player with neutral standing')
            return 1

    if check_for_player_type_suspect == 1:
        suspect = pag.locateCenterOnScreen(
            './img/overview/player_type_suspect.bmp',
            confidence=conf,
            region=(originx, originy,
                    windowx, windowy))
        if suspect is not None:
            print('detect_pcs -- found suspect')
            return 1

    if check_for_player_type_terrible_standing == 1:
        terrible_standing = pag.locateCenterOnScreen(
            './img/overview/player_type_terrible_standing.bmp',
            confidence=conf,
            region=(originx, originy,
                    windowx, windowy))
        if terrible_standing is not None:
            print('detect_pcs -- found player with terrible '
                  'standing', terrible_standing)
            return 1

    if check_for_player_type_war_target == 1:
        war_target = pag.locateCenterOnScreen(
            './img/overview/player_type_war_target.bmp',
            confidence=conf,
            region=(originx, originy,
                    windowx, windowy))
        if war_target is not None:
            print('detect_pcs -- found war target')
            return 1

    if check_for_player_type_war_target_militia == 1:
        war_target_militia = pag.locateCenterOnScreen(
            './img/overview/player_type_war_target_militia.bmp',
            confidence=conf,
            region=(originx, originy,
                    windowx, windowy))
        if war_target_militia is not None:
            print('detect_pcs -- found militia war target')
            return 1

    if check_for_player_type_zero_sec == 1:
        zero_sec = pag.locateCenterOnScreen(
            './img/overview/player_type_zero_sec.bmp',
            confidence=conf,
            region=(originx, originy,
                    windowx, windowy))
        if zero_sec is not None:
            print('detect_pcs -- found player with under 0 security')
            return 1

    else:
        print('detect_pcs -- found no players')
        return 0

def check_for_enemies():
    # Check entire window for red ship hud icons, indicating hostile npcs.
    # Only avoid the hostile ship classes specified by the user in the
    # global variables above. Script will try looking for these icons on the
    # default 'general' overview tab. Script will keep the 'general' overview
    # tab visible by default until switching tabs in required to locate another
    # asteroid.
    print('check_for_enemies -- called')
    if check_for_enemy_frigates == 1:
        enemy_frigate = pag.locateCenterOnScreen(
            './img/overview/enemy_frigate.bmp',
            confidence=0.92,  # High confidence required because script will
            #  not match icon consistently on the grid. Must match on
            # overview only.
            region=(originx, originy, windowx, windowy))
        if enemy_frigate is not None:
            (enemy_frigatex, enemy_frigatey) = enemy_frigate
            print('check_for_enemies -- found hostile npc frigate at',
                  enemy_frigatex, enemy_frigatey)
            pag.moveTo(enemy_frigatex, enemy_frigatey,  # Move mouse over
                       # enemy frigate so it can be identified
                       .5, mouse.path())
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

# ALTERNATIVE CHECK FOR PLAYERS WITH ONLY ONE SCREENSHOT
def detect_pcs():
    print('detect_pcs -- called')
    conf = 0.96
    if check_for_players_var == 1:

        # take a single screenshot of the rightmost quarter of the screen to capture the overview. do this at the beginning of the
        # function only once, rather than each time a ship icon is searched for
        overview = pag.screenshot(region=((windowx - (int(windowx / 4))), originy,
            (int(windowx / 4)), windowy))

        if check_for_player_type_barge_and_industrial == 1:  

            # look for ship icon on the screenshot that was taken. keep the screenshot in memory so you don't have to wait for it to
            # write to disk
            mining_barge_and_industrial = pag.locate(
                './img/overview/player_ship_icons'
                '/archetype_icons/player_mining_barge_and_industrial.bmp', overview,
                confidence=conf,

            if mining_barge_and_industrial is not None:
                print('detect_pcs -- found mining_barge_and_industrial')
                (x, y) = mining_barge_and_industrial
                pag.moveTo(x, y,  # Move mouse over
                           # icon for debugging purposes
                           .5, mouse.path())
                return 1
        # continue to check for other player ship icons using the same overview screenshot from the beginning of the function
'''
