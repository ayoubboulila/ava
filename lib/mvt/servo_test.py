'''
Created on 5 feb. 2018

@author: AYB
'''


from servo import Servo
import traceback
from time import sleep

serv = Servo()


try:
    print("starting")
    print("UP/DOWN")
    print("Neutral")
    serv.set_duty_cycle(serv.PWM_UD, 7)
    sleep(1)
    print("move 30 LR")
    serv.move_LR(30)
    print("move 100 LR")
    serv.move_LR(100)
    print("180")
    serv.set_duty_cycle(serv.PWM_UD, 8.5)
    sleep(1)
    
    print("0")
    serv.set_duty_cycle(serv.PWM_UD, 10.5)
    sleep(1)
    
    
    print("right/left")
    print("Neutral")
    serv.set_duty_cycle(serv.PWM_LR, 6)
    sleep(1)
    
    print("180")
    serv.set_duty_cycle(serv.PWM_LR, 10)
    sleep(1)
    
    print("0")
    serv.set_duty_cycle(serv.PWM_LR, 3)
    sleep(1)
    
    
    print("calibrating Neutral")
    serv.set_duty_cycle(serv.PWM_UD, 8.5)
    sleep(0.5)
    serv.set_duty_cycle(serv.PWM_LR, 6)
    sleep(0.5)
except Exception as ex:
    print("exception in main")
    traceback.print_exc()
    serv.clean_up()
finally:
    serv.stop()
    sleep(3)
    serv.clean_up()
