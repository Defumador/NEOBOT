import random
import time
import logging

from lib import keyboard as key, locate as lo

import pyautogui as pag

drones_dict = {1: "1", 2: "2", 3: "3", 4: "4", 5: "5"}

logging.basicConfig(format='(%(levelno)s) %(asctime)s - %(funcName)s -- %('
                           'message)s', level=logging.DEBUG)


def launch_drones_loop(drone_num):
    # User must custom-set the "launch drones" hotkey to be Shift-l
    if drone_num != 0:
        logging.info('launching drones')
        time.sleep(float(random.randint(5, 500)) / 1000)
        key.hotkey('shift', 'l')

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
            return 0
    else:
        return 1


def detect_drones_launched():
    if lo.locate('./img/indicators/drones/0_drone_in_bay.bmp') is not None:
        logging.debug('drones are in space')
        return 1
    else:
        return 0


def recall_drones_loop(drone_num):
    if drone_num != 0:
        time.sleep(float(random.randint(5, 500)) / 1000)
        key.hotkey('shift', 'r')

        # Wait for all drones to return to drone bay. Very sensitive to the
        # drones variable. Won't work unless the drones variable is correct.
        tries = 0
        while lo.locate('./img/indicators/drones/' + drone_num
                        + '_drone_in_bay.bmp') is None and tries <= 25:
            tries += 1
            time.sleep(float(random.randint(1000, 2000)) / 1000)

        if lo.locate('./img/indicators/drones/' + drone_num
                     + '_drone_in_bay.bmp') is not None and tries <= 25:
            logging.debug('drones returned to bay ' + (str(tries)))
            return 1

        else:
            logging.warning('timed out waiting for drones to return '
                            + (str(tries)))
            return 0
    else:
        return 0
