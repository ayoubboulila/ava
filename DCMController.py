'''
Created on 14 FEB. 2018

@author: AYB
'''


#import redis
#from utils.RedisClient import RedisClient
#from utils.Broker import BROKER
from utils.RabbitCtl import BROKER
from lib.light.Rgb import RGB
from datetime import datetime
import json
#from pprint import pprint
import ast
from lib.mvt.Dcm import DCM
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
    try:
        
        cont = DCM()
        return cont
    except Exception as ex:
        log.error("exception setting   L298N_pins")
        cont.clean_up()
        log.error(ex, exc_info=True)
        return None
    
# def callback(client, userdata, msg):
    # message = str(msg.payload)
    # log.debug(type(message))
    # data = json.loads(message.decode('utf-8'))
    # log.debug("DCMC: received data:")
    # log.debug(data)
    # action = data['action']
    # speed = int(data['speed'])
    # time_limit = 0
    # if 'time_limit' in data:
        # time_limit = float(data['time_limit'])
    # if not (dcm is None):            
        # execute_action(dcm, action, speed, time_limit)
    # else:
        # log.error("dcm was not initialized not performing action!")

def callback(ch, method, properties, message):
    
    log.debug(message.decode('utf-8'))
    data = json.loads(message.decode('utf-8'))
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



def main():
    #broker = redis.StrictRedis()
    #broker = RedisClient().conn
    #sub = broker.pubsub()
    global dcm
    sub = BROKER()
    
    

    try:
        dcm = init_dc_motors()
        sub.subscribe(callback, DCM_CH)
        # while True:
            # #message = sub.get_message()
            # topic, message = sub.get()
            # if message != None:
                # log.debug((message))
                # data = json.loads(message)
                # log.debug("DCMC: received data:")
                # log.debug(data)
                # action = data['action']
                # speed = int(data['speed'])
                # time_limit = 0
                # if 'time_limit' in data:
                    # time_limit = float(data['time_limit'])
                # if not (dcm is None):            
                    # execute_action(dcm, action, speed, time_limit)
                # else:
                    # log.error("dcm was not initialized not performing action!")
            # sleep(0.2)
            
    except Exception as ex:
        log.error("exception in DCMController")
        log.error(ex, exc_info=True)
        dcm.clean_up()

        

if __name__ == "__main__":
    main()     
        
