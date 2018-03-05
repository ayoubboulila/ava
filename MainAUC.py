'''
Created on 15 FEB. 2018

@author: AYB
'''


import redis
from datetime import datetime
import json
import time
from time import sleep
import Logger


SC_CH = 'SC'
DCM_CH = 'DCMC'
US_CH = 'US'
MAUC_CH = 'MAUC'

log = Logger.RCLog('MainAUC')



def execute_action(data, broker):
    if data['action'] == "slowdown":
        command = '{"action": "go",  "speed": "40", "time_limit": "0"}'
        broker.publish(DCM_CH, command)
    elif data['action'] == "stopandturn":
        # first of all stop
        com1 = '{"action": "stop",  "speed": "0", "time_limit": "0"}'
        broker.publish(DCM_CH, com1)
        com2 = json = '{"action": "back",  "speed": "50", "time_limit": "0.5"}'
        broker.publish(DCM_CH, com2)
        #com3 = '{"action": "neutral",  "angle": "-1"}'
        #broker.publish(SC_CH, com3)
        #time.sleep(0.1)
        com4 = '{"action": "moveX",  "angle": "0"}'
        broker.publish(SC_CH, com4)
        time.sleep(0.1)
        left_dist = 0
        right_dist = 0
        com5 = '{"action": "mesure", "distance": "0"}'
        broker.publish(US_CH, com5)
        while True:
            sub = broker.pubsub()
            sub.subscribe(US_CH)
            message = sub.get_message()
            if message and not isinstance(message['data'], int) and message['type'] == 'message':
                data = json.loads(message['data'].decode('utf-8'))
                if data['action'] == 'mesure':
                    left_dist = data['distance']
                    break
        com6 = '{"action": "moveX",  "angle": "180"}'
        broker.publish(SC_CH, com6)
        time.sleep(0.1)
        com7 = '{"action": "mesure", "distance": "0"}'
        broker.publish(US_CH, com7)
        while True:
            sub = broker.pubsub()
            sub.subscribe(US_CH)
            message = sub.get_message()
            if message and not isinstance(message['data'], int) and message['type'] == 'message':
                data = json.loads(message['data'].decode('utf-8'))
                if data['action'] == 'mesure':
                    right_dist = data['distance']
                    break
        if left_dist < right_dist:
            com8 = '{"action": "right",  "speed": "50", "time_limit": "0.7"}'
            broker.publish(DCM_CH, com8)
        else:
            com9 = '{"action": "left",  "speed": "50", "time_limit": "0.7"}'
            broker.publish(DCM_CH, com9)
            
        com10 = '{"action": "go",  "speed": "100", "time_limit": "0"}' 
        broker.publish(DCM_CH, com10)   
        # look left and mesure
        # look right and mesure
    
    






















def main():
    try:
        
        broker = redis.StrictRedis()
        sub = broker.pubsub()
        sub.subscribe(MAUC_CH)
        while True:
            message = sub.get_message()
            if message and not isinstance(message['data'], int) and message['type'] == 'message':
                log.debug(type(message['data']))
                data = json.loads(message['data'].decode('utf-8'))
                log.debug("MainAUC: received data:")
                log.debug(data)
                execute_action(data, broker)
            sleep(0.2)
                
                
    except Exception as ex:
        log.error("exception in MainAUC")
        log.error(ex, exc_info=True)
        



if __name__ == '__main__':
    main()