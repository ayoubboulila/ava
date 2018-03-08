'''
Created on 15 FEB. 2018

@author: AYB
'''

import redis
from datetime import datetime
import json
import time
from utils import Logger
from lib.mvt.DSensor import DSensor

# both pub and sub
US_CH = 'US'
MAUC_CH = 'MAUC'

log = Logger.RCLog('USController')

# sub json = '{"action": "mesure", "distance": "0"}'
# sub json = '{"action": "exit", "distance": "0"}'

# pub json = '{"action": "mesure", "distance": "15"}'
# pub json = '{"action": "stopandturn", "distance": "15"}'
# pub json = '{"action": "slowdown", "distance": "25"}'




def execute_action(us, action, broker):
    if action == "mesure":
        d = us.get_distance()
        data = '{"action": "mesure", "distance": "' + d + '"}'
        broker.publish(MAUC_CH, data)
        
    elif action == "exit":
        log.debug('US exit: cleaning up used pins')
        us.clean_up()

def background_job(us, broker):
    d = us.get_distance()
    if d > us._WARN_DIST_:
        pass
    elif (d <= us._WARN_DIST_ and d > us._STOP_DIST_):
        log.debug('US Warning: getting close')
        data = '{"action": "slowdown", "distance": "' + d + '"}'
        broker.publish(MAUC_CH, data)
    elif d <= us._STOP_DIST_:
        log.debug('US Danger: going to crash')
        data = '{"action": "stopandturn", "distance": "' + d + '"}'
        broker.publish(MAUC_CH, data)
    time.sleep(0.5)



def main():
    try:
        us = DSensor()
        broker = redis.StrictRedis()
        sub = broker.pubsub()
        sub.subscribe(US_CH)
        while True:
            message = sub.get_message()
            if message and not isinstance(message['data'], int) and message['type'] == 'message':
                log.debug(type(message['data']))
                data = json.loads(message['data'].decode('utf-8'))
                log.debug("US: received data:")
                log.debug(data)
                action = data['action']
                if not (us is None):
                    execute_action(us, action, broker)
                else:
                    log.error("servos were not initialized not performing action!")
            else:
                background_job(us, broker)
            time.sleep(0.5)
        
    except Exception as ex:
        log.error("exception in USController")
        log.error(ex, exc_info=True)
        us.clean_up()