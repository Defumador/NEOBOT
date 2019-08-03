# encoding: utf-8
# import pyximport
# pyximport.install(pyimport=True)
import time
import random
import pyautogui as pag
from src.vars import originx, originy, windowx, windowy

#####################################################################
# Bezier curve movement testing
# from https://stackoverflow.com/questions/44467329
# /pyautogui-mouse-movement-with-bezier-curve

import scipy
from scipy import interpolate


def bezmove():
    # This function is currently not implemented as it is not yet working.
    cp = random.randint(3, 5)  # Number of control points. Must be at least 2.
    x1, y1 = pag.position()  # Starting position
    x2, y2 = 444, 631  # Destination

    # Distribute control points between start and destination evenly.
    x = scipy.linspace(x1, x2, num=cp, dtype='int')
    y = scipy.linspace(y1, y2, num=cp, dtype='int')

    # Randomise inner points a bit (+-RND at most).
    RND = 10
    xr = scipy.random.randint(-RND, RND, size=cp)
    yr = scipy.random.randint(-RND, RND, size=cp)
    xr[0] = yr[0] = xr[-1] = yr[-1] = 0
    x += xr
    y += yr

    # Approximate using Bezier spline.
    degree = 3 if cp > 3 else cp - 1  # Degree of b-spline. 3 is recommended.
    # Must be less than number of control points.
    tck, u = scipy.interpolate.splprep([x, y], k=degree)
    u = scipy.linspace(0, 1, num=max(pag.size()))
    points = scipy.interpolate.splev(u, tck)

    # Move mouse.
    duration = 0.2
    timeout = duration / len(points[0])
    for point in zip(*(i.astype(int) for i in points)):
        pag.platformModule._moveTo(*point)
        time.sleep(timeout)


################################################################################


def move_away(direction):
    """Moves the mouse to a random spot on right half or the left half of
    the client window, away from wherever it clicked,
    to prevent tooltips from interfering with the script."""
    time.sleep(float(random.randint(0, 500)) / 1000)
    if direction == 'r':
        print('right')
        pag.moveTo((random.randint(
            ((windowx - 100) - (windowx / 2)), (windowx - 100))),
            (random.randint(10, (windowy - 100))),
            duration(), path())
        time.sleep(float(random.randint(0, 500)) / 1000)
        return

    elif direction == 'l':
        print('left')
        pag.moveTo((random.randint(10, ((windowx - 100) - (windowx / 2)))),
                   (random.randint(10, (windowy - 100))),
                   duration(), path())
        time.sleep(float(random.randint(0, 500)) / 1000)
        return


def move_to_neutral():
    """Moves the mouse to a 'neutral zone', away from any buttons or tooltop
    icons that could get in the way of the script. Designed for the miner()
    gui layout."""
    pag.moveTo((originx + (random.randint(50, 300))),
               (originy + (random.randint(300, 500))),
               duration(), path())
    return 1


def click():
    """Clicks the primary mouse button, waiting both before and after for a
    randomized period of time."""
    time.sleep(float(random.randint(0, 500)) / 1000)
    pag.click(duration=(float(random.randint(0, 100) / 1000)))
    time.sleep(float(random.randint(0, 500)) / 1000)
    return


def click_right():
    """Clicks the secondary mouse button, waiting both before and after for a
    randomized period of time."""
    time.sleep(float(random.randint(0, 500)) / 1000)
    pag.click(button='right', duration=(float(random.randint(0, 100) / 1000)))
    time.sleep(float(random.randint(0, 500)) / 1000)
    return


def duration():
    """Randomizes the amount of time the mouse cursor takes to move to a
    new location."""
    movetimevar = (float(random.randint(50, 1500) / 1000))
    return movetimevar


def path():
    """Randomizes the movement behavior of the mouse cursor as it moves to a
    new location."""
    # TODO: implement bezier-curve mouse behavior
    # https://stackoverflow.com/questions/44467329
    # /pyautogui-mouse-movement-with-bezier-curve
    rand = random.randint(1, 22)
    
    if rand == 1:
        return pag.easeInQuad
    elif rand == 2:
        return pag.easeOutQuad
    elif rand == 3:
        return pag.easeInOutQuad
    
    elif rand == 4:
        return pag.easeInQuart
    elif rand == 5:
        return pag.easeOutQuart
    elif rand == 6:
        return pag.easeInOutQuart
    
    elif rand == 7:
        return pag.easeInQuint
    elif rand == 8:
        return pag.easeOutQuint
    elif rand == 9:
        return pag.easeInOutQuint
    
    elif rand == 10:
        return pag.easeInBack
    elif rand == 11:
        return pag.easeOutBack
    elif rand == 12:
        return pag.easeInOutBack
    
    elif rand == 13:
        return pag.easeInCirc
    elif rand == 14:
        return pag.easeOutCirc
    elif rand == 15:
        return pag.easeInOutCirc
    
    elif rand == 16:
        return pag.pytweening.easeInSine
    elif rand == 17:
        return pag.pytweening.easeOutSine
    elif rand == 18:
        return pag.pytweening.easeInOutSine
    
    elif rand == 19:
        return pag.pytweening.linear

    elif rand == 20:
        return pag.pytweening.easeInExpo
    elif rand == 21:
        return pag.pytweening.easeOutExpo
    elif rand == 22:
        return pag.pytweening.easeInOutExpo
