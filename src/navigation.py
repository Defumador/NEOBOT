# encoding: utf-8
import sys
import time
import logging
import random
import traceback

import pyautogui as pag

from src import mouse, keyboard as key, overview, locate as lo
from src.vars import originx, originy, windowx, windowy

sys.setrecursionlimit(9999999)


def has_route():
    """Checks the top-left corner of the client window to see if a route has actually been
    set by the user."""
    route_set_var = lo.locate('./img/indicators/detect_route.bmp', conf=0.85)
    if route_set_var is None:
        logging.error('no route set!')
        sys.exit(0)
    else:
        return


def warp_to_waypoint():
    """Clicks on the current waypoint and uses the warp hotkey to warp to waypoint.
     Currently only supports warping to stargate and station waypoints."""
    # TODO: add support for warping to citadels and engineering complexes
    logging.debug('looking for waypoints')
    # Speed up image searching by looking within overview only. This
    # obviously requires the user to place the overview on the right side of
    # the client window.
    
    for tries in range(1, 15)
        stargate = lo.oclocate('./img/overview/stargate_waypoint.bmp', conf=0.96)
        if stargate is not None:
            logging.debug('found stargate waypoint')
            (x, y) = stargate
            pag.moveTo((x + (random.randint(-8, 30)))), 
                        (y + (random.randint(-8, 8))), 
                        mouse.duration(), mouse.path()
            mouse.click()
            key.keypress('d')  # 'dock / jump' hotkey.
            # Move mouse to the left side of the client to prevent
            # tooltips from interfering with image searches.
            mouse.move_away('l')
            return 2
        
        station = lo.oclocate('./img/overview/station_waypoint.bmp', conf=0.96)
        if station is not None:
            logging.debug('found station waypoint')
            (x, y) = station
            pag.moveTo((x + (random.randint(-8, 30))),
                       (y + (random.randint(-8, 8))),
                       mouse.duration(), mouse.path())
            mouse.click()
            key.keypress('d')
            mouse.move_away('l')
            return 2

        if stargate is None and station is None:
            time.sleep(float(random.randint(500, 1500)) / 1000)
            logging.debug('looking for waypoints ' + (str(tries)))
        
    logging.error('no waypoints found')
    return 0


def wait_for_warp_to_complete():
    """Detects when a warp has started and been
    completed by watching the spedometer."""
    warp_duration = 1
    # TODO: force ship to wait a minimum period of time while beginning its
    # warp, similar to what tinyminer does to eliminate possible issues.
    
    # Wait for warp to begin by waiting until the speedometer is full. Ship
    # might be stuck on something so this could take an variable amount of
    # time.
    warping = lo.locate('./img/indicators/warping2.bmp', conf=0.94)
    while warping is None and warp_duration <= 300:
        warp_duration += 1
        logging.debug('waiting for warp to start ' + (str(warp_duration)))
        time.sleep(float(random.randint(500, 1000)) / 1000)
        warping = lo.locate('./img/indicators/warping2.bmp', conf=0.94)

    # Once warp begins, wait for warp to end by waiting for the 'warping'
    # text on the spedometer to disappear.
    time.sleep(float(random.randint(3000, 5000)) / 1000)
    while warping is not None and warp_duration <= 300:
        warp_duration += 1
        logging.debug('warping ' + (str(warp_duration)))
        time.sleep(float(random.randint(1000, 3000)) / 1000)
        warping = lo.locate('./img/indicators/warping3.bmp', conf=0.9)

    if warping is None and warp_duration <= 300:
        time.sleep(float(random.randint(1000, 3000)) / 1000)
        logging.debug('warp completed')
        return 1
    else:
        logging.error('error warping or timed out waiting for warp to \
                      complete')
        return 0


def wait_for_jump():
    """Waits for a jump by looking for the cyan session-change icon in top left
    corner of the client window. Also checks if the 'low security system warning'
    window has appeared and is preventing the ship from jumping. Times out after
    about four minutes."""
    # Confidence must be lower than normal since icon is partially
    # transparent.
    for tries in range(1, 240)
        jumped = lo.locate('./img/indicators/session_change_cloaked.bmp', conf=0.55)
        
        if jumped is not None:
            logging.debug('jump detected')
            time.sleep(float(random.randint(1000, 2000)) / 1000)
            return 1
        
        elif jumped is None:
            losec = lo.locate('./img/warnings/low_security_system.bmp', conf=0.9)
            if losec is not None:
                time.sleep(float(random.randint(2000, 5000)) / 1000)
                key.keypress('enter')
                continue
            
            logging.debug('waiting for jump ' + (str(tries)))
            time.sleep(float(random.randint(5, 20)) / 10)

    logging.error('timed out waiting for jump')
    emergency_terminate()
    traceback.print_stack()
    sys.exit()


