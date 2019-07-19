import time
import random
import sys
import logging
import pyautogui as pag
from lib import mouse, keyboard, locate as lo
from lib.vars import originx, originy, windowx, windowy, conf

logging.basicConfig(format='(%(levelno)s) %(asctime)s - %(funcName)s -- %('
                           'message)s', level=logging.DEBUG)


def is_docked():
    """Check if the ship is currently docked by looking for the undock
     icon."""
    if lo.locate('./img/buttons/undock.bmp') is None:
        logging.debug('not docked')
        return 0
    else:
        logging.debug('docked')
        return 1


def open_ship_inv():
    """Click on the ship's inventory button in the inventory window while
    docked."""
    logging.debug('opening ship inventory')
    tries = 0
    ship_inv = lo.clocate('./img/buttons/ship_inv.bmp')

    while ship_inv is None and tries <= 25:
        logging.error('cannot find ship inventory')
        tries += 1
        time.sleep(float(random.randint(500, 2000)) / 1000)
        ship_inv = lo.clocate('./img/buttons/ship_inv.bmp')

    if ship_inv is not None and tries <= 25:
        (x, y) = ship_inv
        pag.moveTo((x + (random.randint(-4, 50))),
                   (y + (random.randint(-6, 6))),
                   mouse.duration(), mouse.path())
        mouse.click()
        return 1
    else:
        logging.error('function timed out!')
        return 0


def open_spec_inv(type):
    """If a special inventory was found (for ore, minerals, planetary
    products etc.) click on it in inventory window while docked."""
    # TODO: add support for other special inventory spots like fleet hangars
    logging.debug('opening' + type + 'inventory')
    tries = 0
    spec_inv = lo.clocate('./img/buttons/spec_inv_' + type + '.bmp')

    while spec_inv is None and tries <= 25:
        logging.error('cannot find' + type + 'inventory' + (str(tries)))
        tries += 1
        time.sleep(float(random.randint(500, 2000)) / 1000)
        spec_inv = lo.clocate('./img/buttons/spec_inv_' + type + '.bmp')

    if spec_inv is not None and tries <= 25:
        (x, y) = spec_inv
        pag.moveTo((x + (random.randint(-4, 50))),
                   (y + (random.randint(-3, 3))),
                   mouse.duration(), mouse.path())
        mouse.click()
        return 1
    else:
        logging.error('function timed out!')
        return 0


def open_station_inv():
    """Click on the station inventory button within the main inventory window
    while docked."""
    logging.debug('opening station inventory')
    tries = 0
    station_inv = lo.clocate('./img/buttons/station_inv.bmp')

    while station_inv is None and tries <= 25:
        logging.error('cannot find station inventory icon')
        tries += 1
        time.sleep(float(random.randint(500, 2000)) / 1000)
        station_inv = lo.clocate('./img/buttons/station_inv.bmp')

    if station_inv is not None and tries <= 25:
        (x, y) = station_inv
        pag.moveTo((x + (random.randint(-6, 50))),
                   (y + (random.randint(-6, 6))),
                   mouse.duration(), mouse.path())
        mouse.click()
        return 1
    else:
        logging.error('function timed out!')
        return 0


def focus_inv_window():
    """Click somewhere inside the station inventory window to focus it before
    any items are selected. Look for the sorting buttons in top right corner
    of the inventory window and position the mouse cursor relative to those
    buttons to click a non-interactive area within the inventory window."""
    tries = 0
    window = lo.clocate('./img/buttons/station_sorting.bmp')

    while window is None and tries <= 25:
        logging.error('cannot find sorting icon')
        tries += 1
        time.sleep(float(random.randint(500, 2000)) / 1000)
        window = lo.clocate('./img/buttons/station_sorting.bmp')

    if window is not None and tries <= 25:
        (x, y) = window
        pag.moveTo((x - (random.randint(0, 250))),
                   (y + (random.randint(50, 300))),
                   mouse.duration(), mouse.path())
        mouse.click()
        return 1
    else:
        logging.error('function timed out!')
        return 0


