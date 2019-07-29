# encoding: utf-8
import random
import time
import logging

from src import keyboard as key, locate as lo

drones_dict = {1: "1", 2: "2", 3: "3", 4: "4", 5: "5"}


def launch_drones(drone_num):
    """Launches drones and waits for them to leave the drone bay. User must
    custom-set the "launch drones" hotkey to be Shift-l."""
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


def are_drones_launched():
    """Checks if any drones are present in the drone bay."""
    if lo.locate('./img/indicators/drones/0_drone_in_bay.bmp', conf=0.99) is \
            not None:
        logging.debug('drones are in space')
        return 1
    else:
        return 0


def recall_drones(drone_num):
    """Recalls drones and waits for them to return to the drone bay."""
    if drone_num != 0:
        time.sleep(float(random.randint(5, 500)) / 1000)
        key.hotkey('shift', 'r')

        # Wait for all drones to return to drone bay. Very sensitive to the
        # drones variable. Won't work unless the drones variable is correct.
        tries = 0
        while lo.locate('./img/indicators/drones/' + (str(drone_num))
                        + '_drone_in_bay.bmp') is None and tries <= 30:
            tries += 1
            time.sleep(float(random.randint(1000, 2000)) / 1000)

        if lo.locate('./img/indicators/drones/' + (str(drone_num))
                     + '_drone_in_bay.bmp') is not None and tries <= 30:
            logging.debug('drones returned to bay ' + (str(tries)))
            return 1

        elif lo.locate('./img/indicators/drones/' + (str(drone_num))
                       + '_drone_in_bay.bmp') is None and tries > 30:
            logging.warning('timed out waiting for drones to return '
                            + (str(tries)))
            return 0
    else:
        return 0
