'''
Created on 15 FEB. 2018

@author: AYB
'''

import redis
from datetime import datetime
import json
import ast
import time
import Logger
from servo import Servo

SC_CH = 'SC'
log = Logger.RCLog('ServosController')

# json = '{"action": "moveX",  "angle": "-1"}'
# json = '{"action": "moveY",  "angle": "-1"}'


def execute_action(servo, action, angle):
    # servo.move_UD
    # servo.move_LR
    if action == "moveX":
        servo.move_UD(angle)
    elif action == "moveY":
        servo.move_LR(angle)
    else:
        # wrong angle go neutral
        servo.move_UD(0)
        servo.move_LR(0)
        pass





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
            
    except Exception as ex:
        log.error("exception in ServosController")
        log.error(ex, exc_info=True)
        







if __name__ == "__main__":
    main()     