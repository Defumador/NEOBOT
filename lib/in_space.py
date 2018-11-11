from lib import while_docked, mouse
import sys, pyautogui, os, time, random
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 2.5
os.chdir('D:\OneDrive\Documents\Scripts\Python\PY-NEOBOT-GitHub\lib')
sys.setrecursionlimit(100000)

def select_waypoint():  # click on current waypoint in overview by looking for either station or stargate icons
    # look for station icon
    os.chdir('c:/users/austin/desktop/icons')
    station_waypoint_icon = pyautogui.locateCenterOnScreen('station_waypoint_icon.png', confidence = 0.9)
    while station_waypoint_icon is None:
        print('cant find station_waypoint_icon')
        time.sleep(1)  # wait 1 second before rerunning loop
        # if station icon not found, look for stargate icon
        stargate_waypoint_icon = pyautogui.locateCenterOnScreen('stargate_waypoint_icon.png', confidence = 0.9)
        if stargate_waypoint_icon is None:
            print('cant find stargate_waypoint_icon')
            time.sleep(1)
            select_waypoint()
        else:
            print('found startgate_waypoint_icon')
            # separate x and y coordinates of location
            (stargate_waypoint_iconx, stargate_waypoint_icony) = stargate_waypoint_icon
            # clicks the center of where the button was found
            pyautogui.moveTo((stargate_waypoint_iconx + (random.randint(-8, 50))),
                             (stargate_waypoint_icony + (random.randint(-8, 8))),
                             mouse.move_time(), mouse.mouse_path())
            mouse.click()
            select_warp_button()

    else:
        print('found station_waypoint_icon')
        (station_waypoint_iconx, station_waypoint_icony) = station_waypoint_icon
        # clicks the center of where the button was found
        pyautogui.moveTo((station_waypoint_iconx + (random.randint(-8, 50))),
                         (station_waypoint_icony + (random.randint(-8, 8))),
                         mouse.move_time(), mouse.mouse_path())
        mouse.click()
        select_warp_button()


def select_warp_button():  # locate jump button in selection box if stargate icon was found
    os.chdir('c:/users/austin/desktop/icons')
    jump_button = pyautogui.locateCenterOnScreen('jump_button_icon.png', confidence = 0.9)
    while jump_button is None:
        print('cant find jump_button_icon')
        time.sleep(1)
        dock_button = pyautogui.locateCenterOnScreen('dock_button_icon.png', confidence=0.9)
        if dock_button is None:
            print('cant find dock_button_icon')
            time.sleep(1)
            select_warp_button()
        else:
            print('found dock_button_icon')
            (dock_buttonx, dock_buttony) = dock_button
            pyautogui.moveTo((dock_buttonx + (random.randint(-8, 8))),
                             (dock_buttony + (random.randint(-8, 8))),
                             mouse.move_time(), mouse.mouse_path())
            mouse.click()
            pyautogui.moveRel(((random.randint(-300, 300))), (random.randint(40, 300)),
                              mouse.move_time(), mouse.mouse_path()) #move mouse away from button
            time.sleep(20)
            detect_dock_or_jump()
    else:
        print('found jump_button_icon')
        (jump_buttonx, jump_buttony) = jump_button
        pyautogui.moveTo((jump_buttonx + (random.randint(-8, 8))),
                         (jump_buttony + (random.randint(-8, 8))),
                         mouse.move_time(), mouse.mouse_path())
        mouse.click()
        pyautogui.moveRel(((random.randint(-300, 300))), (random.randint(40, 300)),
                          mouse.move_time(), mouse.mouse_path())  # move mouse away from button
        time.sleep(20)  # wait for warp to start before starting to search for new waypoints
        detect_dock_or_jump()


def detect_dock_or_jump():  # check if client has docked or jumped
    # look for undock icon to indicate a dock has been made
    os.chdir('c:/users/austin/desktop/icons')
    undock_icon = pyautogui.locateCenterOnScreen('undock_icon.png', confidence = 0.9)
    # if undock icon is not found, look for 'no object selected' in selection box, indicating a jump has been made
    if undock_icon is None:
        print('waiting for jump or dock')
        time.sleep(0.5)
        no_object_selected_icon = pyautogui.locateCenterOnScreen('no_object_selected_icon.png', confidence = 0.9)
        if no_object_selected_icon is None:  # if jump is not detected, wait and rerun function
            detect_dock_or_jump()
        else:
            print('jump detected')
            time.sleep(3)  # wait for jump to complete
            # if jump detected, warp to next waypoint
            select_warp_button()
    else:
        print('dock detected')
        while_docked.at_home_check()
