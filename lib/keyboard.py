
import pyautogui  # import pyautogui
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 2.5
import os, random, time  # import module to allow for Random command in ahk
# change directory in order to locate pyautogui module
os.chdir('C:\\Program Files (x86)\\Python37-32\Lib\\site-packages\\')


def enter():  # hit enter key to confirm pop-up
    print('hitting enter')
    time.sleep((random.randint(0, 100) / 1000))  # wait up to 1 second before starting hotkey sequence
    pyautogui.keyDown('enter')
    time.sleep((random.randint(0, 100) / 1000))  # hold down key for up to 500ms
    pyautogui.keyUp('enter')
    time.sleep((random.randint(0, 100) / 1000))  # wait up to 1 second after starting hotkey sequence
    return


def select_all():  # hotkey to select all items in a menu
    print('selecting all')
    time.sleep((random.randint(0, 100) / 1000))
    pyautogui.keyDown('ctrl')
    time.sleep((random.randint(0, 100) / 1000))
    pyautogui.keyDown('a')
    time.sleep((random.randint(0, 100) / 1000))
    pyautogui.keyUp('a')
    time.sleep((random.randint(0, 100) / 1000))
    pyautogui.keyUp('ctrl')
    time.sleep((random.randint(0, 100) / 1000))
    return


def open_station_hangar(): # hotkey to open station hangar inventory window when docked
    print('alt a')
    time.sleep((random.randint(0, 1000) / 1000))
    pyautogui.keyDown('alt')
    time.sleep((random.randint(0, 500) / 1000))
    pyautogui.keyDown('g')
    time.sleep((random.randint(0, 500) / 1000))
    pyautogui.keyUp('g')
    time.sleep((random.randint(0, 500) / 1000))
    pyautogui.keyUp('alt')
    time.sleep((random.randint(0, 1000) / 1000))
    return
