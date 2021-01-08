'''
Created on 15 FEB. 2018

@author: AYB
'''

#import redis
#from utils.RedisClient import RedisClient
#from utils.Broker import BROKER
from utils.RabbitCtl import BROKER
from datetime import datetime
import json
import ast
import time
from time import sleep
from utils import Logger
from lib.mvt.Servo import SERVO

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
        log.debug("ServoController execute action")
        if action == "moveX":
            servo.tilt(angle)
        elif action == "moveY":
            servo.pan(angle)
        elif action == "up":
            if angle == -1 and servo.current_pan() in range(-90, 80):
                angle = servo.current_pan() + 10
            else:
                angle = servo.current_pan()
            servo.pan(angle)
        elif action == "down":
            if angle == -1 and servo.current_pan() in range(-80, 90):
                angle = servo.current_pan() - 10
            else:
                angle = servo.current_pan()
            servo.pan(angle)
        elif action == "left":
            if angle == -1 and servo.current_tilt() in range(-90, 80):
                angle = servo.current_tilt() + 10
            else:
                angle = servo.current_tilt()
            servo.tilt(angle)
        elif action == "right":
            if angle == -1 and servo.current_tilt() in range(-80, 90):
                angle = servo.current_tilt() - 10
            else:
                angle = servo.current_tilt()
            servo.tilt(angle)
        elif action == 'exit':
            log.debug('exit: cleaning up used pins')
            servo.clean_up()
        else:
            # wrong angle go neutral
            servo.pan(0)
            servo.tilt(25)
        
    except Exception as ex:
        log.error("exception in SC execute_action()")
        log.error(ex, exc_info=True)
        servo.clean_up()


def callback(ch, method, properties, message):
    log.debug(message.decode('utf-8'))
    data = json.loads(message.decode('utf-8'))
    log.debug("SC: received data:")
    log.debug(data)
    action = data['action']
    angle = int(data['angle'])
    if not (sc is None):
        execute_action(sc, action, angle)
    else:
        log.error("servos were not initialized not performing action!")



def main():
    #broker = redis.StrictRedis()
    #broker = RedisClient().conn
    #sub = broker.pubsub()
    global sc

    try:
        '''
        UP/DOWN servo => pin 13
        LEFT/RIGHT servo => pin 19
        '''
        sub = BROKER()
        
        sc = SERVO()
        sub.subscribe(callback,SC_CH)
        # while True:
            # topic, message = sub.get()
            # if message != None:
                # log.debug(message)
                # data = json.loads(message)
                # log.debug("SC: received data:")
                # log.debug(data)
                # action = data['action']
                # angle = int(data['angle'])
                # if not (sc is None):
                    # execute_action(sc, action, angle)
                # else:
                    # log.error("servos were not initialized not performing action!")
            # sleep(0.2)
            
    except Exception as ex:
        log.error("exception in ServosController")
        log.error(ex, exc_info=True)
        sc.clean_up()
        







if __name__ == "__main__":
    main()     
