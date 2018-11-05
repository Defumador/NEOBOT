import os, random #import system modules
os.chdir('D:\\OneDrive\\Documents\\Scripts\\Python\\NEOBOT')
from lib import move, click #import custom modules
os.chdir('C:\\Program Files (x86)\\Python37-32\Lib\\site-packages\\') #change directory in order to locate pyautogui module
import pyautogui #import pyautogui
pyautogui.PAUSE = 2.5 #set default wait time

#test alert box
pyautogui.alert('This is an alert box.')
'OK'

pyautogui.moveTo(0, 0, move.movetime(), move.mousepath())


#mousemove command
#pyautogui.moveTo(0, 0, duration=0)  # move mouse to XY coordinates over num_second seconds


#def Undock(): #undock from station
#pyautogui.moveTo((random.randint(0,1000)), (random.randint(0,1000)), duration=0)

    
