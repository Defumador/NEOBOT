import sys, pyautogui, os, time, random, ctypes
from lib import mouse, unload_ship, load_ship, while_docked

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 2.5

sys.setrecursionlimit(100000)
conf = 0.95

# get monitor resolution, used to speed up image searching
user32 = ctypes.windll.user32
screenwidth = user32.GetSystemMetrics(0)
screenheight = user32.GetSystemMetrics(1)
halfscreenwidth = (int(screenwidth / 2))
halfscreenheight = (int(screenheight / 2))


def select_waypoint():  # click on current waypoint in overview by looking for either station or stargate icons
    # look for station icon
    print('looking for waypoints')
    stargate_look_num = 1
    # search right half of screen only for stargate icon
    stargate_waypoint = pyautogui.locateCenterOnScreen('stargate_waypoint.bmp', confidence=conf,
                                                            region=(halfscreenwidth, 0, screenwidth, screenheight))
    while stargate_waypoint is None and stargate_look_num < 100:  # search for waypoints up to 100 times
        stargate_look_num += 0
        global select_waypoint_var
        # if stargate waypoint not found, look for station waypoint
        station_waypoint = pyautogui.locateCenterOnScreen('station_waypoint.bmp', confidence=conf,
                                                               region=(halfscreenwidth, 0, screenwidth, screenheight))
        # if station waypoint not found, look for stargate waypoint again and restart loop
        if station_waypoint is None:
            stargate_waypoint = pyautogui.locateCenterOnScreen('stargate_waypoint.bmp', confidence=conf,
                                                               region=(halfscreenwidth, 0, screenwidth, screenheight))
            print('looking waypoints ...', stargate_look_num)
            continue
        elif station_waypoint is not None:
            print('found station waypoint')
            # separate x and y coordinates of location
            (station_waypointx, station_waypointy) = station_waypoint
            # clicks the center of where the button was found
            pyautogui.moveTo((station_waypointx + (random.randint(-8, 220))),
                             (station_waypointy + (random.randint(-8, 8))),
                             mouse.move_time(), mouse.mouse_path())
            mouse.click()
            select_waypoint_var = 2
            return
    # check if stargate waypoint was found before loop expired
    if stargate_waypoint is not None and stargate_look_num < 100:
        print('found stargate waypoint')
        (stargate_waypointx, stargate_waypointy) = stargate_waypoint
        # clicks the center of where the button was found
        pyautogui.moveTo((stargate_waypointx + (random.randint(-8, 220))),
                         (stargate_waypointy + (random.randint(-8, 8))),
                         mouse.move_time(), mouse.mouse_path())
        pyautogui.click()
        select_waypoint_var = 1
        return
    else: # loop breaks to here
        print('cant find waypoints')
        select_waypoint_var = 0
        return


def select_warp_button():  # locate jump button in selection box if stargate icon was found
    print('looking for warp buttons')
    # search right half of screen only
    jump_button = pyautogui.locateCenterOnScreen('jump_button.bmp', confidence=conf,
                                                 region=(halfscreenwidth, 0, screenwidth, screenheight))
    while jump_button is None:
        print('cant find jump button')
        dock_button = pyautogui.locateCenterOnScreen('dock_button.bmp', confidence=conf,
                                                     region=(halfscreenwidth, 0, screenwidth, screenheight))
        if dock_button is None:
            print('cant find dock button')
            select_warp_button()
        else:
            print('found dock button')
            (dock_buttonx, dock_buttony) = dock_button
            pyautogui.moveTo((dock_buttonx + (random.randint(-8, 8))),
                             (dock_buttony + (random.randint(-8, 8))),
                             mouse.move_time(), mouse.mouse_path())
            pyautogui.click()
            # move mouse away to prevent tooltips from blocking buttons
            pyautogui.moveRel((-1 * (random.randint(10, 500))), (random.randint(40, 500)),
                              mouse.move_time(), mouse.mouse_path())
            print('warping to station')
            time.sleep(15)
            return
    else:
        print('found jump button')
        (jump_buttonx, jump_buttony) = jump_button
        pyautogui.moveTo((jump_buttonx + (random.randint(-8, 8))),
                         (jump_buttony + (random.randint(-8, 8))),
                         mouse.move_time(), mouse.mouse_path())
        pyautogui.click()
        pyautogui.moveRel((-1 * (random.randint(10, 500))), (random.randint(40, 500)),
                          mouse.move_time(), mouse.mouse_path())  # move mouse away from button
        print('warping to gate')
        time.sleep(15)  # wait for warp to start before starting to search for new waypoints
        return


