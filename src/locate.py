# encoding: utf-8
# import pyximport
# pyximport.install(pyimport=True)
import logging
import sys
from src.vars import originx, originy, windowx, windowy
import pyautogui as pag


def mlocate(needle, haystack=0, conf=0.95, loctype='l', grayscale=False):
    """Searches the haystack image for the needle image, returning a tuple
    of the needle's coordinates within the haystack. If a haystack image is
    not provided, searches the client window or the overview window,
    as specified by the loctype parameter."""
    if haystack != 0:
        locate_var = pag.locate(needle, haystack, confidence=conf,
                                grayscale=grayscale)
        if locate_var is not None:
            logging.debug('found needle  ' + (str(needle)) +
                          ' in haystack' + (str(haystack)) + ', ' +
                          (str(locate_var)))
            return locate_var
        else:
            logging.debug('cant find needle  ' + (str(needle)) +
                          ' in haystack' + (str(haystack)) + ', ' +
                          (str(locate_var)) + ', conf=' + (str(conf)))
            return 0

    if haystack == 0 and loctype == 'l':  # 'l' for regular 'locate'
        locate_var = pag.locateOnScreen(needle, confidence=conf, region=(
            originx, originy, windowx, windowy), grayscale=grayscale)
        if locate_var is not None:
            logging.debug('found l image ' + (str(needle)) + ', ' + (str(
                locate_var)))
            # If the center of the image is not needed, don't return any
            # coordinates.
            return 1
        elif locate_var is None:
            logging.debug('cannot find l image ' + (
                    str(needle) + ' conf=' + (str(conf))))
            return 0

    if haystack == 0 and loctype == 'c':  # 'c' for 'center'
        locate_var = pag.locateCenterOnScreen(needle, confidence=conf, region=(
            originx, originy, windowx, windowy), grayscale=grayscale)
        if locate_var is not None:
            logging.debug('found c image ' + (str(needle)) + ', ' + (str(
                locate_var)))
            # Return the xy coordinates for the center of the image, relative to
            # the coordinate plane of the haystack.
            return locate_var
        elif locate_var is None:
            logging.debug('cannot find c image ' + (
                    str(needle) + ', conf=' + (str(conf))))
            return 0

    if haystack == 0 and loctype == 'o':  # 'o' for 'overview'
        overviewx = (originx + (windowx - (int(windowx / 3.8))))
        overviewlx = (int(windowx / 3.8))
        locate_var = pag.locateOnScreen(needle, confidence=conf, region=(
            overviewx, originy, overviewlx, windowy), grayscale=grayscale)
        if locate_var is not None:
            logging.debug('found o image ' + (str(needle)) + ', ' + (str(
                locate_var)))
            return 1
        elif locate_var is None:
            logging.debug('cannot find o image ' + (
                    str(needle) + ', conf=' + (str(conf))))
            return 0

    if haystack == 0 and loctype == 'co':  # 'co' for 'center of overview'
        overviewx = (originx + (windowx - (int(windowx / 3.8))))
        overviewlx = (int(windowx / 3.8))
        locate_var = pag.locateCenterOnScreen(needle, confidence=conf, region=(
            overviewx, originy, overviewlx, windowy), grayscale=grayscale)
        if locate_var is not None:
            logging.debug('found co image ' + (str(needle)) + ', ' + (str(
                locate_var)))
            return locate_var
        elif locate_var is None:
            logging.debug('cannot find co image ' + (
                    str(needle) + ', conf=' + (str(conf))))
            return 0

    else:
        logging.critical('incorrect function parameters')
        sys.exit()
