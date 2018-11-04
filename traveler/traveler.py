import os
os.chdir('C:\\Program Files (x86)\\Python37-32\Lib\\site-packages\\')

import pyautogui
pyautogui.PAUSE = 2.5

pyautogui.alert('This is an alert box.')
'OK'

pyautogui.moveTo(0, 0, duration=0)  # move mouse to XY coordinates over num_second seconds