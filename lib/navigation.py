import sys
import time
import ctypes
import random
import traceback

import pyautogui as pag

from lib import mouse

pag.FAILSAFE = True
sys.setrecursionlimit(100000)
conf = 0.95

# get monitor resolution, used to speed up image searching
user32 = ctypes.windll.user32
screenwidth = user32.GetSystemMetrics(0)
screenheight = user32.GetSystemMetrics(1)
halfscreenwidth = (int(screenwidth / 2))
halfscreenheight = (int(screenheight / 2))


def route_set():  # check to see if a route has actually been set
    route = pag.locateCenterOnScreen('./img/route_set.bmp', confidence=0.9,
                                     region=(0, 0, (int(screenwidth / 4)), screenheight))
    if route is None:
        sys.exit('no route set!')
    else:
        return


def focus_overview():  # click on overview to focus EVE window
    pag.moveTo((screenwidth - (random.randint(10, 230))),
               (75 + (random.randint(0, (screenheight - 10)))),
               mouse.move_time(), mouse.mouse_path())
    time.sleep(float(random.randint(50, 500)) / 1000)
    mouse.click()
    return


def select_waypoint_warp_hotkey():  # click on current waypoint and hold down warp hotkey to warp to waypoint
    # look for station icon
    print('looking for waypoints')
    select_waypoint_look_num = 0
    # search right half of screen only for stargate icon
    stargate_waypoint = pag.locateCenterOnScreen('./img/stargate_waypoint.bmp', confidence=0.96,
                                                 region=(halfscreenwidth, 0, screenwidth, screenheight))
    while stargate_waypoint is None and select_waypoint_look_num < 15:
        select_waypoint_look_num += 1
        # if stargate waypoint not found, look for station waypoint
        station_waypoint = pag.locateCenterOnScreen('./img/station_waypoint.bmp', confidence=0.96,
                                                    region=(halfscreenwidth, 0, screenwidth, screenheight))
        # if station waypoint not found, look for stargate waypoint again and restart loop
        if station_waypoint is None:
            stargate_waypoint = pag.locateCenterOnScreen('./img/stargate_waypoint.bmp', confidence=0.96,
                                                         region=(halfscreenwidth, 0, screenwidth, screenheight))
            print('looking for waypoints ...', select_waypoint_look_num)
            time.sleep(float(random.randint(400, 1200)) / 1000)
            continue
        elif station_waypoint is not None:
            print('found station waypoint')
            (station_waypointx, station_waypointy) = station_waypoint  # separate x and y coordinates of location
            pag.moveTo((station_waypointx + (random.randint(-8, 8))),
                       (station_waypointy + (random.randint(-8, 8))),
                       mouse.move_time(), mouse.mouse_path())
            pag.keyDown('d')  # hotkey to hold down to warp when clicking on waypoint in overview
            time.sleep(float(random.randint(600, 1200)) / 1000)
            mouse.click()
            pag.keyUp('d')
            # move mouse away from button to prevent tooltips from blocking other buttons
            pag.moveTo((random.randint(0, (screenheight - 100))),
                       (random.randint(0, ((screenwidth - 100) / 2))),
                       mouse.move_time(), mouse.mouse_path())
            return 2
    # check if stargate waypoint was found before loop expired
    if stargate_waypoint is not None and select_waypoint_look_num < 15:
        print('found stargate waypoint')
        (stargate_waypointx, stargate_waypointy) = stargate_waypoint
        pag.moveTo((stargate_waypointx + (random.randint(-8, 8))),
                   (stargate_waypointy + (random.randint(-8, 8))),
                   mouse.move_time(), mouse.mouse_path())
        pag.keyDown('d')
        time.sleep(float(random.randint(600, 1200)) / 1000)
        mouse.click()
        pag.keyUp('d')
        # move mouse away from button to prevent tooltips from blocking other buttons
        pag.moveTo((random.randint(150, (int(screenheight - (screenheight / 4))))),
                   (random.randint(150, (int(screenwidth - (screenwidth / 4))))),
                   mouse.move_time(), mouse.mouse_path())  # 150 min value to prevent mouse from blocking jump check
        return 1
    else:  # if can't find any waypoints, dock at nearest station
        print('no waypoints found')
        emergency_dock()
        traceback.print_stack()
        sys.exit()


