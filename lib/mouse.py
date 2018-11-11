import random, os, time
os.chdir('C:\\Program Files (x86)\\Python37-32\Lib\\site-packages\\')
import pyautogui  # import pyautogui
pyautogui.FAILSAFE = True
os.chdir('D:\OneDrive\Documents\Scripts\Python\PY-NEOBOT-GitHub\lib')


def click():  # click the mouse for a randomized period of time
    print('clicking')
    # wait up to 1 second before clicking, divide by 1000 to convert from miliseconds to seconds
    time.sleep((random.randint(0, 10) / 10))
    pyautogui.click(duration=((random.randint(5, 25) / 10)))
    time.sleep((random.randint(0, 10) / 10))  # wait up to 1 second after clicking
    return


def click_right(): # same thing but with right mouse button
    print('right clicking')
    time.sleep((random.randint(0, 50) / 10))
    pyautogui.click(button='right', duration=((random.randint(5, 25) / 10)))
    time.sleep((random.randint(0, 50) / 10))
    return


def move_time():  # randomize the amount of time mouse takes to move to a new location
    # take up to 3 seconds to move mouse, convert from miliseconds to seconds
    movetimevar = (random.randint(0, 30) / 10)
    return movetimevar


def mouse_path():  # randomize the behavior of mouse button as it moves to a location
    mousepathvar = (random.randint(1, 6))
    # higher chance of easeInQuad and easeOutQuad movement methods than easeInBounce or easeInElastic
    if mousepathvar == 1:
        return pyautogui.easeInQuad
    elif mousepathvar == 2:
        return pyautogui.easeInQuad
    elif mousepathvar == 3:
        return pyautogui.easeOutQuad
    elif mousepathvar == 4:
        return pyautogui.easeOutQuad
    elif mousepathvar == 5:
        return pyautogui.easeInBounce
    else:
        return pyautogui.easeInElastic