def detect_dock_or_jump():  # check if client has docked or jumped
    # look for undock icon to indicate a dock has been made
    global detect_dock_or_jump_var
    detect_loop_num = 0
    # search right half of screen only
    undock_icon = pyautogui.locateCenterOnScreen('undock.bmp', confidence=conf,
                                                 region=(halfscreenwidth, 0, screenwidth, screenheight))
    # if undock icon is not found, look for 'no object selected' in selection box, indicating a jump has been made
    while undock_icon is None:
        detect_loop_num += 1
        print('waiting for jump or dock ...',detect_loop_num)
        time.sleep(3)
        # search bottom half of screen only
        spedometer = pyautogui.locateCenterOnScreen('spedometer.bmp', confidence=0.97,
                                                    region=(0, halfscreenheight, screenwidth, screenheight))
        if spedometer is None:  # if jump is not detected, wait and rerun function
            undock_icon = pyautogui.locateCenterOnScreen('undock.bmp', confidence=conf,
                                                 region=(halfscreenwidth, 0, screenwidth, screenheight))
        else:
            # if jump detected, warp to next waypoint
            print('jump detected')
            time.sleep(2)  # wait for jump transition to complete
            # double-check to make sure ship is not moving
            spedometer = pyautogui.locateCenterOnScreen('spedometer.bmp', confidence=0.97,
                                                        region=(0, halfscreenheight, screenwidth, screenheight))
            if spedometer is None:
                print('jump check denied -----------------------------------------')
                detect_dock_or_jump()
            else:
                print('jump confirmed')
                detect_dock_or_jump_var = 1
                return
    else:
        print('dock detected')
        detect_dock_or_jump_var = 2
        return


# check if ship has arrived back at its home station by looking for an entry in 'people and places' starting with 3 0's
def at_home_check():
    # search left half of screen only
    global at_home_check_var
    at_home = pyautogui.locateCenterOnScreen('at_home.bmp', confidence=conf,
                                             region=(0, 0, halfscreenwidth, screenheight))
    if at_home is None:
        print('not at home station')
        at_home_check_var = 0
        return
    elif at_home is not None:
        print('at home station')
        at_home_check_var = 1
        return


# check if ship has arrived back at its destination by looking for an entry in 'people and places' starting with 3 1's
def at_dest_check():
    global at_dest_check_var
    at_dest = pyautogui.locateCenterOnScreen('at_dest.bmp', confidence=conf,
                                             region=(0, 0, halfscreenwidth, screenheight))
    if at_dest is None:
        print('not at destination station')
        at_dest_check_var = 0
        return
    else:
        print('at destination station')
        at_dest_check_var = 1
        return


# set waypoint back to home station before undocking from destination station
def return_home():
    print('at destination station, setting home waypoint')
    home = pyautogui.locateCenterOnScreen('home.bmp', confidence=conf,
                                          region=(0, 0, halfscreenwidth, screenheight))
    (homex, homey) = home
    pyautogui.moveTo((homex + (random.randint(-1, 200))), (homey + (random.randint(-3, 3))),
                     mouse.move_time(), mouse.mouse_path())
    mouse.click_right()  # right click to open dropdown menu
    pyautogui.moveRel((0 + (random.randint(10, 50))), (0 + (random.randint(20, 25))),
                      mouse.move_time(), mouse.mouse_path())
    mouse.click()  # click set destination in drop down
    return


def return_to_dest():
    print('at home station, setting destination waypoint')
    dest = pyautogui.locateCenterOnScreen('dest.bmp', confidence=conf,
                                          region=(0, 0, halfscreenwidth, screenheight))
    (destx, desty) = dest
    pyautogui.moveTo((destx + (random.randint(-1, 200))), (desty + (random.randint(-3, 3))),
                     mouse.move_time(), mouse.mouse_path())
    mouse.click_right()  # right click to open dropdown menu
    pyautogui.moveRel((0 + (random.randint(10, 50))), (0 + (random.randint(20, 25))),
                      mouse.move_time(), mouse.mouse_path())
    mouse.click()  # click set destination in drop down
    return
