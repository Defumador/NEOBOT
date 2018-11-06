import random, os #import module to allow for Random command in ahk
os.chdir('C:\\Program Files (x86)\\Python37-32\Lib\\site-packages\\') #change directory in order to locate pyautogui module 
import pyautogui #import pyautogui
pyautogui.PAUSE = 2.5

def enter(): #hit enter key to confirm pop-up
    pyautogui.PAUSE = (random.randint(0,1000) / 1000) #wait up to 1 second before starting hotkey sequence
    pyautogui.keyDown('enter') 
    pyautogui.PAUSE = (random.randint(0,500) / 1000) #hold down key for up to 500ms   
    pyautogui.keyUp('enter')
    pyautogui.PAUSE = (random.randint(0,1000) / 1000) #wait up to 1 second after starting hotkey sequence
    return

def select_all(): #hotkey to select all items in a menu
    pyautogui.PAUSE = (random.randint(0,1000) / 1000)
    pyautogui.keyDown('ctrl') 
    pyautogui.PAUSE = (random.randint(0,500) / 1000)
    pyautogui.keyDown('a') 
    pyautogui.PAUSE = (random.randint(0,500) / 1000)
    pyautogui.keyUp('a') 
    pyautogui.PAUSE = (random.randint(0,500) / 1000)
    pyautogui.keyUp('ctrl')
    pyautogui.PAUSE = (random.randint(0,1000) / 1000)
    return
 
def open_station_hangar(): #hotkey to open station hangar inventory window when docked
    pyautogui.PAUSE = (random.randint(0,1000) / 1000)
    pyautogui.keyDown('alt') 
    pyautogui.PAUSE = (random.randint(0,500) / 1000)
    pyautogui.keyDown('g') 
    pyautogui.PAUSE = (random.randint(0,500) / 1000)
    pyautogui.keyUp('g') 
    pyautogui.PAUSE = (random.randint(0,500) / 1000)
    pyautogui.keyUp('alt')
    pyautogui.PAUSE = (random.randint(0,1000) / 1000)
    return


