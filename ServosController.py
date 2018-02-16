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



def execute_action():
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
                log.debug("DCMC: received data:")
                log.debug(data)
                
            
    except Exception as ex:
        log.error("exception in ServosController")
        log.error(ex, exc_info=True)
        







if __name__ == "__main__":
    main()     