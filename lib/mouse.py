import time
import random

import pyautogui


def click():
	# click the primary mouse button, waiting both before and after for a randomized period of time
	time.sleep(float(random.randint(0, 500)) / 1000)
	pyautogui.click() #(duration=(float(random.randint(500, 2000) / 1000)))
	time.sleep(float(random.randint(0, 500)) / 1000)
	return


def click_right():
	time.sleep(float(random.randint(0, 500)) / 1000)
	pyautogui.click(button='right') #duration=(float(random.randint(500, 2500) / 1000)))
	time.sleep(float(random.randint(0, 500)) / 1000)
	return


def move_time():
	# randomize the amount of time mouse takes to move to a new location
	movetimevar = (float(random.randint(200, 1500) / 1000))
	return movetimevar


def mouse_path():
	# randomize the moving behavior of mouse cursor as it moves to a location
	rand = random.randint(1, 2)
	if rand == 1:
		return pyautogui.easeInQuad
	elif rand == 2:
		return pyautogui.easeOutQuad
