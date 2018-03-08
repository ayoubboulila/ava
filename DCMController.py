'''
Created on 14 FEB. 2018

@author: AYB
'''


import redis
from datetime import datetime
import json
#from pprint import pprint
import ast
from lib.mvt.AMSpi import AMSpi
import time
from time import sleep
from utils import Logger

DCM_CH = 'DCMC'
log = Logger.RCLog('DCMController')
# json = '{"action": "go",  "speed": "100", "time_limit": "0"}'
# json = '{"action": "back",  "speed": "100", "time_limit": "0"}'
# json = '{"action": "left",  "speed": "100", "time_limit": "0"}'
# json = '{"action": "right",  "speed": "100", "time_limit": "0"}'
# json = '{"action": "stop",  "speed": "0", "time_limit": "0"}'
# json = '{"action": "exit",  "speed": "0", "time_limit": "0"}'


def execute_action(dcm, action, speed=100, time_limit=0):
    try:
        
        if action == 'go':
            dcm.go(speed)
            log.debug('go')    
        elif action == 'back':
            log.debug('back')
            dcm.go_back(speed)
            if time_limit > 0:
                time.sleep(time_limit)
                dcm.stop()
        elif action == 'right':
            log.debug('right')
            dcm.turn_right(speed)
            if time_limit > 0:
                time.sleep(time_limit)
                dcm.stop()
        elif action == 'left':
            log.debug('left')
            dcm.turn_left(speed)
            if time_limit > 0:
                time.sleep(time_limit)
                dcm.stop()
        elif action == 'stop':
            log.debug('stop')
            dcm.stop()
        elif action == 'exit':
            log.debug('exit: cleaning up used pins')
            dcm.stop()
            dcm.clean_up()
    except Exception as ex:
        log.error("exception in execute_action()")
        log.error(ex, exc_info=True)
        dcm.clean_up()

def init_dc_motors():
    ### ASM init
    cont = AMSpi() 
    try:
        # pin 12 -> D7 is set per default 
        cont.set_74HC595_pins(21, 20, 16)
        # Set PINs for controlling all 4 motors (GPIO numbering)
        #amspi.set_L293D_pins(5, 6, 13, 19)
        # PWM2A -> DC_MOTOR_1
        # PWM2B -> DC_MOTOR_2
        cont.set_L293D_pins(PWM2A=5, PWM2B=6)
        return cont
    except Exception as ex:
        log.error("exception setting 74HC595_pins or L293D_pins")
        cont.clean_up()
        log.error(ex, exc_info=True)
        return None
    


def main():
    broker = redis.StrictRedis()
    sub = broker.pubsub()
    sub.subscribe(DCM_CH)

    try:
        dcm = init_dc_motors()
        while True:
            message = sub.get_message()
            if message and not isinstance(message['data'], int) and message['type'] == 'message':
                log.debug(type(message['data']))
                data = json.loads(message['data'].decode('utf-8'))
                log.debug("DCMC: received data:")
                log.debug(data)
                action = data['action']
                speed = int(data['speed'])
                time_limit = 0
                if 'time_limit' in data:
                    time_limit = float(data['time_limit'])
                if not (dcm is None):            
                    execute_action(dcm, action, speed, time_limit)
                else:
                    log.error("dcm was not initialized not performing action!")
            sleep(0.2)
            
    except Exception as ex:
        log.error("exception in DCMController")
        log.error(ex, exc_info=True)
        dcm.clean_up()

##while True:
##    message = sub.get_message()
##    if message:
##        local_now = datetime.now()
##        print("local now: {}".format(local_now))
##        print("remote time: {}".format(message))
        

if __name__ == "__main__":
    main()     
        
