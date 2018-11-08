import random
import os  # import module to allow for Random command in ahk
os.chdir('C:\\Program Files (x86)\\Python37-32\Lib\\site-packages\\')
import pyautogui  # import pyautogui
os.chdir('D:\OneDrive\Documents\Scripts\Python\PY-NEOBOT-GitHub\lib')


def click():  # click the mouse for a randomized period of time
    pyautogui.PAUSE = (random.randint(0,500) / 1000)  # wait up to 1 second before clicking, divide by 1000 to convert from miliseconds to seconds
    pyautogui.mouseDown()  # click mouse button down
    pyautogui.PAUSE = (random.randint(0,100) / 1000)  # hold down mouse button for up to 250ms
    pyautogui.mouseUp()  # release mouse button
    pyautogui.PAUSE = (random.randint(0,500) / 1000)  # wait up to 1 second after clicking
    return


def clickright(): # same thing but with right mouse button
    pyautogui.PAUSE = (random.randint(0,1000) / 1000)
    pyautogui.mouseDown(button='right')
    pyautogui.PAUSE = (random.randint(0,250) / 1000)                       
    pyautogui.mouseUp(button='right')
    pyautogui.PAUSE = (random.randint(0,1000) / 1000)
    return


def move_time():  # randomize the amount of time mouse takes to move to a new location
    movetimevar = (random.randint(0,3000) / 1000)  # take up to 3 seconds to move mouse, convert from miliseconds to seconds
    return movetimevar


def mouse_path():  # randomize the behavior of mouse button as it moves to a location
    mousepathvar = (random.randint(1,6))
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
