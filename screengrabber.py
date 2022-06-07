import cv2 as cv
import numpy as np
from time import time
from windowcapture import WindowCapture
from vision import Vision


wincap = WindowCapture('Minecraft 1.8.9')

vision_table = Vision('crafting table.png')

loop_time = time()
while(True):

    screenshot = wincap.get_screen()
    #changes color from rgb to BGR for cv2
    #screenshot = screenshot[:, :, ::-1].copy()

    #shows raw screenshot we got, not neccasary becuase we are running it through computer vision first
    #cv.imshow('Computer Vision', screenshot
#    if screenshot is None:
#        continue
    points = vision_table.find(screenshot, 0.5, 'boxes')

    #useing our computer vision
    #points = vision_hay.find(screenshot, 0.5 , 'boxes')

    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()


    #breaks process if q is pressed
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')
