import logging
from src.vars import originx, originy, windowx, windowy

import pyautogui as pag

overviewx = (originx + (windowx - (int(windowx / 3.8))))
overviewlx = (int(windowx / 3.8))


# OPEN CV TEMPLATEMATCH EXAMPLE #########################################
# TODO: transition to opencv template matching instead of pyautogui
import cv2
import numpy as np
from matplotlib import pyplot as plt

def cvlocate_example(image, conf=0.95, region=(originx, originy, windowx, windowy)):
    client = pag.screenshot(region=(originx, originy, windowx, windowy)
    img = cv2.imread(image,0)
    img2 = img.copy()
    template = cv2.imread(client,0)
    w, h = template.shape[::-1]

    # All the 6 methods for comparison in a list
    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
                'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

    for meth in methods:
        img = img2.copy()
        method = eval(meth)

        # Apply template Matching
        res = cv2.matchTemplate(img,template,method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        cv2.rectangle(img,top_left, bottom_right, 255, 2)

        plt.subplot(121),plt.imshow(res,cmap = 'gray')
        plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(img,cmap = 'gray')
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        plt.suptitle(meth)

        plt.show()
#############################################################################  

# CV locate for speed benchmarking
                            
 def cvlocate(image, threshold=0.9):
    client = pag.screenshot(region=(originx, originy, windowx, windowy))
    # for cv2.imread, a '0' denotes converting the image to grayscale
    # replace the 0 with 'CV_LOAD_IMAGE_ANYDEPTH' for color
    # see https://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html#Mat%20imread(const%20string&%20filename,%20int%20flags)
    img = cv2.imread(image,0)
    img2 = img.copy()
    template = cv2.imread(client,0)
    w, h = template.shape[::-1]

    img = img2.copy()
    method = cv2.TM_CCOEFF_NORMED

    # Apply template Matching
    res = cv2.matchTemplate(img,template,method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if max_loc > threshold
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        cv2.rectangle(img,top_left, bottom_right, 255, 2)

        plt.subplot(121),plt.imshow(res,cmap = 'gray')
        plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(img,cmap = 'gray')
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])                  
        plt.suptitle(method)
                            
        plt.show()
        print('client is', client)
                            
        print('image is', image)
        print('img is', img)
        print('img2 is', img2)
                            
        print('top_left is', top_left)
        print('bottom_right is', bottom_right)
                            
        print('res is', res)
                            
        print('min_val is', min_val)
        print('max_val is', max_val)
        print('min_loc is', min_loc)
        print('max_loc is', max_loc)
                            
    else:
        print('didnt reach threshold')
    return
##############################################################   
                            
                            
# screen class from https://github.com/vbidin/aspirant/blob/master/src/screen.py

class Screen:

    def __init__(self):
        pyautogui.PAUSE = 0
        self.root = 'img'
        self.ext = '.png'
        self.source_path = self.root + '\\' + 'source' + self.ext
        self.method = eval('cv2.TM_CCORR_NORMED')

    def read_source(self):
        path = self.path('source')
        pyautogui.screenshot(path)
        return cv2.imread(path, 0)
        
    def read_template(self, path):
        img = cv2.imread(path, 0)
        if img is None:
            raise ValueError('Invalid image path: ' + path)
        return img
        
    def path(self, name):
        return self.root + '\\' + name + self.ext
        
    def locate(self, name, threshold=0):
        path = self.path(name)
        source = self.read_source()
        template = self.read_template(path)
        
        res = cv2.matchTemplate(source, template, self.method)
        min, max, min_loc, max_loc = cv2.minMaxLoc(res)
        print(name + " similiarity: " + str(max))
        
        if max > threshold:
            return 1
        
        x, y = max_loc
        w, h = template.shape[::-1]        
        return x, y, w, h
#############################################################################

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
