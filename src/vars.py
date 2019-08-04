# encoding: utf-8
# import pyximport
# pyximport.install(pyimport=True)
import sys
import pyautogui as pag

# CUSTOM CONFIGS THAT MUST BE SET MANUALLY ON THE EVE CLIENT
# HOTKEYS
# general tab > exit station > ctrl-u
# drones tab > launch drones > shift-l

# OVERVIEW
# default warpto tab should have only planets and stations, nothing else
# default mining tab should have only asteroids, nothing else
# default general tab should have stations, gates, and ships, nothing else

# MISC
# for mining, default orbit distance must be within the range of mining lasers
# right click on item > orbit > set default
# drones should be set to 'agressive'
# click on hamburger menu in top left corner of drone window > agressive

gotosite = 0

# timervar = 0

sys.setrecursionlimit(9999999)  # set high recursion limit for functions that
# call themselves.

conf = 0.95

#target_lock_time = 2  # Seconds (rounded up) current ship takes to lock a
# target on average.

system_mining = 1  # Tell the miner script if you're mining in the same
# system you're storing your ore in. 1 is yes, 0 is no.

window_resolutionx = 1024
window_resolutiony = 768

# TODO: check for client after clicking 'start' button, not after beginning
#  script
# Get the coordinates of the eve client window and restrict image searching to
# within these boundaries.
# search for the eve neocom logo in top left corner of the eve client window.
# This will become the origin of the coordinate system.
origin = pag.locateCenterOnScreen('./img/buttons/neocom.bmp', confidence=0.90)
if origin is None:
    print("origin -- can't find client!")
    sys.exit(0)
else:
    (originx, originy) = origin

# Move the origin up and to the left slightly to get it to the exact top
# left corner of the eve client window. This is necessary  because the image
# searching algorithm returns coordinates to the center of the image rather
# than its top right corner.
originx -= 20
originy -= 20
windowx = window_resolutionx
windowy = window_resolutiony

