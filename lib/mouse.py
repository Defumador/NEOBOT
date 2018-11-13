import sys, pyautogui, os, time, random, ctypes

pyautogui.FAILSAFE = True


def click():  # click the mouse for a randomized period of time
    print('clicking')
    pyautogui.click(duration=(random.randint(5, 20) / 10))
    print('done clicking')
    return


def click_right():  # same thing but with right mouse button
    print('right clicking')
    pyautogui.click(button='right', duration=(random.randint(5, 25) / 10))
    return


def move_time():  # randomize the amount of time mouse takes to move to a new location
    movetimevar = (random.randint(0, 20) / 10)
    return movetimevar


def mouse_path():  # randomize the behavior of mouse button as it moves to a location
    return pyautogui.easeInQuad

    """
    mousepathvar = (random.randint(1, 15))
    # higher chance of easeInQuad and easeOutQuad movement methods than easeInBounce or easeInElastic
    if mousepathvar == 1:
        return pyautogui.easeInQuad
    elif mousepathvar == 2:
        return pyautogui.easeInQuad
    elif mousepathvar == 3:
        return pyautogui.easeOutQuad
    elif mousepathvar == 4:
        return pyautogui.easeOutQuad
    else:
        return pyautogui.easeOutQuad
    """