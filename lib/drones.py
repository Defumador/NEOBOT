import random
import time
import logging

from lib import locate as lo

import pyautogui as pag

drones_dict = {1: "1", 2: "2", 3: "3", 4: "4", 5: "5"}

logging.basicConfig(format='(%(levelno)s) %(asctime)s - %(funcName)s -- %('
                           'message)s', level=logging.DEBUG)


def launch_drones_loop(drones):
    # User must custom-set the "launch drones" hotkey to be Shift-l
    if drones != 0:
        logging.info('launching drones')
        time.sleep(float(random.randint(5, 500)) / 1000)
        pag.keyDown('shift')
        time.sleep(float(random.randint(5, 500)) / 1000)
        pag.keyDown('l')
        time.sleep(float(random.randint(5, 500)) / 1000)
        pag.keyUp('shift')
        time.sleep(float(random.randint(5, 500)) / 1000)
        pag.keyUp('l')
        time.sleep(float(random.randint(100, 500)) / 1000)

        tries = 0
        while lo.locate('./img/indicators/drones/0_drone_in_bay.bmp') is None \
                and tries <= 25:
            tries += 1
            logging.debug('waiting for drones to launch ' + (str(tries)))
            time.sleep(float(random.randint(500, 2000)) / 1000)

        if lo.locate('./img/indicators/drones/0_drone_in_bay.bmp') is not \
                None and tries <= 25:
            logging.debug('drones launched ' + (str(tries)))
            return 1

        else:
            logging.warning('timed out waiting for drones to launch')
            return 1
    else:
        return 1


def detect_drones_launched():
    if lo.locate('./img/indicators/drones/0_drone_in_bay.bmp') is not None:
        logging.debug('drones are in space')
        return 1
    else:
        return 0


def recall_drones_loop(drones):
    if drones != 0:
        time.sleep(float(random.randint(5, 500)) / 1000)
        pag.keyDown('shift')
        time.sleep(float(random.randint(5, 500)) / 1000)
        pag.keyDown('r')
        time.sleep(float(random.randint(5, 500)) / 1000)
        pag.keyUp('shift')
        time.sleep(float(random.randint(5, 500)) / 1000)
        pag.keyUp('r')
        time.sleep(float(random.randint(5, 500)) / 1000)

        # Wait for all drones to return to drone bay. Very sensitive to the
        # drones variable. Won't work unless the drones variable is correct.
        tries = 0
        while lo.locate('./img/indicators/drones/' + (drones_dict[drones])
                        + '_drone_in_bay.bmp') is None and tries <= 25:
            tries += 1
            time.sleep(float(random.randint(1000, 2000)) / 1000)

        if lo.locate('./img/indicators/drones/' + (drones_dict[drones])
                     + '_drone_in_bay.bmp') is not None and tries <= 25:
            logging.debug('drones returned to bay ' + (str(tries)))
            return 1

        else:
            logging.warning('timed out waiting for drones to return '
                            + (str(tries)))
            return 1
    else:
        return 0
