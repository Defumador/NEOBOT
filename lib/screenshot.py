import autopy as autopy
import numpy
import pyautogui
import imutils
import pyscreeze
import cv2

def take_screenshot():  # take screenshot of the entire screen and save file to current working directory
    image = pyautogui.screenshot()
    image = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)
    cv2.imwrite("in_memory_to_disk.png", image)

    img_rgb = cv2.imread('in_memory_to_disk.png')
    template = cv2.imread('dock_button_icon.png',0)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img_rgb,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = numpy.where( res >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    cv2.imwrite('res.png',img_rgb)

take_screenshot()