import sys
import time
import logging
import random
import traceback
import pyautogui as pag
from lib import mouse, keyboard, overview
from lib.vars import originx, originy, windowx, windowy

sys.setrecursionlimit(9999999)

logging.basicConfig(format='(%(levelno)s) %(asctime)s - %(funcName)s -- %('
                           'message)s', level=logging.DEBUG)

def detect_route():
    # Check the top-left corner of the hud to see if a route has actually been
    # set by the user.
    route_set_var = pag.locateCenterOnScreen('./img/indicators/detect_route.bmp',
                                             confidence=0.85,
                                             region=(originx, originy,
                                                     windowx, windowy))
    if route_set_var is None:
        logging.error('no route set!')
        sys.exit(0)
    else:
        return


def warp_to_waypoint():
    # Click on the current waypoint and use warp hotkey to warp to waypoint.
    # Currently supports warping to stargate and station waypoints.
    logging.debug('looking for waypoints')
    tries = 0
    # Speed up image searching by checking right half of eve window only. This
    # obviously requires the user to place the overview on the right half of
    # the client window.
    stargate_waypoint = pag.locateCenterOnScreen(
        './img/overview/stargate_waypoint.bmp',
        confidence=0.96,
        region=(originx, originy, windowx, windowy))
    # If stargate waypoint not found, look for station waypoint.
    while stargate_waypoint is None and tries <= 15:
        tries += 1
        station_waypoint = pag.locateCenterOnScreen(
            './img/overview/station_waypoint.bmp',
            confidence=0.96,
            region=(originx, originy, windowx, windowy))
        # If station waypoint not found, look for stargate waypoint again
        # and restart loop.
        if station_waypoint is None:
            stargate_waypoint = pag.locateCenterOnScreen(
                './img/overview/stargate_waypoint.bmp',
                confidence=0.96,
                region=(originx, originy, windowx, windowy))
            logging.debug('looking for waypoints ' + (str(tries)))
            time.sleep(float(random.randint(400, 1200)) / 1000)
            continue
        elif station_waypoint is not None:
            logging.debug('found station waypoint')
            (station_waypointx, station_waypointy) = station_waypoint
            pag.moveTo((station_waypointx + (random.randint(-8, 8))),
                       (station_waypointy + (random.randint(-8, 8))),
                       mouse.duration(), mouse.path())
            pag.keyDown('d')  # 'dock' hotkey.
            time.sleep(float(random.randint(600, 1200)) / 1000)
            mouse.click()
            pag.keyUp('d')
            # Move mouse away from overview to prevent tooltips from blocking
            # script from seeing the icons.
            pag.moveTo((random.randint(0, (windowy - 100))),
                       (random.randint(0, ((windowx - 100) / 2))),
                       mouse.duration(), mouse.path())
            return 2

    # Check if stargate waypoint was found before loop expired.
    if stargate_waypoint is not None and tries <= 15:
        logging.debug('found stargate waypoint')
        (stargate_waypointx, stargate_waypointy) = stargate_waypoint
        pag.moveTo((stargate_waypointx + (random.randint(-8, 8))),
                   (stargate_waypointy + (random.randint(-8, 8))),
                   mouse.duration(), mouse.path())
        pag.keyDown('d')
        time.sleep(float(random.randint(600, 1200)) / 1000)
        mouse.click()
        pag.keyUp('d')
        pag.moveTo(
            (random.randint(150, (int(windowy - (windowy / 4))))),
            (random.randint(150, (int(windowx - (windowx / 4))))),
            mouse.duration(), mouse.path())
        return 1
    elif stargate_waypoint is None and tries > 15:
        logging.error('no waypoints found')
        emergency_terminate()
        traceback.print_stack()
        sys.exit()


