import random
import time
import logging

import pyautogui as pag

from lib import mouse
from lib.vars import originx, originy, windowx, windowy

detect_npcs_var = 1

detect_npc_frigate_and_destroyer = 0
detect_npc_cruiser_and_battlecruiser = 1
detect_npc_battleship = 1

detect_pcs_var = 1

detect_pc_industrial = 1
detect_pc_mining_barge = 1
detect_pc_frigate_and_destroyer = 1
detect_pc_capital_industrial_and_freighter = 1
detect_pc_cruiser_and_battlecruiser = 1
detect_pc_battleship = 1
detect_pc_rookie_ship = 1
detect_pc_capsule = 1

logging.basicConfig(format='(%(levelno)s) %(asctime)s - %(funcName)s -- %('
                           'message)s', level=logging.DEBUG)


def detect_target_lock():
    # Wait for ship to finish acquiring target lock.
    target_lock = pag.locateOnScreen(
        './img/indicators/target_lock_attained.bmp',
        confidence=0.95,
        region=(originx, originy,
                windowx, windowy))
    tries = 1
    while target_lock is None and tries <= 100:
        target_lock = pag.locateOnScreen(
            './img/indicators/target_lock_attained.bmp',
            confidence=0.95,
            region=(originx, originy,
                    windowx, windowy))
        time.sleep(float(random.randint(100, 500)) / 1000)
        logging.debug('locking target' + (str(tries)))
    if target_lock is not None and tries <= 100:
        logging.debug('lock attained')
        return 1
    elif target_lock is None and tries > 100:
        logging.error('timed out waiting for target lock')
        return 0


def detect_jam():
    # Check overview window for target jamming icon on the right edge
    overview = pag.screenshot('test.bmp',
                              region=(
                                  (originx + (windowx - (int(windowx / 8)))),
                                  originy, (int(windowx / 8)), windowy))
    jammed = pag.locate(
        './img/overview/jammed_overview.bmp', overview, confidence=0.95)
    if jammed is not None:
        logging.info('ship has been jammed!')
        return 1
    else:
        return 0


def focus_overview_tab(tab):
    # Switch to the specified tab of the overview
    logging.debug('focusing ' + (str(tab)) + ' tab')
    tab_selected = pag.locateCenterOnScreen(
        './img/overview/' + tab + '_overview_tab_selected.bmp',
        # Requires very high confidence since the button looks only slightly
        # different when it's selected.
        confidence=0.992,
        region=(originx, originy,
                windowx, windowy))
    if tab_selected is not None:
        logging.debug('tab ' + (str(tab)) + ' -- already selected')
        return 1
    else:
        tab_unselected = pag.locateCenterOnScreen(
            './img/overview/' + tab + '_overview_tab.bmp',
            confidence=0.95,
            region=(originx, originy,
                    windowx, windowy))

        if tab_unselected is not None:
            (x, y) = tab_unselected
            pag.moveTo((x + (random.randint(-12, 12))),
                       (y + (random.randint(-6, 6))),
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
        logging.debug('within targeting range')
        return 1
    elif target_lock_available is None:
        logging.debug('outside of targeting range')
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
                logging.debug('found ship at ' + (str(hostile_npc_found)))
                logging.debug('located icon ' + (str(npc_icon)))
                # Break up the tuple so mouse can point at icon for debugging.
                # (x, y, t, w) = hostile_npc_found
                # Coordinates must compensate for the altered coordinate-space
                # of the screenshot.
                # pag.moveTo((x + (originx + (windowx - (int(windowx / 2))))),
                #           (y + originy),
                #           0, mouse.path())
                return 1
        logging.debug('passed npc check')
        return 0
    else:
        return 0


def detect_pcs():
    # Check for player characters by looking for player ship icons in the
    # overview.
    # print('detect_pcs -- called')
    conf = 0.95
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
        if detect_pc_industrial == 1:
            pc_list.append(
                './img/overview/player_ship_icons/archetype_icons'
                '/player_industrial.bmp')
        if detect_pc_mining_barge == 1:
            pc_list.append(
                './img/overview/player_ship_icons/archetype_icons'
                '/player_mining_barge.bmp')
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
                logging.debug('found player at' + (str(player_found)))
                logging.debug('located icon' + (str(pc_icon)))
                # Break up the tuple so mouse can point at icon for debugging.
                (x, y, t, w) = player_found
                # Coordinates must compensate for the altered coordinate-space
                # of the screenshot.
                pag.moveTo((x + (originx + (windowx - (int(windowx / 3.8))))),
                           (y + originy),
                           0, mouse.path())
                return 1
        logging.debug('passed pc check')
        return 0
    else:
        return 0


def focus_client():
    # Click on a blank area in the client, assuming user has
    # properly configured the UI.
    logging.debug('focusing client')
    pag.moveTo((originx + (random.randint(50, 300))),
               (originy + (random.randint(300, 500))),
               mouse.duration(), mouse.path())
    time.sleep(float(random.randint(50, 500)) / 1000)
    mouse.click()
    return 1
