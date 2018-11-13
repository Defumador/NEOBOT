import sys #import module to allow for Random command in ahk
from mouse import *
import pyautogui #import pyautogui
pyautogui.PAUSE = 2.55
os.chdir('D:\OneDrive\Documents\Scripts\Python\PY-NEOBOT-GitHub\lib')

def select_waypoint():
    station_waypoint_icon = pyautogui.locateCenterOnScreen('station_waypoint_icon.png')
    print(station_waypoint_icon)
    while station_waypoint_icon == None:
        print('cant find station_waypoint_icon')
        pyautogui.PAUSE = 1
        stargate_waypoint_icon = pyautogui.locateCenterOnScreen('stargate_waypoint_icon.png')
        print(stargate_waypoint_icon)
        if stargate_waypoint_icon == None:
            print('cant find stargate_waypoint_icon')
            pyautogui.PAUSE = 1
            select_waypoint()
        else:
            (stargate_waypoint_iconx, stargate_waypoint_icony) = stargate_waypoint_icon
            pyautogui.moveTo(stargate_waypoint_iconx, stargate_waypoint_icony, move_time(), mouse_path())  # clicks the center of where the button was found
            click()
            select_jump_button()
            return
    else:
        print('found station_waypoint_icon')
        (station_waypoint_iconx, station_waypoint_icony) = station_waypoint_icon
        pyautogui.moveTo(station_waypoint_iconx, station_waypoint_icony, move_time(), mouse_path())  # clicks the center of where the button was found
        click()
        select_dock_button()
        return

def select_jump_button():
    jump_button = pyautogui.locateCenterOnScreen('jump_button.png')
    print(jump_button)
    if jump_button == None:
        print('cant find jump_button')
        sys.exit()
    else:
        (jump_buttonx, jump_buttony) = jump_button
        pyautogui.moveTo(jump_buttonx, jump_buttony, move_time(), mouse_path())  # clicks the center of where the button was found
        click()
        return
    
def select_dock_button():
    dock_button = pyautogui.locateCenterOnScreen('dock_button.png')
    print(dock_button)
    if dock_button == None:
        print('cant find dock_button')
        sys.exit()
    else:
        (dock_buttonx, dock_buttony) = dock_button
        pyautogui.moveTo(dock_buttonx, dock_buttony, move_time(), mouse_path())  # clicks the center of where the button was found
        click()
        return
    
def detect_dock_or_jump(): #check if client has docked or jumped
    undock_icon = pyautogui.locateCenterOnScreen('undock_icon.png') #look for undock icon to indicate a dock has been made
    print(undock_icon)
    while undock_icon == None: #if undock icon is not found, look for 'no object selected' in selection box, indicating a jump has been made
        print('not docked')
        no_object_selected_icon = pyautogui.locateCenterOnScreen('no_object_selected_icon.png')
        print(no_object_selected_icon)
        if no_object_selected_icon == None: #if jump is not detected, wait and rerun function
            print('no jump')
            pyautogui.PAUSE = 0.5
            detect_dock_or_jump()
        else:
            print('detected jump')
            pyautogui.PAUSE = 1
            (no_object_selected_iconx, no_object_selected_icony) = no_object_selected_icon
            pyautogui.moveTo(no_object_selected_iconx, no_object_selected_icony, move_time(), mouse_path())
            click()
            return 
    else:
        print('detected dock!')
        pyautogui.PAUSE = 1
        (undock_iconx, undock_icony) = undock_icon
        pyautogui.moveTo(undock_iconx, undock_icony, move_time(), mouse_path())
        click()
        return
    
