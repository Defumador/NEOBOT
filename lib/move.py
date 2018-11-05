import random, os #import module to allow for Random command in ahk
os.chdir('C:\\Program Files (x86)\\Python37-32\Lib\\site-packages\\') #change directory in order to locate pyautogui module  
import pyautogui #import pyautogui
pyautogui.PAUSE = 2.5

def movetime(): #randomize the amount of time mouse takes to move to a new location
    movetimevar = (random.randint(0,3000) / 1000) #take up to 3 seconds to move mouse, convert from miliseconds to seconds
    return movetimevar

def mousepath(): #randomize the behavior of mouse button as it moves to a location
    mousepathvar = (random.randint(1,6))
    #higher chance of easeInQuad and easeOutQuad movement methods than easeInBounce or easeInElastic
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
