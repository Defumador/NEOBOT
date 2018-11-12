import pyautogui  # import pyautogui
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 2.5
import os, random, time
# change directory in order to locate pyautogui module
os.chdir('C:\\Program Files (x86)\\Python37-32\Lib\\site-packages\\')


def enter():  # hit enter key to confirm pop-up
    print('hitting enter')
    pyautogui.keyDown('enter')
    #time.sleep((random.randint(0, 10) / 10))  # hold down key for up to 500ms
    pyautogui.keyUp('enter')
    return


def select_all():  # hotkey to select all items in a menu
    print('selecting all')
    pyautogui.keyDown('ctrl')
    #time.sleep((random.randint(0, 10) / 10))
    pyautogui.keyDown('a')
    #time.sleep((random.randint(0, 10) / 10))
    pyautogui.keyUp('a')
    #time.sleep((random.randint(0, 10) / 10))
    pyautogui.keyUp('ctrl')
    return


def open_station_hangar():  # hotkey to open station hangar inventory window when docked
    print('alt a')
    pyautogui.keyDown('alt')
    #time.sleep((random.randint(0, 10) / 10))
    pyautogui.keyDown('g')
    #time.sleep((random.randint(0, 10) / 10))
    pyautogui.keyUp('g')
    #time.sleep((random.randint(0, 10) / 10))
    pyautogui.keyUp('alt')
    return
