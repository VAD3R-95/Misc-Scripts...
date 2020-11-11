import pyautogui
import math
import time
import sys

def drag_square(distance):
    pyautogui.drag(distance, 0, duration=0.5)   # move right
    pyautogui.drag(0, distance, duration=0.5)   # move down
    pyautogui.drag(-distance, 0, duration=0.5)  # move left
    pyautogui.drag(0, -distance, duration=0.5)  # move up
        
start_time = time.time()
try:
    while True:
        print("--------Running Auto Script--------- :)")
        drag_square(200)
        time.sleep(1)
        pyautogui.press('alt')
except KeyboardInterrupt:
    print("Total: %s minutes " % round(((time.time() - start_time) / 60),2))
    print("Interrupt Found...Exiting")
    sys.exit()    

