# encoding: utf-8
import logging
from src.vars import originx, originy, windowx, windowy

import pyautogui as pag

overviewx = (originx + (windowx - (int(windowx / 3.8))))
overviewlx = (int(windowx / 3.8))


def hslocate(needle, haystack=0, conf=0.95, grayscale=False):
    """Searches the haystack image for the provided needle image, returns a tuple.
    If a haystack image is not provided, search the client window instead."""
    if haystack == 0:
        locate_var = pag.locateOnScreen(needle, confidence=conf, region=(originx, originy, windowx, windowy))
        if locate_var is not None:
            logging.debug('found image ' + (str(needle)))
            return locate_var
        elif locate_var is None:
            logging.debug('cannot find standard image ' + (
                    str(needle) + ' confidence is ' + (str(conf))))
            return 0
    else:
        locate_var = pag.locate(needle, haystack, confidence=conf, grayscale=grayscale)
        if locate_var is not None:
            logging.debug('found needle image ' + (str(needle)) + ' within haystack image' + (str(haystack)))
            return locate_var
        else:
            logging.debug('cannot find image ' + (
                    str(needle) + ' confidence is ' + (str(conf))))
            return 0


def locate(image, conf=0.95, region=(originx, originy, windowx, windowy)):
    """Searches the client window for the provided image, returns a tuple."""
    locate_var = pag.locateOnScreen(image, confidence=conf, region=region)
    if locate_var is not None:
        logging.debug('found image ' + (str(image)))
        return locate_var
    elif locate_var is None:
        # logging.debug('cannot find image ' + (
        #            str(image) + ' confidence is ' + (str(conf))))
        return locate_var


def clocate(image, conf=0.95, region=(originx, originy, windowx, windowy)):
    """Searches the client window for the center coordinates of the provided
    image, returns x and y coordinates."""
    # 'clocate' = 'center locate'
    clocate_var = pag.locateCenterOnScreen(image, confidence=conf,
                                           region=region)
    if clocate_var is not None:
        logging.debug('found image ' + (str(image)))
        return clocate_var
    elif clocate_var is None:
        # logging.debug('cannot find image ' + (
        #            str(image) + ' confidence is ' + (str(conf))))
        return clocate_var


def olocate(image, conf=0.95, region=(overviewx, originy, overviewlx,
                                      windowy)):
    """Searches the rightmost quarter of the client window (the 'o' stands
    for 'overview,' assuming the overview is attached to the right side of
    the client). Searches for the provided image, returns a tuple"""
    olocate_var = pag.locateOnScreen(image, confidence=conf, region=region)
    if olocate_var is not None:
        logging.debug('found image ' + (str(image)))
        return olocate_var
    elif olocate_var is None:
        # logging.debug('cannot find image ' + (
        #            str(image) + ' confidence is ' + (str(conf))))
        return olocate_var


def oclocate(image, conf=0.95, region=(overviewx, originy, overviewlx,
                                       windowy)):
    """Searches the rightmost quarter of the client window (the 'o' stands
    for 'overview,' assuming the overview is attached to the right side of
    the client). Searches for the center coordinates of the provided image,
    returns x and y coordinates."""
    oclocate_var = pag.locateCenterOnScreen(image, confidence=conf,
                                            region=region)
    if oclocate_var is not None:
        logging.debug('found image ' + (str(image)))
        return oclocate_var
    elif oclocate_var is None:
        # logging.debug('cannot find image ' + (
        #            str(image) + ' confidence is ' + (str(conf))))
        return oclocate_var
