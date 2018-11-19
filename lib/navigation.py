import sys, pyautogui, os, time, random, ctypes
from lib import mouse, unload_ship, load_ship, while_docked

pyautogui.FAILSAFE = True
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
    select_waypoint_look_num = 0
    # search right half of screen only for stargate icon
    stargate_waypoint = pyautogui.locateCenterOnScreen('stargate_waypoint.bmp', confidence=0.96,
                                                            region=(halfscreenwidth, 0, screenwidth, screenheight))
    while stargate_waypoint is None and select_waypoint_look_num < 100:  # search for waypoints up to 100 times
        select_waypoint_look_num += 1
        global select_waypoint_var
        # if stargate waypoint not found, look for station waypoint
        station_waypoint = pyautogui.locateCenterOnScreen('station_waypoint.bmp', confidence=0.96,
                                                               region=(halfscreenwidth, 0, screenwidth, screenheight))
        # if station waypoint not found, look for stargate waypoint again and restart loop
        if station_waypoint is None:
            stargate_waypoint = pyautogui.locateCenterOnScreen('stargate_waypoint.bmp', confidence=0.96,
                                                               region=(halfscreenwidth, 0, screenwidth, screenheight))
            print('looking waypoints ...', select_waypoint_look_num)
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
    if stargate_waypoint is not None and select_waypoint_look_num < 100:
        print('found stargate waypoint')
        (stargate_waypointx, stargate_waypointy) = stargate_waypoint
        # clicks the center of where the button was found
        pyautogui.moveTo((stargate_waypointx + (random.randint(-8, 220))),
                         (stargate_waypointy + (random.randint(-8, 8))),
                         mouse.move_time(), mouse.mouse_path())
        mouse.click()
        select_waypoint_var = 1
        return
    else: # loop breaks to here
        print('cant find waypoints')
        select_waypoint_var = 0
        return


def select_warp_button():  # locate jump button in selection box if stargate icon was found
    select_warp_button_loop_num = 0
    print('looking for warp buttons')
    # search right half of screen only
    jump_button = pyautogui.locateCenterOnScreen('jump_button.bmp', confidence=0.85,
                                                 region=(halfscreenwidth, 0, screenwidth, screenheight))
    while jump_button is None:
        print('cant find jump button')
        dock_button = pyautogui.locateCenterOnScreen('dock_button.bmp', confidence=0.85,
                                                     region=(halfscreenwidth, 0, screenwidth, screenheight))
        if dock_button is None:
            select_warp_button_loop_num += 1
            print('cant find dock button ...',select_warp_button_loop_num)
        elif dock_button is not None:
            print('found dock button')
            (dock_buttonx, dock_buttony) = dock_button
            pyautogui.moveTo((dock_buttonx + (random.randint(-8, 8))),
                             (dock_buttony + (random.randint(-8, 8))),
                             mouse.move_time(), mouse.mouse_path())
            mouse.click()
            # move mouse away to prevent tooltips from blocking buttons
            pyautogui.moveRel((-1 * (random.randint(10, 500))), (random.randint(40, 500)),
                              mouse.move_time(), mouse.mouse_path())
            print('warping to station')
            time.sleep(10)
            return
    if jump_button is not None:
        print('found jump button')
        (jump_buttonx, jump_buttony) = jump_button
        pyautogui.moveTo((jump_buttonx + (random.randint(-8, 8))),
                         (jump_buttony + (random.randint(-8, 8))),
                         mouse.move_time(), mouse.mouse_path())
        mouse.click()
        pyautogui.moveRel((-1 * (random.randint(10, 500))), (random.randint(40, 500)),
                          mouse.move_time(), mouse.mouse_path())  # move mouse away from button
        print('warping to gate')
        time.sleep(10)  # wait for warp to start before starting to search for new waypoints
        return


