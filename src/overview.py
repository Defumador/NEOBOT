import random
import time
import logging

import pyautogui as pag

from src import mouse, keyboard, locate as lo
from src.vars import originx, originy, windowx, windowy

# Specify the target names you wish the script to search for in the Overview.
# For mining, this would be ore types.

ox = (originx + (windowx - (int(windowx / 3.8)))) 
oy = originy
olx = (int(windowx / 3.8))
oly = windowy

logging.basicConfig(format='(%(levelno)s) %(asctime)s - %(funcName)s -- %('
                           'message)s', level=logging.DEBUG)


# TODO: function to sort overview by distance


def is_jammed(jam_var):
    """Check for an ecm-jamming icon on the rightmost column of the
    overview."""
    if jam_var == 1:
        global oy, oly
        ox_jam = (originx + (windowx - (int(windowx / 8))))
        olx_jam = (int(windowx / 8))
        if lo.locate('./img/overview/jammed_overview.bmp',
                     region=(ox_jam, oy, olx_jam, oly)) is not None:
            logging.info('ship has been jammed!')
            return 1
        else:
            return 0
    elif jam_var == 0:
        return 0

    
def build_ship_list(detect_npcs_var, npc_frig_dest,
                npc_cruiser_bc, detect_pcs_var, pc_indy, pc_barge, pc_frig_dest,
               pc_cruiser_bc, pc_bs, pc_capindy_freighter, pc_rookie, pc_pod):
    """Build lists of npc and pc ship icons, through which another function can iterate and
    check if any of those icons are present on the overview."""
    npc_list = []
    if detect_npcs_var == 1:
        if npc_frig_dest == 1:
            npc_list.append(
                './img/overview/npc_ship_icons/npc_hostile_frigate.bmp')
        if npc_cruiser_bc == 1:
            npc_list.append(
                './img/overview/npc_ship_icons/npc_hostile_cruiser.bmp')
    pc_list = []
    if detect_pcs_var == 1:
        logging.debug('detect pcs is' + (str(detect_pcs_var)))
        logging.debug('pc bs is' + (str(pc_bs)))
        logging.debug('pc list is' + (str(pc_list)))
        if pc_indy == 1:
            pc_list.append(
                './img/overview/player_ship_icons/archetype_icons'
                '/player_industrial.bmp')
        if pc_barge == 1:
            pc_list.append(
                './img/overview/player_ship_icons/archetype_icons'
                '/player_mining_barge.bmp')
        if pc_frig_dest == 1:
            pc_list.append(
                './img/overview/player_ship_icons'
                '/archetype_icons/player_frigate_and_destroyer.bmp')
        if pc_cruiser_bc == 1:
            pc_list.append(
                './img/overview/player_ship_icons'
                '/archetype_icons/player_cruiser_and_battlecruiser.bmp')
        if pc_bs == 1:
            pc_list.append(
                './img/overview/player_ship_icons/archetype_icons'
                '/player_battleship.bmp')
        if pc_capindy_freighter == 1:
            pc_list.append(
                './img/overview/player_ship_icons/archetype_icons'
                '/player_capital_industrial_and_freighter.bmp')
        if pc_rookie == 1:
            pc_list.append(
                './img/overview/player_ship_icons/archetype_icons'
                '/player_rookie_ship.bmp')
        if pc_pod == 1:
            pc_list.append(
                './img/overview/player_ship_icons/archetype_icons'
                '/player_capsule.bmp')
        logging.debug('pc list is now' + (str(pc_list)))
    return npc_list, pc_list


def look_for_ship(npc_list, pc_list):
    """Check if any of the ship icons in the given lists are currently
    present on the overview, searching the rightmost quarter of the screen
    only."""
    # Search within the rightmost quarter of the client. Script assumes
    # overview is on the right half of the screen. This is about
    # twice as fast as searching an entire 1024x768 client window.
    
    # Use the same screenshot for both checks. 
    # If either list is empty, skip checking.
    logging.debug('npc_list is ' + (str(npc_list)) + ' and pc_list is ' + (
        str(pc_list)))

    if len(npc_list) != 0 or len(pc_list) != 0:
        overview = pag.screenshot(
            region=((originx + (windowx - (int(windowx / 3.8)))),
                    originy, (int(windowx / 3.8)), windowy))
    
        if len(npc_list) != 0:
            conf = 0.98
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
            
        if len(pc_list) != 0:
            conf = 0.95
            for pc_icon in pc_list:
                player_found = lo.olocate(pc_icon)

                if player_found is not None:
                    logging.debug('found player at' + (str(player_found)))
                    logging.debug('located icon' + (str(pc_icon)))
                    (x, y, l, w) = player_found
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


