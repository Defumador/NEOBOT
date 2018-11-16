import sys, pyautogui, os, time, random, ctypes
from lib import mouse, keyboard, load_ship, unload_ship, while_docked, navigation

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 2.5  # set default wait time
sys.setrecursionlimit(100000)


load_ship.load_ship()
print(load_ship.load_ship)

sys.exit()
'''
def traveler():
    while_docked.docked_check()
    if docked_check = 1
        while_docked.undock()
    elif docked_check = 0
        navgation.look_for_waypoint()
'''