import os
import pyautogui
from lib import while_docked
from lib import in_space
os.chdir('C:\\Program Files (x86)\\Python37-32\Lib\\site-packages\\')  # change directory in order to locate pyautogui module


pyautogui.PAUSE = 2.5  # set default wait time
os.chdir('D:\OneDrive\Documents\Scripts\Python\PY-NEOBOT-GitHub\lib')


#while_docked.undock()  # undock from station
pyautogui.PAUSE = 15  # wait for undock to complete
in_space.select_waypoint()  # look for and click on waypoint, then jump to waypoint destination



# sys.exit()
# select_station_waypoint()
