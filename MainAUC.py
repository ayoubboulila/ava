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
import time
from time import sleep
from utils import Logger


SC_CH = 'SC'
DCM_CH = 'DCMC'
US_CH = 'US'
MAUC_CH = 'MAUC'

log = Logger.RCLog('MainAUC')



def execute_action(data, broker):
    if data['action'] == "slowdown":
        command = '{"action": "go",  "speed": "50", "time_limit": "0"}'
        broker.publish(DCM_CH, command)
    elif data['action'] == "stopandturn":
        # first of all stop
        com1 = '{"action": "stop",  "speed": "0", "time_limit": "0"}'
        broker.publish(DCM_CH, com1)
        # go back a little to stop US warnings
        com2 = json = '{"action": "back",  "speed": "100", "time_limit": "0.5"}'
        broker.publish(DCM_CH, com2)
        
        #com3 = '{"action": "neutral",  "angle": "-1"}'
        #broker.publish(SC_CH, com3)
        #time.sleep(0.1)
        
        #turn left to check distance
        com4 = '{"action": "left",  "speed": "100", "time_limit": "0.5"}'
        broker.publish(DCM_CH, com4)
        
        time.sleep(0.2)
        left_dist = 0
        right_dist = 0
        # request left distance mesurement
        com5 = '{"action": "mesure", "distance": "0", "metadata": "left"}'
        broker.publish(US_CH, com5)
        time.sleep(0.2)
        
        
        # while True:
            # sub = BROKER()
            # sub.subscribe(US_CH)
            
            # topic, message = sub.get()
            
            # if message != None:
                # data = json.loads(message)
                # if data['action'] == 'mesure':
                    # left_dist = data['distance']
                    # break
        # turn right to mesure distance
        com6 = '{"action": "right",  "speed": "100", "time_limit": "1"}'
        broker.publish(DCM_CH, com6)
        time.sleep(0.2)
        com7 = '{"action": "mesure", "distance": "0", "metadata": "right"}'
        broker.publish(US_CH, com7)
        time.sleep(0.2)
        # while True:
            # #sub = broker.pubsub()
            # sub = BROKER()
            # sub.subscribe(US_CH)
            # topic, message = sub.get()
            # if message != None:
                # data = json.loads(message)
                # if data['action'] == 'mesure':
                    # right_dist = data['distance']
                    # break
        if left_dist < right_dist:
            com8 = '{"action": "right",  "speed": "100", "time_limit": "0"}'
            time.sleep(0.1)
            broker.publish(DCM_CH, com8)
        else:
            com9 = '{"action": "left",  "speed": "100", "time_limit": "0"}'
            broker.publish(DCM_CH, com9)
            
        com10 = '{"action": "go",  "speed": "100", "time_limit": "0"}' 
        broker.publish(DCM_CH, com10)   
        # look left and mesure
        # look right and mesure
    
    

def callback(ch, method, properties, message):
    log.debug(message.decode('utf-8'))
    data = json.loads(message.decode('utf-8'))
    log.debug("MainAUC: received data:")
    log.debug(data)
    if 'metadata' in data:
        if data['metadata'] == "left":
            left_dist = int(float(data['distance']))
        if data['metadata'] == "right":
            left_dist = int(float(data['distance']))
    else:
        execute_action(data, broker)
    



def main():
    try:
        global left_dist 
        global right_dist 
        global broker
        
        broker = BROKER()
        
        broker.subscribe(callback, MAUC_CH)
        # while True:
            # topic, message = broker.get()
            # if message != None:
                # log.debug(message)
                # data = json.loads(message)
                # log.debug("MainAUC: received data:")
                # log.debug(data)
                # execute_action(data, broker)
            # sleep(0.2)
                
                
    except Exception as ex:
        log.error("exception in MainAUC")
        log.error(ex, exc_info=True)
        



if __name__ == '__main__':
    main()
