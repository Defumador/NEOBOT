# encoding: utf-8
import logging
from src.vars import originx, originy, windowx, windowy

import pyautogui as pag


def mlocate(needle, haystack=0, conf=0.95, loctype='none', grayscale=False):
    """Searches the haystack image for the needle image, returning a tuple of the needle's
    coordinates within the haystack. If a haystack image is not provided, searches
    the client window or the overview window, as specified by the loctype parameter."""
    
    if haystack == 0 and loctype == 'l':
        locate_var = pag.locateOnScreen(needle, confidence=conf, region=(originx, originy, windowx, windowy))
        if locate_var is not None:
            logging.debug('found image ' + (str(needle)))
            return locate_var
        elif locate_var is None:
            logging.debug('cannot find standard image ' + (
                    str(needle) + ' confidence is ' + (str(conf))))
            return 0
        
    if haystack == 0 and loctype == 'c':
        locate_var = pag.locateCenterOnScreen(needle, confidence=conf, region=(originx, originy, windowx, windowy))
        if locate_var is not None:
            logging.debug('found image ' + (str(needle)))
            return locate_var
        elif locate_var is None:
            logging.debug('cannot find standard image ' + (
                    str(needle) + ' confidence is ' + (str(conf))))
            return 0
        
    if haystack == 0 and loctype == 'o':
        overviewx = (originx + (windowx - (int(windowx / 3.8))))
        overviewlx = (int(windowx / 3.8))
        locate_var = pag.locateOnScreen(needle, confidence=conf, region=(overviewx, originy, overviewlx, windowy))
        if locate_var is not None:
            logging.debug('found image ' + (str(needle)))
            return locate_var
        elif locate_var is None:
            logging.debug('cannot find standard image ' + (
                    str(needle) + ' confidence is ' + (str(conf))))
            return 0
        
    if haystack == 0 and loctype == 'co':
        overviewx = (originx + (windowx - (int(windowx / 3.8))))
        overviewlx = (int(windowx / 3.8))
        locate_var = pag.locateCenterOnScreen(needle, confidence=conf, region=(overviewx, originy, overviewlx, windowy))
        if locate_var is not None:
            logging.debug('found image ' + (str(needle)))
            return locate_var
        elif locate_var is None:
            logging.debug('cannot find standard image ' + (
                    str(needle) + ' confidence is ' + (str(conf))))
            return 0
        
    if haystack != 0:
        locate_var = pag.locate(needle, haystack, confidence=conf, grayscale=grayscale)
        if locate_var is not None:
            logging.debug('found needle image ' + (str(needle)) + ' within haystack image' + (str(haystack)))
            return locate_var
        else:
            logging.debug('cannot find image ' + (
                    str(needle) + ' confidence is ' + (str(conf))))
            return 0
        
    else:
        logging.error('incorrect function parameters')
        sys.exit()