def emergency_dock():
    print('emergency docking')
    emergency_dock_look_num = 0
    # search right half of screen only for stargate icon
    emergency_dock_icon = pag.locateCenterOnScreen('./img/emergency_dock.bmp', confidence=0.9,
                                                   region=(0, 0, screenwidth, screenheight))
    while emergency_dock_icon is None and emergency_dock_look_num < 25:
        emergency_dock_look_num += 1
        time.sleep(1)
        emergency_dock_icon = pag.locateCenterOnScreen('./img/emergency_dock.bmp', confidence=0.9,
                                                       region=(0, 0, screenwidth, screenheight))
    if emergency_dock_icon is not None and emergency_dock_look_num < 25:
        (emergency_dockx, emergency_docky) = emergency_dock_icon
        pag.moveTo((emergency_dockx + (random.randint(-2, 50))),
                   (emergency_docky + (random.randint(-2, 2))),
                   mouse.move_time(), mouse.mouse_path())
        pag.keyDown('d')  # hotkey to hold down to warp when clicking on waypoint in overview
        time.sleep(float(random.randint(600, 1200)) / 1000)
        mouse.click()
        pag.keyUp('d')
        # move mouse away from button to prevent tooltips from blocking other buttons
        pag.moveTo((random.randint(150, (int(screenheight - (screenheight / 4))))),
                   (random.randint(150, (int(screenwidth - (screenwidth / 4))))),
                   mouse.move_time(), mouse.mouse_path())
        return
    else:
        print('cant emergency dock')
        return


'''
def select_waypoint():  # click on current waypoint in overview by looking for either station or stargate icons
    # look for station icon
    print('looking for waypoints')
    select_waypoint_look_num = 0
    # search right half of screen only for stargate icon
    stargate_waypoint = pag.locateCenterOnScreen('./img/stargate_waypoint.bmp', confidence=0.96,
                                                 region=(halfscreenwidth, 0, screenwidth, screenheight))
    while stargate_waypoint is None and select_waypoint_look_num < 100:  # search for waypoints up to 100 times
        select_waypoint_look_num += 1
        # if stargate waypoint not found, look for station waypoint
        station_waypoint = pag.locateCenterOnScreen('./img/station_waypoint.bmp', confidence=0.96,
                                                    region=(halfscreenwidth, 0, screenwidth, screenheight))
        # if station waypoint not found, look for stargate waypoint again and restart loop
        if station_waypoint is None:
            stargate_waypoint = pag.locateCenterOnScreen('./img/stargate_waypoint.bmp', confidence=0.96,
                                                         region=(halfscreenwidth, 0, screenwidth, screenheight))
            print('looking waypoints ...', select_waypoint_look_num)
            time.sleep(3)
            continue
        elif station_waypoint is not None:
            print('found station waypoint')
            # separate x and y coordinates of location
            (station_waypointx, station_waypointy) = station_waypoint
            pag.moveTo((station_waypointx + (random.randint(0, 230))),
                       (station_waypointy + (random.randint(-8, 8))),
                       mouse.move_time(), mouse.mouse_path())
            time.sleep(float(random.randint(100, 1000)) / 1000)
            mouse.click()
            return 2
    # check if stargate waypoint was found before loop expired
    if stargate_waypoint is not None and select_waypoint_look_num < 100:
        print('found stargate waypoint')
        (stargate_waypointx, stargate_waypointy) = stargate_waypoint
        pag.moveTo((stargate_waypointx + (random.randint(-8, 220))),
                   (stargate_waypointy + (random.randint(-8, 8))),
                   mouse.move_time(), mouse.mouse_path())
        time.sleep(float(random.randint(0, 1000)) / 1000)
        mouse.click()
        return 1
    else:  # loop breaks to here
        print('cant find waypoints')
        return -1
'''


def detect_jump():
    detect_jump_loop_num = 0
    spedometer = pag.locateCenterOnScreen('./img/session_change.bmp', confidence=0.55,
                                          region=(0, 0, (int(screenwidth / 5)), screenheight))
    while spedometer is None and detect_jump_loop_num < 180:
        detect_jump_loop_num += 1
        print('waiting for jump...', detect_jump_loop_num)
        time.sleep(1.5)
        # search bottom half of screen only
        spedometer = pag.locateCenterOnScreen('./img/session_change.bmp', confidence=0.55,
                                              region=(0, 0, (int(screenwidth / 5)), screenheight))
    if spedometer is not None and detect_jump_loop_num < 180:
        # if jump detected, warp to next waypoint
        print('jump detected')
        time.sleep(float(random.randint(900, 2400)) / 1000)
        return 1
    else:
        print('timed out looking for jump')
        emergency_dock()
        traceback.print_stack()
        sys.exit()


def detect_dock():
    detect_dock_loop_num = 0
    docked = pag.locateCenterOnScreen('./img/undock.bmp', confidence=0.91,
                                      region=(halfscreenwidth, 0, screenwidth, screenheight))
    while docked is None and detect_dock_loop_num < 80:
        detect_dock_loop_num += 1
        print('waiting for dock...', detect_dock_loop_num)
        time.sleep(3)
        # search bottom half of screen only
        docked = pag.locateCenterOnScreen('./img/undock.bmp', confidence=0.91,
                                          region=(halfscreenwidth, 0, screenwidth, screenheight))
    if docked is not None and detect_dock_loop_num < 80:
        # if jump detected, warp to next waypoint
        print('detected dock')
        time.sleep(float(random.randint(2000, 5000)) / 1000)
        return 1
    else:
        print('timed out looking for dock')
        emergency_dock()
        traceback.print_stack()
        sys.exit()


