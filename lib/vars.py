import sys

import pyautogui as pag

global windowx
global windowy
global originx
global originy

global conf

global alignment_time

global atsite
global gotosite

atsite = 0
gotosite = 0
sys.setrecursionlimit(9999999)  # set high recursion limit for functions that
# call themselves.

conf = 0.95
alignment_time = 6  # Seconds (rounded up) current ship takes to begin a warp.

window_resolutionx = 1024
window_resolutiony = 768

# Get the coordinates of the eve client window and restrict image searching to
# within these boundaries.
# search for the eve neocom logo in top left corner of the eve client window.
# This will become the origin of the coordinate system.
origin = pag.locateCenterOnScreen('./img/buttons/neocom.bmp', confidence=0.90)
(originx, originy) = origin

# Move the origin up and to the left slightly to get it to the exact top
# left corner of the eve client window. This is necessary  because the image
# searching algorithm returns coordinates to the center of the image rather
# than its top right corner.
originx -= 18
originy -= 18
windowx = originx + window_resolutionx
windowy = originy + window_resolutiony

sys.setrecursionlimit(9999999)
