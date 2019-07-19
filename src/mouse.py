import time, random
import pyautogui as pag


def click():
    """Click the primary mouse button, waiting both before and after for a
    randomized period of time."""
    time.sleep(float(random.randint(0, 500)) / 1000)
    pag.click(duration=(float(random.randint(0, 100) / 1000)))
    time.sleep(float(random.randint(0, 500)) / 1000)
    return


def click_right():
    time.sleep(float(random.randint(0, 500)) / 1000)
    pag.click(button='right', duration=(float(random.randint(0, 100) / 1000)))
    time.sleep(float(random.randint(0, 500)) / 1000)
    return


def duration():
    """Randomize the amount of time the mouse cursor takes to move to a
    new location."""
    movetimevar = (float(random.randint(50, 1500) / 1000))
    return movetimevar


def path():
    """Randomize the movement behavior of the mouse cursor as it moves to a
    new location."""
    # https://stackoverflow.com/questions/44467329/pyautogui-mouse-movement-with-bezier-curve
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
