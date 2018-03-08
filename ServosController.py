'''
Created on 15 FEB. 2018

@author: AYB
'''

import redis
from datetime import datetime
import json
import ast
import time
from time import sleep
from utils import Logger
from lib.mvt.servo import Servo

SC_CH = 'SC'
log = Logger.RCLog('ServosController')

# json = '{"action": "moveX",  "angle": "-1"}'
# json = '{"action": "moveY",  "angle": "-1"}'
# json = '{"action": "up",  "angle": "-1"}'
# json = '{"action": "down",  "angle": "-1"}'
# json = '{"action": "left",  "angle": "-1"}'
# json = '{"action": "right",  "angle": "-1"}'
# json = '{"action": "exit",  "angle": "-1"}'



def execute_action(servo, action, angle):
    try:
        
        # servo.move_UD
        # servo.move_LR
        if action == "moveX":
            servo.move_UD(angle)
        elif action == "moveY":
            servo.move_LR(angle)
        elif action == "up":
            servo.transit_U()
        elif action == "down":
            servo.transit_D()
        elif action == "left":
            servo.transit_L()
        elif action == "right":
            servo.transit_R()
        elif action == 'exit':
            log.debug('exit: cleaning up used pins')
            servo.clean_up()
        else:
            # wrong angle go neutral
            servo.move_UD(servo.NEUTRAL_Y)
            servo.move_LR(servo.NEUTRAL_X)
        
    except Exception as ex:
        log.error("exception in SC execute_action()")
        log.error(ex, exc_info=True)
        servo.clean_up()





def main():
    broker = redis.StrictRedis()
    sub = broker.pubsub()
    sub.subscribe(SC_CH)

    try:
        '''
        UP/DOWN servo => pin 13
        LEFT/RIGHT servo => pin 19
        '''
        sc = Servo()
        while True:
            message = sub.get_message()
            if message and not isinstance(message['data'], int) and message['type'] == 'message':
                log.debug(type(message['data']))
                data = json.loads(message['data'].decode('utf-8'))
                log.debug("SC: received data:")
                log.debug(data)
                action = data['action']
                angle = int(data['angle'])
                if not (sc is None):
                    execute_action(sc, action, angle)
                else:
                    log.error("servos were not initialized not performing action!")
            sleep(0.2)
            
    except Exception as ex:
        log.error("exception in ServosController")
        log.error(ex, exc_info=True)
        sc.clean_up()
        







if __name__ == "__main__":
    main()     