def detect_warp_loop():
    # Detect when a warp has been completed by waiting for the 'warping' text
    # to disappear from the spedometer. Wait for the ship to begin its warp
    # before checking though, otherwise the script will think the warp has
    # already been completed.
    warp_duration = 1
    time.sleep(1)
    warp_drive_active = pag.locateCenterOnScreen(
        './img/indicators/warping.bmp',
        confidence=0.90,
        region=(originx, originy, windowx,
                windowy))

    # Wait for warp to begin by waiting until the spedometer is full. Ship
    # might be stuck on something so this could take an variable amount of
    # time.
    while warp_drive_active is None and warp_duration <= 300:
        logging.debug('waiting for warp to start ' + (str(warp_duration)))
        time.sleep(float(random.randint(1000, 3000)) / 1000)
        warp_duration += 1
        warp_drive_active = pag.locateCenterOnScreen(
            './img/indicators/warping.bmp',
            confidence=0.9,
            region=(originx, originy, windowx,
                    windowy))

    # Wait up to 300 seconds before concluding there was an error with the
    # function.
    while warp_drive_active is not None and warp_duration <= 150:
        # print('warp icon found at', warp_drive_active)
        logging.debug('warping ' + (str(warp_duration)))
        warp_duration += 1
        time.sleep(2)
        warp_drive_active = pag.locateCenterOnScreen(
            './img/indicators/warping.bmp',
            confidence=0.9,
            region=(originx, originy, windowx,
                    windowy))

    if warp_drive_active is None and warp_duration <= 150:
        time.sleep(float(random.randint(1000, 3000)) / 1000)
        logging.debug('warp completed')
        return 1
    else:
        logging.error('timed out waiting for warp')
        emergency_terminate()
        return 0


def detect_jump_loop():
    # Detect a jump by looking for the cyan session-change icon in top left
    # corner of the eve client window. If a jump hasn't been detected after
    # 50 checks, check if the 'low security system warning' window has appeared
    # and is preventing the ship from jumping.
    tries = 0
    detect_jump_var = pag.locateCenterOnScreen(
        './img/indicators/session_change_cloaked.bmp',
        # Confidence must be lower than normal since icon is partially
        # transparent.
        confidence=0.55, region=(originx, originy, windowx, windowy))

    while detect_jump_var is None and tries <= 180:
        tries += 1
        logging.debug('waiting for jump ' + (str(tries)))
        time.sleep(1.5)
        detect_jump_var = pag.locateCenterOnScreen(
            './img/indicators/session_change_cloaked.bmp',
            confidence=0.55,
            region=(originx, originy, windowx, windowy))

        if detect_jump_var is not None and tries >= 50:
            low_sec_popup = pag.locateCenterOnScreen(
                './img/warnings/low_security_system.bmp',
                confidence=0.9,
                region=(originx, originy, windowx, windowy))

            if low_sec_popup is not None:
                keyboard.keypress('enter')
                continue
            else:
                continue

    if detect_jump_var is not None and tries <= 180:
        logging.debug('jump detected ' + (str(tries)))
        time.sleep(float(random.randint(900, 2400)) / 1000)
        return 1

    else:
        logging.error('timed out looking for jump ' + (str(tries)))
        emergency_terminate()
        traceback.print_stack()
        sys.exit()


def detect_dock_loop():
    # Detect a station dock by looking for undock_loop icon on the right half of the
    # eve client window.
    tries = 0
    detect_dock_var = pag.locateCenterOnScreen('./img/buttons/undock.bmp',
                                               confidence=0.91,
                                               region=(originx, originy,
                                                       windowx, windowy))
    while detect_dock_var is None and tries <= 100:
        tries += 1
        logging.debug('waiting for dock ' + (str(tries)))
        time.sleep(3)
        detect_dock_var = pag.locateCenterOnScreen('./img/buttons/undock.bmp',
                                                   confidence=0.91,
                                                   region=(originx, originy,
                                                           windowx, windowy))
    if detect_dock_var is not None and tries <= 100:
        logging.debug('detected dock ' + (str(tries)))
        time.sleep(float(random.randint(2000, 5000)) / 1000)
        return 1
    else:
        logging.error('timed out looking for dock ' + (str(tries)))
        return 0


