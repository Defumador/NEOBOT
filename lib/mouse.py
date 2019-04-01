import time
import random

import pyautogui as pag


def click():
    # Click the primary mouse button, waiting both before and after for a
    # randomized period of time.
    time.sleep(float(random.randint(0, 500)) / 1000)
    pag.click()  # (duration=(float(random.randint(500, 2000) / 1000)))
    time.sleep(float(random.randint(0, 500)) / 1000)
    return


def click_right():
    time.sleep(float(random.randint(0, 500)) / 1000)
    pag.click(
        button='right')  # duration=(float(random.randint(500, 2500) /
    # 1000)))
    time.sleep(float(random.randint(0, 500)) / 1000)
    return


def duration():
    # Randomize the amount of time the mouse cursor takes to move to a
    # new location.
    movetimevar = (float(random.randint(200, 1500) / 1000))
    return movetimevar


def path():
    # Randomize the movement behavior of the mouse cursor as it moves to a
    # new location.
    rand = random.randint(1, 2)
    if rand == 1:
        return pag.easeInQuad
    elif rand == 2:
        return pag.easeOutQuad
