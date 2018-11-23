import sys
import time
import ctypes
import random

import pyautogui

from lib import mouse

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
    stargate_waypoint = pyautogui.locateCenterOnScreen('./img/stargate_waypoint.bmp', confidence=0.96,
                                                       region=(halfscreenwidth, 0, screenwidth, screenheight))
    while stargate_waypoint is None and select_waypoint_look_num < 100:  # search for waypoints up to 100 times
        select_waypoint_look_num += 1
        global select_waypoint_var
        # if stargate waypoint not found, look for station waypoint
        station_waypoint = pyautogui.locateCenterOnScreen('./img/station_waypoint.bmp', confidence=0.96,
                                                          region=(halfscreenwidth, 0, screenwidth, screenheight))
        # if station waypoint not found, look for stargate waypoint again and restart loop
        if station_waypoint is None:
            stargate_waypoint = pyautogui.locateCenterOnScreen('./img/stargate_waypoint.bmp', confidence=0.96,
                                                               region=(halfscreenwidth, 0, screenwidth, screenheight))
            print('looking waypoints ...', select_waypoint_look_num)
            time.sleep(3)
            continue
        elif station_waypoint is not None:
            print('found station waypoint')
            # separate x and y coordinates of location
            (station_waypointx, station_waypointy) = station_waypoint
            pyautogui.moveTo((station_waypointx + (random.randint(-8, 220))),
                             (station_waypointy + (random.randint(-8, 8))),
                             mouse.move_time(), mouse.mouse_path())
            time.sleep(float(random.randint(0, 3000)) / 1000)
            mouse.click()
            select_waypoint_var = 2
            return
    # check if stargate waypoint was found before loop expired
    if stargate_waypoint is not None and select_waypoint_look_num < 100:
        print('found stargate waypoint')
        (stargate_waypointx, stargate_waypointy) = stargate_waypoint
        pyautogui.moveTo((stargate_waypointx + (random.randint(-8, 220))),
                         (stargate_waypointy + (random.randint(-8, 8))),
                         mouse.move_time(), mouse.mouse_path())
        time.sleep(float(random.randint(0, 3000)) / 1000)
        mouse.click()
        select_waypoint_var = 1
        return
    else:  # loop breaks to here
        print('cant find waypoints')
        select_waypoint_var = 0
        return