def detect_items():
    """Look at the bottom-right corner of the station inventory window for the
    '0 items found' text. If it isn't present, there must be items in the
    station's inventory."""
    if lo.locate('./img/indicators/station_inv_0_items.bmp', conf=0.9) is None:
        logging.debug('items remain')
        return 1
    elif lo.locate('./img/indicators/station_inv_0_items.bmp', conf=0.9) is not None:
        logging.debug('no more items')
        return 0


def detect_spec_inv(type):
    """Look for different kinds of special inventory locations on your ship."""
    if lo.locate('./img/buttons/spec_inv_' + type + '.bmp') is not None:
        logging.debug('found' + (str(type)) + 'inventory')
        return 1
    else:
        return 0


def spec_inv_warning():
    """Look for a popup indicating the selected inventory items aren't
    compatible with the ship's special inventory. This warning is partially
    transparent so confidence rating must be slightly lower than normal."""
    if lo.locate('./img/popups/spec_inv.bmp', conf=0.8) is not None:
        logging.debug('detected special inventory warning')
        return 1
    else:
        logging.debug('no special inventory warning')
        return 0


def set_quant_warning():
    """Check if a 'set quantity' window appears, indicating there isn't enough
    space in the ship's inventory for a full item stack."""

    if lo.locate('./img/popups/set_quant.bmp', conf=0.85) is not None:
        logging.debug('detected set quantity warning')
        time.sleep(float(random.randint(100, 800)) / 1000)
        pag.keyDown('enter')
        time.sleep(float(random.randint(5, 100)) / 1000)
        pag.keyUp('enter')
        return 1
    else:
        logging.debug('no set quantity warning')
        return 0


def not_enough_space_warning():
    # Check if a 'not enough space' warning appears, indicating the item stacks
    # selected will not fit into the ship's inventory, or inventory is
    # already full.
    if lo.locate('./img/warnings/not_enough_space.bmp') is not None:
        logging.debug('detected not enough space warning')
        time.sleep(float(random.randint(100, 800)) / 1000)
        pag.keyDown('enter')
        time.sleep(float(random.randint(5, 100)) / 1000)
        pag.keyUp('enter')
        return 1
    else:
        logging.debug('no not enough space warning')
        return 0


def undock_loop():
    """Undock from the station with the default hotkey. The undock_loop has been
    completed once the script sees the cyan ship icon in the top left corner
    of the client window, indicating a session change has just ocurred."""
    logging.info('undocking')
    pag.keyDown('ctrl')
    time.sleep(float(random.randint(100, 800)) / 1000)
    keyboard.keypress('u')
    time.sleep(float(random.randint(100, 800)) / 1000)
    pag.keyUp('ctrl')

    # Wait for the 'undock' button to change to 'undocking', indicating the
    # undock action has been confirmed.
    tries = 0

    while lo.olocate('./img/buttons/undocking.bmp', conf=0.9) is None and \
            tries <= 25:
        tries += 1
        logging.debug('waiting for session change to begin ' + (str(tries)))
        time.sleep(int((random.randint(500, 2000) / 1000)))

    if lo.olocate('./img/buttons/undocking.bmp', conf=0.9) is not None and \
            tries <= 25:
        logging.debug('session change underway ' + (str(tries)))

        # Now wait for the undock to complete by looking for the session
        # change indicator.
        tries = 0

        while lo.locate('./img/indicators/session_change_undocked.bmp',
                        conf=0.55) is None and tries <= 100:
            tries += 1
            time.sleep(int((random.randint(500, 2000) / 1000)))
            logging.debug('waiting for session change to complete ' +
                          (str(tries)))

        if lo.locate('./img/indicators/session_change_undocked.bmp',
                     conf=0.55) is not None and tries <= 100:
            logging.debug('undock completed ' + (str(tries)))
            return 1
          
        # If script times out waiting for the session change icon, simply
        # look for the undock button instead since ship has likely completed
        # an undock, but at this point the session change icon is probably
        # gone.
        elif lo.locate('./img/indicators/session_change_undocked.bmp',
                       conf=0.55) is None and tries > 100:
            if is_docked() == 1:
                logging.error('cannot undock')
                sys.exit()
            elif is_docked() == 0:
                logging.warning('undock tentatively completed')
                return 1
    elif lo.locate('./img/buttons/undocking.bmp', conf=0.9) is None and \
            tries > 25:
        logging.error('timed out waiting for session change')
        sys.exit()
