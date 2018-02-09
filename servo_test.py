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
    serv.set_duty_cycle(serv.PWM_UD, 7.5)
    sleep(1)
    
    print("180")
    serv.set_duty_cycle(serv.PWM_UD, 12.5)
    sleep(1)
    
    print("0")
    serv.set_duty_cycle(serv.PWM_UD, 2.5)
    sleep(1)
    
    
    print("right/left")
    print("Neutral")
    serv.set_duty_cycle(serv.PWM_LR, 7.5)
    sleep(1)
    
    print("180")
    serv.set_duty_cycle(serv.PWM_LR, 12.5)
    sleep(1)
    
    print("0")
    serv.set_duty_cycle(serv.PWM_LR, 2.5)
    sleep(1)
    
    
    
    
except Exception as ex:
    print("exception in main")
    traceback.print_exc()
    serv.clean_up()
finally:
    serv.clean_up()