def look_for_targets(target1, target2, target3, target4, target5):
    """Iterate through a list of user-defined targets. If one is found,
    return its location to the calling function. Searches the rightmost
    quarter of the user's client only (just the overview)."""

    overview = pag.screenshot(
        region=((originx + (windowx - (int(windowx / 3.8)))),
                originy, (int(windowx / 3.8)), windowy))

    target_list = []
    # Populate target_list with only the targets that the user wishes to
    # check for, as specified by the variables at the top of this file. For
    # mining, these targets would be types of ore.
    if target1 != 0:
        target_list.append(target1)
    if target2 != 0:
        target_list.append(target2)
    if target3 != 0:
        target_list.append(target3)
    if target4 != 0:
        target_list.append(target4)
    if target5 != 0:
        target_list.append(target5)

    for target in target_list:
        target = pag.locate(target, overview, confidence=0.90)
        if target is not None:
            logging.debug('found target at ' + (str(target)))
            # (x, y, l, w) = target
            # Move mouse over target for debugging.
            # pag.moveTo((x + (originx + (windowx - (int(windowx / 3.8))))),
            #           (y + originy),
            #           1, mouse.path())
            return target
        else:
            logging.info('No targets found.')
            return 0


def wait_for_target_lock():
    """Waits until a target has been locked."""
    target_lock = pag.locateOnScreen(
        './img/indicators/target_lock_attained.bmp',
        confidence=0.95,
        region=(originx, originy,
                windowx, windowy))
    tries = 0
    while target_lock is None and tries <= 100:
        tries += 1
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


def focus_overview():
    """If undocked, click somewhere on the Overview to focus the client. If
    docked, click somewhere in the undock window below all the buttons."""
    logging.debug('focusing overview')

    x = (originx + (windowx - (int(windowx / 4.5))))
    y = originy
    randx = (random.randint(0, (int(windowx / 4.5) - 30)))
    randy = (random.randint((int(windowx / 2)), (windowy - 10)))
    pag.moveTo((x + randx), (y + randy), mouse.duration(), mouse.path())

    time.sleep(float(random.randint(50, 500)) / 1000)
    mouse.click()
    return 1


def select_overview_tab(tab):
    # Switch to the specified tab of the overview
    logging.debug('focusing ' + (str(tab)) + ' tab')
    tab_selected = pag.locateCenterOnScreen(
        './img/overview/' + tab + '_overview_tab_selected.bmp',
        # Requires very high confidence since the button looks only slightly
        # different when it's selected.
        confidence=0.998,
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


def is_target_lockable():
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


def initiate_target_lock(overview_target):
    """Targets the closest user-defined item in the Overview, assuming overview
    is sorted by distance, with closest objects at the top."""
    if overview_target is not None:
        # Break apart ore_found tuple into coordinates
        (x, y, l, w) = overview_target
        # Adjust coordinates for screen
        x = (x + (originx + (windowx - (int(windowx / 3.8)))))
        y = (y + originy)
        pag.moveTo((x + (random.randint(-100, 20))),
                   (y + (random.randint(-3, 3))),
                   mouse.duration(), mouse.path())
        mouse.click()
        keyboard.keypress('w')
        tries = 0
        while is_target_lockable() == 0 and tries <= 30:
            time.sleep(float(random.randint(1000, 2000)) / 1000)
            tries += 1
            logging.debug('target not yet within range ' + (str(tries)))
        if is_target_lockable() == 1 and tries <= 30:
            logging.debug('locking target')
            keyboard.keypress('ctrl')
            if wait_for_target_lock() == 1:
                return 1
            elif wait_for_target_lock() == 0:
                return 0
        elif is_target_lockable() == 0 and tries > 30:
            logging.warning(
                'timed out waiting for target to get within range!')
            return 0
    else:
        logging.info('no targets available')
        return 0
