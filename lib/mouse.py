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
    rand = random.randint(1, 19)
    n = (float(random.randint(0, 1000) / 1000))
    
    if rand == 1:
        return pag.easeInQuad(n)
    elif rand == 2:
        return pag.easeOutQuad(n)
    elif rand == 3:
        return pag.easeInOutQuad(n)
    
    elif rand == 4:
        return pag.easeInQuart(n)
    elif rand == 5:
        return pag.easeOutQuart(n)
    elif rand == 6:
        return pag.easeInOutQuart(n)
    
    elif rand == 7:
        return pag.easeInQuint(n)
    elif rand == 8:
        return pag.easeOutQuint(n)
    elif rand == 9:
        return pag.easeInOutQuint(n)
    
    elif rand == 10:
        return pag.easeInBack(n)
    elif rand == 11:
        return pag.easeOutBack(n)
    elif rand == 12:
        return pag.easeInOutBack(n)
    
    elif rand == 13:
        return pag.easeInCirc(n)
    elif rand == 14:
        return pag.easeOutCirc(n)
    elif rand == 15:
        return pag.easeInOutCirc(n)
    
    elif rand = 16:
        return pag.pytweening.easeInSine(n)
    elif rand = 17:
        return pag.pytweening.easeOutSine(n)
    elif rand = 18:
        return pag.pytweening.easeInOutSine(n)
    
    elif rand = 19:
        return pag.pytweening.Linear(n)
    
    
    
