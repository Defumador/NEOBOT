import time, random
import pyautogui


def keypress(key):
    """Hold down the specified key for a random period of time rather than just
    pressing it momentarily."""
    time.sleep(float(random.randint(5, 500)) / 1000)
    pyautogui.keyDown(key)
    time.sleep(float(random.randint(5, 190)) / 1000)
    pyautogui.keyUp(key)
    time.sleep(float(random.randint(5, 500)) / 1000)
    return


def select_all():
    pyautogui.keyDown('ctrl')
    time.sleep(float(random.randint(0, 800)) / 1000)

    pyautogui.keyDown('a')
    time.sleep(float(random.randint(0, 800)) / 1000)
    pyautogui.keyUp('a')

    time.sleep(float(random.randint(0, 800)) / 1000)
    pyautogui.keyUp('ctrl')
    return
