import time
import random

import pyautogui

pyautogui.FAILSAFE = True


def enter():  # hit enter key to confirm pop-up
	print('hitting enter')
	pyautogui.keyDown('enter')
	time.sleep(float(random.randint(0, 500)) / 1000)
	pyautogui.keyUp('enter')
	return


def select_all():  # hotkey to select all items in a menu
	print('selecting all')
	pyautogui.keyDown('ctrl')
	time.sleep(float(random.randint(0, 800)) / 1000)
	pyautogui.keyDown('a')
	time.sleep(float(random.randint(0, 800)) / 1000)
	pyautogui.keyUp('a')
	time.sleep(float(random.randint(0, 800)) / 1000)
	pyautogui.keyUp('ctrl')
	return


def open_station_hangar():  # hotkey to open station hangar inventory window when docked
	print('alt a')
	pyautogui.keyDown('alt')
	pyautogui.keyDown('g')
	pyautogui.keyUp('g')
	pyautogui.keyUp('alt')
	return