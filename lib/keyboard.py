import time
import random

import pyautogui


def keypress(key):
    # Hold down the specified key for a random period of time rather than just
    # pressing it momentarily.
    time.sleep(float(random.randint(0, 500)) / 1000)
    pyautogui.keyDown(key)
    time.sleep(float(random.randint(5, 200)) / 1000)
    pyautogui.keyUp(key)
    time.sleep(float(random.randint(0, 500)) / 1000)
    return


def enter():
    print('enter -- called')
    pyautogui.keyDown('enter')
    time.sleep(float(random.randint(0, 500)) / 1000)
    pyautogui.keyUp('enter')
    return


def select_all():
    print('select_all -- called')
    pyautogui.keyDown('ctrl')
    time.sleep(float(random.randint(0, 800)) / 1000)

    pyautogui.keyDown('a')
    time.sleep(float(random.randint(0, 800)) / 1000)
    pyautogui.keyUp('a')

    time.sleep(float(random.randint(0, 800)) / 1000)
    pyautogui.keyUp('ctrl')
    return
