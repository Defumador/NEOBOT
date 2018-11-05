import random, os #import module to allow for Random command in ahk
os.chdir('C:\\Program Files (x86)\\Python37-32\Lib\\site-packages\\') #change directory in order to locate pyautogui module 
import pyautogui #import pyautogui
pyautogui.PAUSE = 2.5

def click(): #click the mouse for a randomized period of time
    pyautogui.PAUSE = (random.randint(0,1000) / 1000) #wait up to 1 second before clicking
    pyautogui.mouseDown()
    pyautogui.PAUSE = (random.randint(0,250) / 1000) #hold down mouse button for up to 250ms                       
    pyautogui.mouseUp()
    pyautogui.PAUSE = (random.randint(0,1000) / 1000) #wait up to 1 second after clicking
    return

def clickright(): #same thing but with right mouse button
    pyautogui.PAUSE = (random.randint(0,1000) / 1000)
    pyautogui.mouseDown(button='right')
    pyautogui.PAUSE = (random.randint(0,250) / 1000)                       
    pyautogui.mouseUp(button='right')
    pyautogui.PAUSE = (random.randint(0,1000) / 1000)
    return