# use a dictionary to dynamically grab destination names
destnum = {0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7"}


# figure out which destination station ship is at
def at_dest_num():
    global at_dest_num_var
    n = 0
    # confidence must be higher than normal because script frequently mistakes dest3 for dest2
    at_dest = pag.locateCenterOnScreen(('./img/dest/at_dest' + (destnum[n]) + '.bmp'), confidence=0.98,
                                       region=(0, 0, halfscreenwidth, screenheight))
    while at_dest is None:
        n = n + 1
        at_dest = pag.locateCenterOnScreen(('./img/dest/at_dest' + (destnum[n]) + '.bmp'), confidence=0.98,
                                           region=(0, 0, halfscreenwidth, screenheight))
        print('looking if at destination' + (destnum[n]))
        if n > 4:
            print('out of destinations to look for')
            # if not at a recognizable station, undock and continue route
            return -1
    if at_dest is not None:
        print('at dest' + (destnum[n]))
        at_dest_num_var = n
        return at_dest_num_var  # return number of station ship is docked in


def blacklist_station():  # determine which station ship is in and blacklist it by editing its name
    at_dest = at_dest_num()
    if at_dest is not None:
        print('blacklisting station')
        at_dest = pag.locateCenterOnScreen(('./img/dest/at_dest' + (destnum[at_dest_num_var]) + '.bmp'),
                                           confidence=conf,
                                           region=(0, 0, halfscreenwidth, screenheight))
        (at_destx), (at_desty) = at_dest
        pag.moveTo((at_destx + (random.randint(-1, 200))), (at_desty + (random.randint(-3, 3))),
                   mouse.move_time(), mouse.mouse_path())
        mouse.click()  # double-click entry to open edit menu
        time.sleep(float(random.randint(5, 400)) / 1000)
        mouse.click()
        time.sleep(float(random.randint(3000, 4000)) / 1000)
        pag.keyDown('home')
        time.sleep(float(random.randint(0, 500)) / 1000)
        pag.keyUp('home')
        time.sleep(float(random.randint(0, 1000)) / 1000)
        pag.keyDown('e')  # an an 'e' to beginning of name indicating station is empty
        pag.keyUp('e')
        time.sleep(float(random.randint(0, 1000)) / 1000)
        pag.keyDown('enter')
        time.sleep((random.randint(0, 200)) / 100)
        pag.keyUp('enter')
        return
    else:
        return


# set next destination to the lowest-numbered destination that isnt blacklisted (starting with 1)
def set_dest():
    next_dest = pag.locateCenterOnScreen(('./img/dest/dest' + (destnum[1]) + '.bmp'),
                                         confidence=0.98,
                                         region=(0, 0, halfscreenwidth, screenheight))
    next_dest_var = 1
    while next_dest is None:
        next_dest_var = next_dest_var + 1
        next_dest = pag.locateCenterOnScreen(('./img/dest/dest' + (destnum[next_dest_var]) + '.bmp'),
                                             confidence=0.98,
                                             region=(0, 0, halfscreenwidth, screenheight))
        print('looking for dest' + (destnum[next_dest_var]))
    if next_dest is not None:
        print('setting destination waypoint')
        (next_destx), (next_desty) = next_dest
        pag.moveTo((next_destx + (random.randint(-1, 200))), (next_desty + (random.randint(-3, 3))),
                   mouse.move_time(), mouse.mouse_path())
        mouse.click_right()  # right click to open dropdown menu
        pag.moveRel((0 + (random.randint(10, 80))), (0 + (random.randint(20, 25))),
                    mouse.move_time(), mouse.mouse_path())
        mouse.click()  # click set destination in drop down
        time.sleep(2)
        return


# check if ship has arrived back at its home station by looking for an entry in 'people and places' starting with 3 0's
def at_home_check():
    # search left half of screen only
    at_home = pag.locateCenterOnScreen('./img/dest/at_dest0.bmp', confidence=conf,
                                       region=(0, 0, halfscreenwidth, screenheight))
    if at_home is None:
        return 0
    elif at_home is not None:
        print('at home station')
        return 1


def set_home():  # return to home station (has 000 in front of name in 'people and places')
    print('setting home waypoint')
    home = pag.locateCenterOnScreen('./img/dest/dest0.bmp', confidence=conf,
                                    region=(0, 0, halfscreenwidth, screenheight))
    (homex, homey) = home
    pag.moveTo((homex + (random.randint(-1, 200))), (homey + (random.randint(-3, 3))),
               mouse.move_time(), mouse.mouse_path())
    mouse.click_right()  # right click to open dropdown menu
    pag.moveRel((0 + (random.randint(10, 80))), (0 + (random.randint(20, 25))),
                mouse.move_time(), mouse.mouse_path())
    mouse.click()  # click set destination in drop down
    return
