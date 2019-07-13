import random
import time
import logging
# from lib.gui import module_logger

import pyautogui as pag

drones_dict = {1: "1", 2: "2", 3: "3", 4: "4", 5: "5"}

logging.basicConfig(format='(%(levelno)s) %(asctime)s - %(funcName)s -- %('
                           'message)s', level=logging.DEBUG)


def launch_drones_loop(drones):
    # User must custom-set the "launch drones" hotkey to be Shift-l
    if drones != 0:
        logging.info('launching drones')
        time.sleep(float(random.randint(10, 800)) / 1000)
        pag.keyDown('shift')
        time.sleep(float(random.randint(10, 800)) / 1000)
        pag.keyDown('l')
        time.sleep(float(random.randint(10, 800)) / 1000)
        pag.keyUp('shift')
        time.sleep(float(random.randint(10, 800)) / 1000)
        pag.keyUp('l')
        time.sleep(float(random.randint(300, 800)) / 1000)

        # Wait for drones to launch by looking for '0' in drone bay
        drones_launched_var = pag.locateOnScreen(
            './img/indicators/drones/0_drone_in_bay.bmp')
        tries = 0
        while drones_launched_var is None and tries <= 25:
            logging.debug('waiting for donres to launch ' + (str(tries)))
            time.sleep(float(random.randint(500, 2000)) / 1000)
            drones_launched_var = pag.locateOnScreen(
                './img/indicators/drones/0_drone_in_bay.bmp')
            tries += 1
        if drones_launched_var is not None and tries <= 25:
            logging.debug('drones launched ' + (str(tries)))
            return 1
        else:
            logging.warning('timed out waiting for drones to launch')
            return 1
    else:
        return 1


def detect_drones_launched():
    drones_launched_var = pag.locateOnScreen(
        './img/indicators/drones/0_drone_in_bay.bmp')
    if drones_launched_var is not None:
        logging.debug('drones are in space')
        return 1
    else:
        return 0


def recall_drones_loop(drones):
    if drones != 0:
        time.sleep(float(random.randint(10, 800)) / 1000)
        pag.keyDown('shift')
        time.sleep(float(random.randint(10, 800)) / 1000)
        pag.keyDown('r')
        time.sleep(float(random.randint(10, 800)) / 1000)
        pag.keyUp('shift')
        time.sleep(float(random.randint(10, 800)) / 1000)
        pag.keyUp('r')

        # Wait for all drones to return to drone bay. Very sensitive to the
        # drones variable. Won't work unless the drones variable is correct.
        drones_recalled = pag.locateOnScreen('./img/indicators/drones/' + (
            drones_dict[drones]) + '_drone_in_bay.bmp')
        tries = 1
        while drones_recalled is None and tries <= 25:
            time.sleep(float(random.randint(1000, 2000)) / 1000)
            drones_recalled = pag.locateOnScreen('./img/indicators/drones/' + (
                drones_dict[drones]) + '_drone_in_bay.bmp')
            tries += 1
        if drones_recalled is not None and tries <= 25:
            logging.debug('drones returned to bay ' + (str(tries)))
            return 1
        else:
            logging.warning('timed out waiting for drones to return ' + (str(
                tries)))
            return 1
    else:
        return 0