def select_warp_button():  # locate jump button in selection box if stargate icon was found
    select_warp_button_loop_num = 0
    print('looking for warp buttons')
    # search right half of screen only
    jump_button = pyautogui.locateCenterOnScreen('./img/jump_button.bmp', confidence=conf,
                                                 region=(halfscreenwidth, 0, screenwidth, screenheight))
    while jump_button is None:
        print('cant find jump button')
        dock_button = pyautogui.locateCenterOnScreen('./img/dock_button.bmp', confidence=conf,
                                                     region=(halfscreenwidth, 0, screenwidth, screenheight))
        if dock_button is None:
            select_warp_button_loop_num += 1
            print('cant find dock button ...', select_warp_button_loop_num)
            jump_button = pyautogui.locateCenterOnScreen('./img/jump_button.bmp', confidence=conf,
                                                         region=(halfscreenwidth, 0, screenwidth, screenheight))
        elif dock_button is not None:
            print('found dock button')
            (dock_buttonx, dock_buttony) = dock_button
            pyautogui.moveTo((dock_buttonx + (random.randint(-8, 8))),
                             (dock_buttony + (random.randint(-8, 8))),
                             mouse.move_time(), mouse.mouse_path())
            time.sleep(float(random.randint(0, 3000)) / 1000)
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
        time.sleep((random.randint(0, 200)) / 100)
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
    undock_icon = pyautogui.locateCenterOnScreen('./img/undock.bmp', confidence=conf,
                                                 region=(halfscreenwidth, 0, screenwidth, screenheight))
    # if undock icon is not found, look for 'no object selected' in selection box, indicating a jump has been made
    while undock_icon is None:
        detect_dock_or_jump_loop_num += 1
        print('waiting for jump or dock ...', detect_dock_or_jump_loop_num)
        time.sleep(3)
        # search bottom half of screen only
        spedometer = pyautogui.locateCenterOnScreen('./img/spedometer.bmp', confidence=0.98,
                                                    region=(0, halfscreenheight, screenwidth, screenheight))
        if spedometer is None:  # if jump is not detected, wait and rerun function
            undock_icon = pyautogui.locateCenterOnScreen('./img/undock.bmp', confidence=conf,
                                                         region=(halfscreenwidth, 0, screenwidth, screenheight))
        else:
            # if jump detected, warp to next waypoint
            print('jump detected')
            time.sleep(float(random.randint(2000, 5000)) / 1000)
            # double-check to make sure ship is not moving
            spedometer = pyautogui.locateCenterOnScreen('./img/spedometer.bmp', confidence=0.98,
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
        time.sleep(float(random.randint(0, 3000)) / 1000)
        return


# use a dictionary to dynamically grab destination names
destnum = {0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7"}


# figure out which destination station ship is at
def at_dest_num_dyn():
    global at_dest_num_var
    n = 0
    at_dest = pyautogui.locateCenterOnScreen(('./img/dest/at_dest' + (destnum[n]) + '.bmp'), confidence=conf,
                                             region=(0, 0, halfscreenwidth, screenheight))
    while at_dest is None:
        n = n + 1
        at_dest = pyautogui.locateCenterOnScreen(('./img/dest/at_dest' + (destnum[n]) + '.bmp'), confidence=conf,
                                                 region=(0, 0, halfscreenwidth, screenheight))
        print('looking for destination' + (destnum[n]))
        if n > 4:
            print('out of destinations to look for')
            sys.exit()
    if at_dest is not None:
        print('at dest' + (destnum[n]))
        at_dest_num_var = n
        return at_dest_num_var  # return number of station ship is docked in


# determine which station ship is in and blacklist it by editing its name
def blacklist_station():
    at_dest_num_dyn()
    print('blacklisting station')
    dest = pyautogui.locateCenterOnScreen(('./img/dest/dest' + (destnum[at_dest_num_var])), confidence=conf,
                                          region=(0, 0, halfscreenwidth, screenheight))
    (destx), (desty) = dest
    pyautogui.moveTo((destx + (random.randint(-1, 200))), (desty + (random.randint(-3, 3))),
                     mouse.move_time(), mouse.mouse_path())
    mouse.click_right()  # right click to open dropdown menu
    pyautogui.moveRel((0 + (random.randint(10, 80))), (0 + (random.randint(20, 25))),
                      mouse.move_time(), mouse.mouse_path())
    mouse.click()  # click edit location in drop down
    time.sleep(float(random.randint(1000, 3000)) / 1000)
    pyautogui.keyDown('home')
    time.sleep(float(random.randint(0, 3000)) / 1000)
    pyautogui.keyUp('home')
    time.sleep(float(random.randint(0, 3000)) / 1000)
    pyautogui.keyDown('e')  # an an 'e' to beginning of name indicating station is empty
    pyautogui.keyUp('e')
    time.sleep(float(random.randint(0, 3000)) / 1000)
    pyautogui.keyDown('enter')
    time.sleep((random.randint(0, 200)) / 100)
    pyautogui.keyUp('enter')
    return


# determine which station ship is currently at, then set destination one number higher
def set_dest():
    at_dest_num_dyn()
    next_dest = pyautogui.locateCenterOnScreen(('./img/dest/dest' + (destnum[at_dest_num_var + 1]) + '.bmp'),
                                               confidence=conf,
                                               region=(0, 0, halfscreenwidth, screenheight))
    next_dest_var = (at_dest_num_var + 1)
    while next_dest is None:
        next_dest_var = next_dest_var + 1
        next_dest = pyautogui.locateCenterOnScreen(('./img/dest/dest' + (destnum[next_dest_var]) + '.bmp'),
                                                   confidence=conf,
                                                   region=(0, 0, halfscreenwidth, screenheight))
        print('looking for dest' + (destnum[next_dest_var]))
    if next_dest is not None:
        print('setting destination waypoint')
        (next_destx), (next_desty) = next_dest
        pyautogui.moveTo((next_destx + (random.randint(-1, 200))), (next_desty + (random.randint(-3, 3))),
                         mouse.move_time(), mouse.mouse_path())
        mouse.click_right()  # right click to open dropdown menu
        pyautogui.moveRel((0 + (random.randint(10, 80))), (0 + (random.randint(20, 25))),
                          mouse.move_time(), mouse.mouse_path())
        mouse.click()  # click set destination in drop down
        set_dest_dyn_var = (destnum[at_dest_num_var + 1])
        return


# check if ship has arrived back at its home station by looking for an entry in 'people and places' starting with 3 0's
def at_home_check():
    # search left half of screen only
    global at_home_check_var
    at_home = pyautogui.locateCenterOnScreen('./img/dest/at_dest0.bmp', confidence=conf,
                                             region=(0, 0, halfscreenwidth, screenheight))
    if at_home is None:
        at_home_check_var = 0
        return
    elif at_home is not None:
        print('at home station')
        at_home_check_var = 1
        return


def set_home():  # return to home station (has 000 in front of name in 'people and places')
    print('setting home waypoint')
    home = pyautogui.locateCenterOnScreen('./img/dest/dest0.bmp', confidence=conf,
                                          region=(0, 0, halfscreenwidth, screenheight))
    (homex, homey) = home
    pyautogui.moveTo((homex + (random.randint(-1, 200))), (homey + (random.randint(-3, 3))),
                     mouse.move_time(), mouse.mouse_path())
    mouse.click_right()  # right click to open dropdown menu
    pyautogui.moveRel((0 + (random.randint(10, 80))), (0 + (random.randint(20, 25))),
                      mouse.move_time(), mouse.mouse_path())
    mouse.click()  # click set destination in drop down
    return


'''
# check if ship has arrived back at its destination by looking for a green entry in 'people and places'
def at_dest1_check():
    global at_dest1_check_var
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
    global set_dest1_var
    dest1 = pyautogui.locateCenterOnScreen('dest1.bmp', confidence=conf,
                                           region=(0, 0, halfscreenwidth, screenheight))
    if dest1 is not None:
        (dest1x, dest1y) = dest1
        pyautogui.moveTo((dest1x + (random.randint(-1, 200))), (dest1y + (random.randint(-3, 3))),
                         mouse.move_time(), mouse.mouse_path())
        mouse.click_right()  # right click to open dropdown menu
        pyautogui.moveRel((0 + (random.randint(10, 80))), (0 + (random.randint(20, 25))),
                          mouse.move_time(), mouse.mouse_path())
        mouse.click()  # click set destination in drop down
        set_dest1_var = 1
        return
    if dest1 is None:  # if cannot locate name, then station must be blacklisted
        set_dest1_var = 0
        return


# check if ship has arrived back at its destination by looking for a green entry in 'people and places'
def at_dest2_check():
    global at_dest2_check_var
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


def set_dest2():  # set station with 222 before name as destination in 'people and places'
    global set_dest2_var
    dest2 = pyautogui.locateCenterOnScreen('dest2.bmp', confidence=conf,
                                           region=(0, 0, halfscreenwidth, screenheight))
    if dest2 is not None:
        (dest2x, dest2y) = dest2
        pyautogui.moveTo((dest2x + (random.randint(-1, 200))), (dest2y + (random.randint(-3, 3))),
                         mouse.move_time(), mouse.mouse_path())
        mouse.click_right()  # right click to open dropdown menu
        pyautogui.moveRel((0 + (random.randint(10, 80))), (0 + (random.randint(20, 25))),
                          mouse.move_time(), mouse.mouse_path())
        mouse.click()  # click set destination in drop down
        set_dest2_var = 1
        return
    if dest2 is None:
        set_dest2_var = 0
        return


# check if ship has arrived back at its destination by looking for a green entry in 'people and places'
def at_dest3_check():
    global at_dest3_check_var
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


def set_dest3():  # set station with 333 before name as destination in 'people and places'
    global set_dest3_var
    dest3 = pyautogui.locateCenterOnScreen('dest3.bmp', confidence=conf,
                                           region=(0, 0, halfscreenwidth, screenheight))
    if dest3 is not None:
        (dest3x, dest3y) = dest3
        pyautogui.moveTo((dest3x + (random.randint(-1, 200))), (dest3y + (random.randint(-3, 3))),
                         mouse.move_time(), mouse.mouse_path())
        mouse.click_right()  # right click to open dropdown menu
        pyautogui.moveRel((0 + (random.randint(10, 80))), (0 + (random.randint(20, 25))),
                          mouse.move_time(), mouse.mouse_path())
        mouse.click()  # click set destination in drop down
        set_dest3_var = 1
        return
    if dest3 is None:
        set_dest3_var = 0
        return


# check if ship has arrived back at its destination by looking for a green entry in 'people and places'
def at_dest4_check():
    global at_dest4_check_var
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


def set_dest4():  # set station with 444 before name as destination in 'people and places'
    global set_dest4_var
    dest4 = pyautogui.locateCenterOnScreen('dest5.bmp', confidence=conf,
                                           region=(0, 0, halfscreenwidth, screenheight))
    if dest4 is not None:
        (dest4x, dest4y) = dest4
        pyautogui.moveTo((dest4x + (random.randint(-1, 200))), (dest4y + (random.randint(-3, 3))),
                         mouse.move_time(), mouse.mouse_path())
        mouse.click_right()  # right click to open dropdown menu
        pyautogui.moveRel((0 + (random.randint(10, 80))), (0 + (random.randint(20, 25))),
                          mouse.move_time(), mouse.mouse_path())
        mouse.click()  # click set destination in drop down
        set_dest4_var = 1
        return
    if dest4 is None:
        set_dest4_var = 0
        return


# check if ship has arrived back at its destination by looking for a green entry in 'people and places'
def at_dest5_check():
    global at_dest5_check_var
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


def set_dest5():  # set station with 555 before name as destination in 'people and places'
    print('at home station, setting destination waypoint')
    global set_dest5_var
    dest5 = pyautogui.locateCenterOnScreen('dest5.bmp', confidence=conf,
                                           region=(0, 0, halfscreenwidth, screenheight))
    if dest5 is not None:
        (dest5x, dest5y) = dest5
        pyautogui.moveTo((dest5x + (random.randint(-1, 200))), (dest5y + (random.randint(-3, 3))),
                         mouse.move_time(), mouse.mouse_path())
        mouse.click_right()  # right click to open dropdown menu
        pyautogui.moveRel((0 + (random.randint(10, 80))), (0 + (random.randint(20, 25))),
                          mouse.move_time(), mouse.mouse_path())
        mouse.click()  # click set destination in drop down
        set_dest5_var = 1
        return
    if dest5 is None:
        set_dest5_var = 0
        return


def blacklist_station():  # change location's name so ship doesn't return to it
    at_dest1_check()
    at_dest2_check()
    at_dest3_check()
    at_dest4_check()
    at_dest5_check()
    if at_dest1_check_var == 1:
        dest1 = pyautogui.locateCenterOnScreen('at_dest1.bmp', confidence=conf,
                                               region=(0, 0, halfscreenwidth, screenheight))
        (dest1x, dest1y) = dest1
        pyautogui.moveTo((dest1x + (random.randint(-1, 200))), (dest1y + (random.randint(-3, 3))),
                         mouse.move_time(), mouse.mouse_path())
        mouse.click_right()  # right click to open dropdown menu
        pyautogui.moveRel((0 + (random.randint(10, 80))), (0 + (random.randint(56, 67))),
                          mouse.move_time(), mouse.mouse_path())
        mouse.click()  # click edit location in drop down
        time.sleep(1)
        pyautogui.keyDown('home')
        pyautogui.keyUp('home')
        time.sleep(1)
        pyautogui.keyDown('e')  # an an 'e' to beginning of name indicating station is empty
        pyautogui.keyUp('e')
        time.sleep(1)
        pyautogui.keyDown('enter')
        pyautogui.keyUp('enter')
        return
    if at_dest2_check_var == 1:
        dest2 = pyautogui.locateCenterOnScreen('at_dest2.bmp', confidence=conf,
                                               region=(0, 0, halfscreenwidth, screenheight))
        (dest2x, dest2y) = dest2
        pyautogui.moveTo((dest2x + (random.randint(-1, 200))), (dest2y + (random.randint(-3, 3))),
                         mouse.move_time(), mouse.mouse_path())
        mouse.click_right()  # right click to open dropdown menu
        pyautogui.moveRel((0 + (random.randint(10, 80))), (0 + (random.randint(56, 67))),
                          mouse.move_time(), mouse.mouse_path())
        mouse.click()  # click edit location in drop down
        time.sleep(1)
        pyautogui.keyDown('home')
        pyautogui.keyUp('home')
        time.sleep(1)
        pyautogui.keyDown('e')  # an an 'e' to beginning of name indicating station is empty
        pyautogui.keyUp('e')
        time.sleep(1)
        pyautogui.keyDown('enter')
        pyautogui.keyUp('enter')
        return
    if at_dest3_check_var == 1:
        dest3 = pyautogui.locateCenterOnScreen('at_dest3.bmp', confidence=conf,
                                               region=(0, 0, halfscreenwidth, screenheight))
        (dest3x, dest3y) = dest3
        pyautogui.moveTo((dest3x + (random.randint(-1, 200))), (dest3y + (random.randint(-3, 3))),
                         mouse.move_time(), mouse.mouse_path())
        mouse.click_right()  # right click to open dropdown menu
        pyautogui.moveRel((0 + (random.randint(10, 80))), (0 + (random.randint(56, 67))),
                          mouse.move_time(), mouse.mouse_path())
        mouse.click()  # click edit location in drop down
        time.sleep(1)
        pyautogui.keyDown('home')
        pyautogui.keyUp('home')
        time.sleep(1)
        pyautogui.keyDown('e')  # an an 'e' to beginning of name indicating station is empty and preventing image
        # search from finding it
        pyautogui.keyUp('e')
        time.sleep(1)
        pyautogui.keyDown('enter')
        pyautogui.keyUp('enter')
        return
    if at_dest4_check_var == 1:
        dest4 = pyautogui.locateCenterOnScreen('at_dest4.bmp', confidence=conf,
                                               region=(0, 0, halfscreenwidth, screenheight))
        (dest4x, dest4y) = dest4
        pyautogui.moveTo((dest4x + (random.randint(-1, 200))), (dest4y + (random.randint(-3, 3))),
                         mouse.move_time(), mouse.mouse_path())
        mouse.click_right()  # right click to open dropdown menu
        pyautogui.moveRel((0 + (random.randint(10, 80))), (0 + (random.randint(56, 67))),
                          mouse.move_time(), mouse.mouse_path())
        mouse.click()  # click edit location in drop down
        time.sleep(1)
        pyautogui.keyDown('home')
        pyautogui.keyUp('home')
        time.sleep(1)
        pyautogui.keyDown('e')  # an an 'e' to beginning of name indicating station is empty
        pyautogui.keyUp('e')
        time.sleep(1)
        pyautogui.keyDown('enter')
        pyautogui.keyUp('enter')
        return
    if at_dest5_check_var == 1:
        dest5 = pyautogui.locateCenterOnScreen('at_dest1.bmp', confidence=conf,
                                               region=(0, 0, halfscreenwidth, screenheight))
        (dest5x, dest5y) = dest5
        pyautogui.moveTo((dest5x + (random.randint(-1, 200))), (dest5y + (random.randint(-3, 3))),
                         mouse.move_time(), mouse.mouse_path())
        mouse.click_right()  # right click to open dropdown menu
        pyautogui.moveRel((0 + (random.randint(10, 80))), (0 + (random.randint(56, 67))),
                          mouse.move_time(), mouse.mouse_path())
        mouse.click()  # click edit location in drop down
        time.sleep(1)
        pyautogui.keyDown('home')
        pyautogui.keyUp('home')
        time.sleep(1)
        pyautogui.keyDown('e')  # an an 'e' to beginning of name indicating station is empty
        pyautogui.keyUp('e')
        time.sleep(1)
        pyautogui.keyDown('enter')
        pyautogui.keyUp('enter')
        return
    else:
        print('no known stations found')
        sys.exit()


def next_destination():  # set next destination based on station blacklist and current location
    at_home_check()
    at_dest1_check()
    at_dest2_check()
    at_dest3_check()
    at_dest4_check()
    at_dest5_check()
    # check if at home
    if at_home_check_var == 1:
        set_dest1()  # set destination only if at home and station is not empty
        if set_dest1_var == 0:
            set_dest2()
            if set_dest2_var == 0:
                set_dest3()
                if set_dest3_var == 0:
                    set_dest4()
                    if set_dest4_var == 0:
                        set_dest5()
                        if set_dest5_var == 0:
                            print('all done!')
                            sys.exit()
    elif at_dest1_check_var == 1:
        set_dest2()
        if set_dest2_var == 0:
            set_dest3()
            if set_dest3_var == 0:
                set_dest4()
                if set_dest4_var == 0:
                    set_dest5()
                    if set_dest5_var == 0:
                        set_home()
    elif at_dest2_check_var == 1:
        set_dest3()
        if set_dest3_var == 0:
            set_dest4()
            if set_dest4_var == 0:
                set_dest5()
                if set_dest5_var == 0:
                    set_dest1()
                    if set_dest1_var == 0:
                        set_home()
                        return
    elif at_dest3_check_var == 1:
        set_dest4()
        if set_dest4_var == 0:
            set_dest5()
            if set_dest5_var == 0:
                set_dest1()
                if set_dest1_var == 0:
                    set_dest2()
                    if set_dest2_var == 0:
                        set_home()
                        return
    elif at_dest4_check_var == 1:
        set_dest5()
        if set_dest5_var == 0:
            set_dest1()
            if set_dest1_var == 0:
                set_dest2()
                if set_dest2_var == 0:
                    set_dest3()
                    if set_dest3_var == 0:
                        set_home()
                        return
    elif at_dest5_check_var == 1:
        set_dest1()
        if set_dest1_var == 0:
            set_dest2()
            if set_dest2_var == 0:
                set_dest3()
                if set_dest3_var == 0:
                    set_dest4()
                    if set_dest4_var == 0:
                        set_home()
                        return
'''
