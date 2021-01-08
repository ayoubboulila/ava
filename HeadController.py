'''
Created on 12 avr. 2018

@author: AYB
'''

import sys, os
import signal
#import redis
#from utils.RedisClient import RedisClient
#from utils.Broker import BROKER
from utils.RabbitCtl import BROKER
from utils import Logger
import json
from time import sleep
from PyQt4 import QtGui
from lib.ai.Head import AVA
#from lib.ai import config


# json =  '{"action": "play",  "anime": "standby"}'
# json =  '{"action": "play",  "anime": "talk"}'
# json =  '{"action": "play",  "anime": "happy"}'
# json =  '{"action": "play",  "anime": "sad"}'

log = Logger.RCLog('HeadController')
HC_CH = 'HC'
TTSC_CH = 'TTSC'



def execute_action(head, action, anime):
    log.info("exec head action")
    if action == 'play':
        if anime == 'standby':
            print('standby')
            head.set_motion(head.CONFIG.AVA_STANDBY_ANIME)
        elif anime == 'talk':
            print('talk')
            head.set_motion(head.CONFIG.AVA_TALK_ANIME)
        elif anime =='happy':
            print('happy')
        elif anime == 'sad':
            print('sad')
    
    elif action == 'stop':
        print('stop')
def callback(ch, method, properties, message):
    ava.process_events()
    log.debug(message.decode('utf-8'))
    data = json.loads(message.decode('utf-8'))
    log.debug("HC: received data:")
    log.debug(data)
    action = data['action']
    anime = data['anime']
    execute_action(ava, action, anime)



def main():
    try:
        ava = AVA()
        #ava.set_motion(ava.CONFIG.AVA_STANDBY_ANIME)
        execute_action(ava, 'play', 'standby')
        
        print(ava.CONFIG.AVA_STANDBY_ANIME + "----------") 
        #sleep(10)
        #ava.set_motion(ava.CONFIG.AVA_TALK_ANIME)
        #broker = redis.StrictRedis()
        #broker = RedisClient().conn
        #sub = broker.pubsub()
        sub = BROKER()
        sub.subscribe(callback, HC_CH)
        # while True:
            
            # ava.process_events()
            # topic, message = sub.get()
            # if message != None:
                # log.debug(message)
                # data = json.loads(message)
                
                # log.debug("HC: received data:")
                # log.debug(data)
                # action = data['action']
                # anime = data['anime']
                # execute_action(ava, action, anime)
                
            # sleep(0.4)
                
    except Exception as ex:
        log.error("error in HeadController")
        log.error(ex, exc_info=True)
        
        
        
if __name__ == "__main__":
    main()   
