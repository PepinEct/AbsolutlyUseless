from pynput.mouse import Controller
import time
import threading
from math import pow
import keyboard
IS_MOVING = True
AUTO_MOVING = False
BOTTOM = 0
mouse = Controller()
#Calculates bottom
oldPos = mouse.position
for x in range(100):
    mouse.position = (mouse.position[0], mouse.position[1]+300)
BOTTOM = mouse.position[1]
mouse.position = oldPos
QUIT = False
WEIGHTING = False
Active_ceil = 0
def TRACK_MOVEMENT():
    global WEIGHTING, QUIT
    oldPos = (0, 0)
    while not QUIT:
        diffX = (mouse.position[0]-oldPos[0])
        diffY = (mouse.position[1]-oldPos[1])
        if diffY < 0:
            diffY /= -1
        if diffX < 0:
            diffX /= -1
        oldPos = mouse.position
        diff = diffX + diffY
        print(diff)
        if diff < 50:
            #print("not moving")
            #Not moving stuff
            if mouse.position[1] != BOTTOM:
                if not threading.active_count() >= Active_ceil:
                    threading.Thread(target=Weigh).start()
                    pass
            time.sleep(1)
        else:
            time.sleep(0.5)
            

def BREAKOUT():
    global QUIT
    while not QUIT:
        if keyboard.is_pressed(" "):
            QUIT = True
 
def Weigh():
    global QUIT, WEIGHTING 
    for x in range(20):
        mouse.position = (mouse.position[0], mouse.position[1]+pow(x, 2))

print(f"BOTTOM: {BOTTOM}")
threading.Thread(target=TRACK_MOVEMENT).start()
threading.Thread(target=BREAKOUT).start()
time.sleep(0.2)
Active_ceil = threading.active_count()+1