def detect_dock_or_jump():  # check if client has docked or jumped
    # look for undock icon to indicate a dock has been made
    global detect_dock_or_jump_var
    detect_dock_or_jump_loop_num = 0
    # search right half of screen only
    undock_icon = pyautogui.locateCenterOnScreen('undock.bmp', confidence=conf,
                                                 region=(halfscreenwidth, 0, screenwidth, screenheight))
    # if undock icon is not found, look for 'no object selected' in selection box, indicating a jump has been made
    while undock_icon is None:
        detect_dock_or_jump_loop_num += 1
        print('waiting for jump or dock ...',detect_dock_or_jump_loop_num)
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
            time.sleep((random.randint(10, 50) / 10))  # wait for jump transition to complete
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
        time.sleep((random.randint(10, 50) / 10))
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


def set_home():  # set station with 000 before name as destination in 'people and places'
    print('at destination station, setting home waypoint')
    home = pyautogui.locateCenterOnScreen('home.bmp', confidence=conf,
                                          region=(0, 0, halfscreenwidth, screenheight))
    (homex, homey) = home
    pyautogui.moveTo((homex + (random.randint(-1, 200))), (homey + (random.randint(-3, 3))),
                     mouse.move_time(), mouse.mouse_path())
    mouse.click_right()  # right click to open dropdown menu
    pyautogui.moveRel((0 + (random.randint(10, 80))), (0 + (random.randint(20, 25))),
                      mouse.move_time(), mouse.mouse_path())
    mouse.click()  # click set destination in drop down
    return


# check if ship has arrived back at its destination by looking for an entry in 'people and places' starting with 3 1's
def at_dest1_check():
    global at_dest_check_var
    at_dest1 = pyautogui.locateCenterOnScreen('at_dest1.bmp', confidence=conf,
                                             region=(0, 0, halfscreenwidth, screenheight))
    if at_dest1 is None:
        print('not at destination1 station')
        at_dest1_check_var = 0
        return
    else:
        print('at destination1 station')
        at_dest1_check_var = 1
        return


def set_dest1():  # set station with 111 before name as destination in 'people and places'
    print('at home station, setting destination waypoint')
    dest1 = pyautogui.locateCenterOnScreen('dest1.bmp', confidence=conf,
                                           region=(0, 0, halfscreenwidth, screenheight))
    (dest1x, dest1y) = dest1
    pyautogui.moveTo((dest1x + (random.randint(-1, 200))), (dest1y + (random.randint(-3, 3))),
                     mouse.move_time(), mouse.mouse_path())
    mouse.click_right()  # right click to open dropdown menu
    pyautogui.moveRel((0 + (random.randint(10, 80))), (0 + (random.randint(20, 25))),
                      mouse.move_time(), mouse.mouse_path())
    mouse.click()  # click set destination in drop down
    return


# check if ship has arrived back at its 2nd destination by looking for an entry in 'people and places' starting with 3 2's
def at_dest2_check():
    global at_dest_check_var
    at_dest2 = pyautogui.locateCenterOnScreen('at_dest2.bmp', confidence=conf,
                                             region=(0, 0, halfscreenwidth, screenheight))
    if at_dest2 is None:
        print('not at destination2 station')
        at_dest2_check_var = 0
        return
    else:
        print('at destination2 station')
        at_dest2_check_var = 1
        return


def set_dest2():  # set station with 111 before name as destination in 'people and places'
    print('at home station, setting destination waypoint')
    dest2 = pyautogui.locateCenterOnScreen('dest2.bmp', confidence=conf,
                                           region=(0, 0, halfscreenwidth, screenheight))
    (dest2x, dest2y) = dest2
    pyautogui.moveTo((dest2x + (random.randint(-1, 200))), (dest2y + (random.randint(-3, 3))),
                     mouse.move_time(), mouse.mouse_path())
    mouse.click_right()  # right click to open dropdown menu
    pyautogui.moveRel((0 + (random.randint(10, 80))), (0 + (random.randint(20, 25))),
                      mouse.move_time(), mouse.mouse_path())
    mouse.click()  # click set destination in drop down
    return

