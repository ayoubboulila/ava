'''
Created on 12 avr. 2018

@author: AYB
'''

import sys, os
import signal
import redis
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

log = Logger.RCLog('TTSController')
HC_CH = 'HC'
TTSC_CH = 'TTSC'




def main():
    try:
        ava = AVA()
        ava.set_motion(ava.CONFIG.AVA_STANDBY_ANIME)
        print(ava.CONFIG.AVA_STANDBY_ANIME) 
        sleep(10)
        ava.set_motion(ava.CONFIG.AVA_TALK_ANIME)
        broker = redis.StrictRedis()
        sub = broker.pubsub()
        sub.subscribe(HC_CH)
        while True:
            message = sub.get_message()
            if message and not isinstance(message['data'], int) and message['type'] == 'message':
                log.debug(type(message['data']))
                data = json.loads(message['data'].decode('utf-8'))
                log.debug("HC: received data:")
                log.debug(data)
                action = data['action']
                anime = data['anime']
                
            sleep(0.4)
                
    except Exception as ex:
        log.error("error in HeadController")
        log.error(ex, exc_info=True)
        
        
        
if __name__ == "__main__":
    main()   