def emergency_terminate():
    # If a function breaks or times out while undocked, look for the nearest
    # station and dock immediately. Incrementally lower the confidence required
    # to match station icon each time the loop runs in order to guarantee
    # a warp.
    # If a station cannot be found after 20 loops,
    # warp to the nearest celestial body and keep at a distance of >100 km. 
    # After warp completes, force an unsafe logout in space.
    logging.debug('EMERGENCY TERMINATE CALLED !!!')
    tries = 0
    confidence = 0.95
    overview.focus_overview_tab('general')
    station_icon = pag.locateCenterOnScreen('./img/overview/station.bmp',
                                            confidence=confidence,
                                            region=((originx + (windowx - (
                                                int(windowx / 3.8)))),
                                                    originy,
                                                    (int(windowx / 3.8)),
                                                    windowy))

    # Look for a station to dock at until confidence is <0.85
    while station_icon is None and tries <= 15:
        logging.debug('looking for station to dock at, confidence = '
                      + (str(confidence)) + ' ' + (str(tries)))
        tries += 1
        time.sleep(float(random.randint(600, 1200)) / 1000)
        station_icon = pag.locateCenterOnScreen('./img/station_icon.bmp',
                                                confidence=confidence,
                                                region=((originx + (windowx - (
                                                    int(windowx / 3.8)))),
                                                        originy,
                                                        (int(windowx / 3.8)),
                                                        windowy))
    if station_icon is not None and tries <= 15:
        logging.debug('emergency docking ' + (str(tries)))
        (station_iconx, station_icony) = station_icon
        pag.moveTo((station_iconx + (random.randint(-2, 50))),
                   (station_icony + (random.randint(-2, 2))),
                   mouse.duration(), mouse.path())
        mouse.click()
        time.sleep(float(random.randint(600, 1200)) / 1000)
        pag.keyDown('d')
        time.sleep(float(random.randint(600, 1200)) / 1000)
        pag.keyUp('d')
        pag.moveTo(
            (random.randint(150, (int(windowy - (windowy / 4))))),
            (random.randint(150, (int(windowx - (windowx / 4))))),
            mouse.duration(), mouse.path())
        if detect_dock_loop() == 1:
            emergency_logout()
        elif detect_dock_loop() == 0:
            time.sleep(float(random.randint(60000, 120000)) / 1000)
            emergency_logout()
        return 0

    # If confidence lowers below threshold, try warping to a planet
    # instead.
    else:
        logging.debug('could not find station to emergency dock at, warping to'
                      'celestial body instead ' + (str(tries)))
        confidence = 1
        overview.focus_overview_tab('warpto')
        planet = pag.locateCenterOnScreen(
            './img/overview/planet.bmp',
            confidence=confidence,
            region=((originx + (windowx - (int(windowx / 3.8)))),
                    originy, (int(windowx / 3.8)), windowy))
        while planet is None and tries <= 50:
            logging.debug('looking for planet ' + (str(tries)) + ' ' +
                          (str(confidence)))
            tries += 1
            # Lower confidence on every third try.
            if (tries % 3) == 0:
                confidence -= 0.01
            time.sleep(float(random.randint(600, 2000)) / 1000)
            planet = pag.locateCenterOnScreen(
                './img/overview/planet.bmp',
                confidence=confidence,
                region=((originx + (windowx - (int(windowx / 3.8)))),
                        originy, (int(windowx / 3.8)), windowy))

        if planet is not None and tries <= 50:
            logging.debug('emergency warping to planet ' + (str(tries)))
            (x, y) = planet
            pag.moveTo((x + (random.randint(-2, 50))),
                       (y + (random.randint(-2, 2))),
                       mouse.duration(), mouse.path())
            mouse.click()
            time.sleep(float(random.randint(600, 1200)) / 1000)
            keyboard.keypress('s')
            pag.moveTo((random.randint(150, (
                int(windowy - (windowy / 4))))),
                       (random.randint(150, (
                           int(windowx - (windowx / 4))))),
                       mouse.duration(), mouse.path())
            detect_warp_loop()
            emergency_logout()
            return 0
        else:
            logging.debug('timed out looking for planet ' + (str(tries)))
            emergency_logout()
        return 1


def emergency_logout():
    # use hotkey to forcefully kill client session, don't use the 'log off
    # safely' feature
    # ALT SHIFT Q
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