def wait_for_dock():
    """Waits for a dock by looking for the undock button on the right half of the
    client window."""
    for tries in range(1, 180)
        docked = lo.locate('./img/buttons/undock.bmp', conf=0.91)
        
        if docked is not None:
            logging.debug('detected dock ' + (str(tries)))
            time.sleep(float(random.randint(1000, 3000)) / 1000)
            return 1
        
        elif docked is None:
            logging.debug('waiting for dock ' + (str(tries)))
            time.sleep(float(random.randint(2000, 5000)) / 1000)
            
    logging.error('timed out waiting for dock')
    return 0


def emergency_terminate():
    """Looks for the nearest station and docks immediately. Incrementally lowers
    the confidence required to match the station icon each time the loop runs
    in order to increase the chances of a warp. If a station cannot be found after a
    certain number of checks, warps to the nearest planet. After warp completes,
    simulates a client disconnection by forcing an unsafe logout in space."""
    logging.warning('EMERGENCY TERMINATE CALLED !!!')
    tries = 0
    confidence = 1
    overview.select_overview_tab('general')
    station_icon = lo.oclocate('./img/overview/station.bmp', conf=confidence)

    # Look for a station to dock at until confidence is <0.85
    while station_icon is None and tries <= 15:
        tries += 1
        confidence -= 0.01
        logging.debug('looking for station to dock at' + (str(tries)) + ', confidence is '
                      + (str(confidence)))
        # Keep time interval relatively short since ship may be in combat.
        time.sleep(float(random.randint(500, 1000)) / 1000)
        station_icon = lo.oclocate('./img/overview/station.bmp', conf=confidence)
        
    if station_icon is not None and tries <= 15:
        logging.debug('emergency docking ' + (str(tries)))
        (x, y) = station_icon
        pag.moveTo((x + (random.randint(-2, 50))),
                   (y + (random.randint(-2, 2))),
                   mouse.duration(), mouse.path())
        mouse.click()
        time.sleep(float(random.randint(600, 1200)) / 1000)
        pag.keyDown('d')
        time.sleep(float(random.randint(600, 1200)) / 1000)
        pag.keyUp('d')
        mouse.move_away('l')
        if wait_for_dock() == 1:
            emergency_logout()
        elif wait_for_dock() == 0:
            time.sleep(float(random.randint(20000, 40000)) / 1000)
            emergency_logout()
        return 0

    # If confidence lowers below threshold, try warping to a planet
    # instead.
    if station_icon is None and tries > 15:
        logging.debug('could not find station to emergency dock at, warping to'
                      'planet instead')
        tries = 0
        confidence = 1
        overview.select_overview_tab('warpto')
        planet = lo.oclocate('./img/overview/planet.bmp', conf=confidence)
        while planet is None and tries <= 50:
            logging.debug('looking for planet ' + (str(tries)) + ', confidence is ' +
                          (str(confidence)))
            tries += 1
            # Lower confidence on every third try.
            if (tries % 3) == 0:
                confidence -= 0.01
            time.sleep(float(random.randint(600, 2000)) / 1000)
            planet = lo.oclocate('./img/overview/planet.bmp', conf=confidence)

        if planet is not None and tries <= 50:
            logging.debug('emergency warping to planet')
            (x, y) = planet
            pag.moveTo((x + (random.randint(-2, 50))),
                       (y + (random.randint(-2, 2))),
                       mouse.duration(), mouse.path())
            mouse.click()
            time.sleep(float(random.randint(600, 1200)) / 1000)
            key.keypress('s')
            mouse.move_away('l')
            wait_for_warp_to_complete()
            emergency_logout()
            return 0
        else:
            logging.debug('timed out looking for planet')
            emergency_logout()
        return 1


def emergency_logout():
    """Forcefully kill the client session, don't use the 'log off
    safely' feature."""
    logging.warning('emergency logout called')
    time.sleep(float(random.randint(1000, 5000)) / 1000)
    pag.keyDown('alt')
    time.sleep(float(random.randint(500, 1000)) / 1000)
    pag.keyDown('shift')
    time.sleep(float(random.randint(500, 1000)) / 1000)
    pag.keyDown('q')
    time.sleep(float(random.randint(300, 1000)) / 1000)
    pag.keyUp('alt')
    time.sleep(float(random.randint(300, 1000)) / 1000)
    pag.keyUp('shift')
    time.sleep(float(random.randint(300, 1000)) / 1000)
    pag.keyUp('q')
    return 0
