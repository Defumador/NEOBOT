import random
import logging
from lib.vars import originx, originy, windowx, windowy

import pyautogui as pag

overviewx = (originx + (windowx - (int(windowx / 3.8))))
overviewlx = (int(windowx / 3.8))


def locate(image, conf=0.95, region=(originx, originy, windowx, windowy)):
    locate_var = pag.locateOnScreen(image, confidence=conf, region=region)
    if locate_var is not None:
        logging.debug('found image ' + (str(image)))
        return locate_var
    elif locate_var is None:
        # logging.debug('cannot find image ' + (str(image) + ' confidence is
        ## ' + (
        #    str(conf))))
        return locate_var


def clocate(image, conf=0.95, region=(originx, originy, windowx, windowy)):
    # 'clocate' = 'center locate'
    clocate_var = pag.locateCenterOnScreen(image, confidence=conf,
                                           region=region)
    if clocate_var is not None:
        logging.debug('found image ' + (str(image)))
        return clocate_var
    elif clocate_var is None:
        logging.debug(
            'cannot find image ' + (str(image) + ' confidence is ' + (
                str(conf))))
        return clocate_var


def olocate(image, conf=0.95, region=(overviewx, originy, overviewlx,
                                      windowy)):
    # locate within the overview window only
    olocate_var = pag.locateOnScreen(image, confidence=conf, region=region)
    if olocate_var is not None:
        logging.debug('found image ' + (str(image)))
        return olocate_var
    elif olocate_var is None:
        # logging.debug(
        #    'cannot find image ' + (str(image) + ' confidence is ' + (
        #        str(conf))))
        return olocate_var


def oclocate(image, conf=0.95, region=(overviewx, originy, overviewlx,
                                       windowy)):
    # locate center within the overview window only
    oclocate_var = pag.locateCenterOnScreen(image, confidence=conf,
                                            region=region)
    if oclocate_var is not None:
        logging.debug('found image ' + (str(image)))
        return oclocate_var
    elif oclocate_var is None:
        # logging.debug(
        #    'cannot find image ' + (str(image) + ' confidence is ' + (
        #        str(conf))))
        return oclocate_var