# check if ship has arrived back at its 3rd destination by looking for an entry in 'people and places' starting with 3 3's
def at_dest3_check():
    global at_dest_check_var
    at_dest3 = pyautogui.locateCenterOnScreen('at_dest3.bmp', confidence=conf,
                                             region=(0, 0, halfscreenwidth, screenheight))
    if at_dest3 is None:
        print('not at destination3 station')
        at_dest3_check_var = 0
        return
    else:
        print('at destination3 station')
        at_dest3_check_var = 1
        return


def set_dest3():  # set station with 111 before name as destination in 'people and places'
    print('at home station, setting destination waypoint')
    dest3 = pyautogui.locateCenterOnScreen('dest3.bmp', confidence=conf,
                                           region=(0, 0, halfscreenwidth, screenheight))
    (dest3x, dest3y) = dest3
    pyautogui.moveTo((dest3x + (random.randint(-1, 200))), (dest3y + (random.randint(-3, 3))),
                     mouse.move_time(), mouse.mouse_path())
    mouse.click_right()  # right click to open dropdown menu
    pyautogui.moveRel((0 + (random.randint(10, 80))), (0 + (random.randint(20, 25))),
                      mouse.move_time(), mouse.mouse_path())
    mouse.click()  # click set destination in drop down
    return


# check if ship has arrived back at its 4th destination by looking for an entry in 'people and places' starting with 3 4's
def at_dest4_check():
    global at_dest_check_var
    at_dest4 = pyautogui.locateCenterOnScreen('at_dest4.bmp', confidence=conf,
                                             region=(0, 0, halfscreenwidth, screenheight))
    if at_dest4 is None:
        print('not at destination4 station')
        at_dest4_check_var = 0
        return
    else:
        print('at destination4 station')
        at_dest4_check_var = 1
        return


def set_dest4():  # set station with 111 before name as destination in 'people and places'
    print('at home station, setting destination waypoint')
    dest4 = pyautogui.locateCenterOnScreen('dest4.bmp', confidence=conf,
                                           region=(0, 0, halfscreenwidth, screenheight))
    (dest4x, dest4y) = dest4
    pyautogui.moveTo((dest4x + (random.randint(-1, 200))), (dest4y + (random.randint(-3, 3))),
                     mouse.move_time(), mouse.mouse_path())
    mouse.click_right()  # right click to open dropdown menu
    pyautogui.moveRel((0 + (random.randint(10, 80))), (0 + (random.randint(20, 25))),
                      mouse.move_time(), mouse.mouse_path())
    mouse.click()  # click set destination in drop down
    return


# check if ship has arrived back at its 5th destination by looking for an entry in 'people and places' starting with 3 5's
def at_dest5_check():
    global at_dest_check_var
    at_dest5 = pyautogui.locateCenterOnScreen('at_dest2.bmp', confidence=conf,
                                             region=(0, 0, halfscreenwidth, screenheight))
    if at_dest5 is None:
        print('not at destination5 station')
        at_dest5_check_var = 0
        return
    else:
        print('at destination5 station')
        at_dest5_check_var = 1
        return


def set_dest5():  # set station with 111 before name as destination in 'people and places'
    print('at home station, setting destination waypoint')
    dest5 = pyautogui.locateCenterOnScreen('dest5.bmp', confidence=conf,
                                           region=(0, 0, halfscreenwidth, screenheight))
    (dest5x, dest5y) = dest5
    pyautogui.moveTo((dest5x + (random.randint(-1, 200))), (dest5y + (random.randint(-3, 3))),
                     mouse.move_time(), mouse.mouse_path())
    mouse.click_right()  # right click to open dropdown menu
    pyautogui.moveRel((0 + (random.randint(10, 80))), (0 + (random.randint(20, 25))),
                      mouse.move_time(), mouse.mouse_path())
    mouse.click()  # click set destination in drop down
    return


def check_all_dest():
    at_home_check()
    if at_home_check_var == 1:
        set_dest1()
    elif at_home_check_var == 0:
        at_dest1_check()
        if at_dest1_check_var == 1 and load