from lib import while_docked, mouse
import sys, pyautogui, os, time, random

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 2.5
os.chdir('D:\OneDrive\Documents\Scripts\Python\PY-NEOBOT-GitHub\lib')
sys.setrecursionlimit(100000)
conf = 0.95


def select_waypoint():  # click on current waypoint in overview by looking for either station or stargate icons
    # look for station icon
    os.chdir('c:/users/austin/desktop/icons')
    station_waypoint_icon = pyautogui.locateCenterOnScreen('station_waypoint_icon.png', confidence=conf)
    while station_waypoint_icon is None:
        print('cant find station_waypoint_icon')
        time.sleep(1)  # wait 1 second before rerunning loop
        # if station icon not found, look for stargate icon
        stargate_waypoint_icon = pyautogui.locateCenterOnScreen('stargate_waypoint_icon.png', confidence=conf)
        if stargate_waypoint_icon is None:
            print('cant find stargate_waypoint_icon')
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
    jump_button = pyautogui.locateCenterOnScreen('jump_button_icon.png', confidence=conf)
    while jump_button is None:
        print('cant find jump_button_icon')
        time.sleep(1)
        dock_button = pyautogui.locateCenterOnScreen('dock_button_icon.png', confidence=conf)
        if dock_button is None:
            print('cant find dock_button_icon')
            select_warp_button()
        else:
            print('found dock_button_icon')
            (dock_buttonx, dock_buttony) = dock_button
            pyautogui.moveTo((dock_buttonx + (random.randint(-8, 8))),
                             (dock_buttony + (random.randint(-8, 8))),
                             mouse.move_time(), mouse.mouse_path())
            mouse.click()
            pyautogui.moveRel((random.randint(-300, 300)), (random.randint(40, 300)),
                              mouse.move_time(), mouse.mouse_path())  # move mouse away from button
            time.sleep(20)
            detect_dock_or_jump()
    else:
        print('found jump_button_icon')
        (jump_buttonx, jump_buttony) = jump_button
        pyautogui.moveTo((jump_buttonx + (random.randint(-8, 8))),
                         (jump_buttony + (random.randint(-8, 8))),
                         mouse.move_time(), mouse.mouse_path())
        mouse.click()
        pyautogui.moveRel((random.randint(-300, 300)), (random.randint(40, 300)),
                          mouse.move_time(), mouse.mouse_path())  # move mouse away from button
        time.sleep(20)  # wait for warp to start before starting to search for new waypoints
        detect_dock_or_jump()


def detect_dock_or_jump():  # check if client has docked or jumped
    # look for undock icon to indicate a dock has been made
    os.chdir('c:/users/austin/desktop/icons')
    undock_icon = pyautogui.locateCenterOnScreen('undock_icon.png', confidence=conf)
    # if undock icon is not found, look for 'no object selected' in selection box, indicating a jump has been made
    if undock_icon is None:
        print('waiting for jump or dock')
        time.sleep(2)
        spedometer = pyautogui.locateCenterOnScreen('spedometer.png', confidence=conf)
        if spedometer is None:  # if jump is not detected, wait and rerun function
            detect_dock_or_jump()
        else:
            print('jump detected')
            # if jump detected, warp to next waypoint
            select_warp_button()
    else:
        print('dock detected')
        at_home_check()


# check if ship has arrived back at its home station by looking for an entry in 'people and places' starting with 3 0's
def at_home_check():
    os.chdir('c:/users/austin/desktop/icons')
    at_home = pyautogui.locateCenterOnScreen('at_home.png', confidence=conf)
    if at_home is None:
        print('not at_home')
        at_dest_check()
    elif at_home is not None:
        print('at home')
        return_to_dest()


# check if ship has arrived back at its destination by looking for an entry in 'people and places' starting with 3 1's
def at_dest_check():
    os.chdir('c:/users/austin/desktop/icons')
    at_dest = pyautogui.locateCenterOnScreen('at_dest.png', confidence=conf)
    if at_dest is None:
        print('not at_dest')
        while_docked.open_station_hangar()
    else:
        print('at dest')
        return_home()


# set waypoint back to home station before undocking from destination station
def return_home():
    os.chdir('c:/users/austin/desktop/icons')
    home = pyautogui.locateCenterOnScreen('home.png', confidence=conf)
    (homex, homey) = home
    pyautogui.moveTo((homex + (random.randint(-1, 20))), (homey + (random.randint(-3, 3))),
                     mouse.move_time(), mouse.mouse_path())
    mouse.click_right()  # right click to open dropdown menu
    pyautogui.moveRel((0 + (random.randint(10, 50))), (0 + (random.randint(20, 25))),
                      mouse.move_time(), mouse.mouse_path())
    mouse.click()  # click set destination in drop down
    while_docked.open_station_hangar()


def return_to_dest():
    os.chdir('c:/users/austin/desktop/icons')
    dest = pyautogui.locateCenterOnScreen('dest.png', confidence=conf)
    (destx, desty) = dest
    pyautogui.moveTo((destx + (random.randint(-1, 20))), (desty + (random.randint(-3, 3))),
                     mouse.move_time(), mouse.mouse_path())
    mouse.click_right()  # right click to open dropdown menu
    pyautogui.moveRel((0 + (random.randint(10, 50))), (0 + (random.randint(20, 25))),
                      mouse.move_time(), mouse.mouse_path())
    mouse.click()  # click set destination in drop down
    while_docked.unload_ship()