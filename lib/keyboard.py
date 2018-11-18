import sys, pyautogui, os, time, random, ctypes

pyautogui.FAILSAFE = True


def enter():  # hit enter key to confirm pop-up
    print('hitting enter')
    pyautogui.keyDown('enter')
    pyautogui.keyUp('enter')
    return



def select_all():  # hotkey to select all items in a menu
    print('selecting all')
    pyautogui.keyDown('ctrl')
    pyautogui.keyDown('a')
    pyautogui.keyUp('a')
    pyautogui.keyUp('ctrl')
    print('done selecting all')
    return


def open_station_hangar():  # hotkey to open station hangar inventory window when docked
    print('alt a')
    pyautogui.keyDown('alt')
    pyautogui.keyDown('g')
    pyautogui.keyUp('g')
    pyautogui.keyUp('alt')
    return