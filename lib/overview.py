import random
import time

import pyautogui as pag

from lib import mouse
from lib.vars import originx, originy, windowx, windowy

detect_npcs_var = 1

detect_npc_frigate_and_destroyer = 0
detect_npc_cruiser_and_battlecruiser = 1
detect_npc_battleship = 1

detect_pcs_var = 1

detect_pc_mining_barge_and_industrial = 1
detect_pc_frigate_and_destroyer = 1
detect_pc_capital_industrial_and_freighter = 1
detect_pc_cruiser_and_battlecruiser = 1
detect_pc_battleship = 1
detect_pc_rookie_ship = 1
detect_pc_capsule = 1


def detect_target_lock():
    # Wait for ship to finish acquiring target lock.
    target_lock = pag.locateOnScreen(
        './img/indicators/target_lock_attained.bmp',
        confidence=0.95,
        region=(originx, originy,
                windowx, windowy))
    tries = 1
    while target_lock is None and tries <= 25:
        target_lock = pag.locateOnScreen(
            './img/indicators/target_lock_attained.bmp',
            confidence=0.95,
            region=(originx, originy,
                    windowx, windowy))
        time.sleep(float(random.randint(100, 500)) / 1000)
    if target_lock is not None and tries <= 25:
        print('detect_target_lock -- lock attained')
        return 1
    else:
        print('detect_target_lock -- timed out waiting for lock')
        return 0


def focus_general_tab():
    # Switch to the default 'General' tab of the overview to check for
    # other
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
        confidence=0.995,
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


def target_available():
    # Look for the target icon in the 'selected item' window, indicating
    # target is close enough in order to achieve a lock.
    target_lock_available = pag.locateOnScreen(
        './img/indicators/target_lock_available.bmp',
        confidence=0.9999,  # High confidence required since greyed-out icon
        # looks so similar to enabled icon.
        region=(originx, originy, windowx, windowy), grayscale=True)
    if target_lock_available is not None:
        print('target_available -- within targeting range')
        return 1
    elif target_lock_available is None:
        print('target_available -- outside of targeting range')
        return 0


def detect_npcs():
    # Check for hostile non-player characters by looking for red ship icons in
    # the overview.
    # print('detect_npcs -- called')
    conf = 0.98
    if detect_npcs_var == 1:

        # Search within the rightmost third of the client. Bot assumes
        # overview is on the right half of the screen. This is about
        # twice as fast as searching the entire 1024x768 client.
        overview = pag.screenshot(
            region=((originx + (windowx - (int(windowx / 3.8)))),
                    originy, (int(windowx / 3.8)), windowy))

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
        # if detect_npc_battleship == 1:
        #    npc_list.append(
        #        './img/overview/npc_ship_icons/npc_hostile_battleship.bmp')

        # Scan the 'overview' screenshot for each player icon in the list.
        for npc_icon in npc_list:
            hostile_npc_found = pag.locate(npc_icon, overview, confidence=conf)

            if hostile_npc_found is not None:
                print('detect_npcs -- found ship at', hostile_npc_found)
                print('located icon', npc_icon)
                # Break up the tuple so mouse can point at icon for debugging.
                # (x, y, t, w) = hostile_npc_found
                # Coordinates must compensate for the altered coordinate-space
                # of the screenshot.
                # pag.moveTo((x + (originx + (windowx - (int(windowx / 2))))),
                #           (y + originy),
                #           0, mouse.path())
                return 1
        print('detect npcs -- passed')
        return 0
    else:
        return 0


def detect_pcs():
    # Check for player characters by looking for player ship icons in the
    # overview.
    # print('detect_pcs -- called')
    conf = 0.98
    if detect_pcs_var == 1:

        # Search within the rightmost third of the client. Bot assumes
        # overview is on the right half of the screen. This is about
        # twice as fast as searching the entire 1024x768 client.
        overview = pag.screenshot(
            region=((originx + (windowx - (int(windowx / 3.8)))),
                    originy, (int(windowx / 3.8)), windowy))

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
                pag.moveTo((x + (originx + (windowx - (int(windowx / 3.8))))),
                           (y + originy),
                           0, mouse.path())
                return 1
        print('detect pcs -- passed')
        return 0
    else:
        return 0


def focus_overview():
    # Click on the overview window to focus the eve client window.
    print('nav.focus_overview -- called')
    pag.moveTo((windowx - (random.randint(10, 90))),
               (75 + (random.randint(0, (windowy - 10)))),
               mouse.duration(), mouse.path())
    time.sleep(float(random.randint(50, 500)) / 1000)
    mouse.click()
    return 1
