'''
Created on 5 feb. 2018

@author: AYB
'''


from Servo import SERVO
import traceback
from time import sleep

s = SERVO()


try:
    print("starting")
    print("UP/DOWN")
    print("UP")
    s.look_up()
    sleep(1)
    print("DOWN")
    s.look_down()
    sleep(1)
    
    print("right/left")
    print("left")
    s.look_left()
    sleep(1)
    print("right")
    s.look_right()
    sleep(1)
    
    print("calibrating Neutral")
    s.reset()
    sleep(1)
    
except Exception as ex:
    print("exception in main")
    traceback.print_exc()
    s.clean_up()
finally:
    s.clean_up()
