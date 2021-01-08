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
from utils import Logger
from lib.sensor.DSensor import DSensor
import threading

# both pub and sub
US_CH = 'US'
MAUC_CH = 'MAUC'

log = Logger.RCLog('USController')

# sub json = '{"action": "mesure", "distance": "0"}'
# sub json = '{"action": "exit", "distance": "0"}'

# pub json = '{"action": "mesure", "distance": "15"}'
# pub json = '{"action": "stopandturn", "distance": "15"}'
# pub json = '{"action": "slowdown", "distance": "25"}'




def execute_action(us, action, broker, metadata=None):
    if action == "mesure":
        d = us.get_distance()
        if metadata is not None:
            data = '{"action": "mesure", "distance": "' + str(d) + '", "metadata": "' + str(metadata) + '"}'
        else:
            data = '{"action": "mesure", "distance": "' + str(d) + '"}'
        broker.publish(MAUC_CH, data)
        
    elif action == "exit":
        log.debug('US exit: cleaning up used pins')
        us.clean_up()

def background_job(us, broker):
    b = BROKER()
    while True:
        
        d = us.get_distance()
        #log.debug("background job distance: {}".format(d))
        if d > us._WARN_DIST_:
            pass
        # elif (d <= us._WARN_DIST_ and d > us._STOP_DIST_):
            # log.debug('US Warning: getting close')
            # log.debug('US distance: {}'.format(d))
            # data = '{"action": "slowdown", "distance": "' + str(d) + '"}'
            # b.publish(MAUC_CH, data)
        elif d <= us._STOP_DIST_:
            log.debug('US Danger: going to crash')
            log.debug('US distance: {}'.format(d))
            data = '{"action": "stopandturn", "distance": "' + str(d) + '"}'
            b.publish(MAUC_CH, data)
            time.sleep(6)
        time.sleep(1)

def callback(ch, method, properties, message):
    log.debug(message)
    data = json.loads(message)
    log.debug("US: received data:")
    log.debug(data)
    action = data['action']
    metadata = None
    if 'metadata' in data:
        metadata = data['metadata']
    if not (us is None):
        execute_action(us, action, broker,metadata)
    else:
        log.error("servos were not initialized not performing action!")

def main():
    try:
        global us
        global broker
        us = DSensor()
        #broker = redis.StrictRedis()
        #broker = RedisClient().conn
        #sub = broker.pubsub()
        broker = BROKER()
        #sub = BROKER()
        thread = threading.Thread(target=background_job, args=(us, broker))
        thread.daemon = True                            
        thread.start()
        broker.subscribe(callback, US_CH)
        # while True:
            # background_job(us, broker)
            # time.sleep(2)
        # while True:
            # topic, message = sub.get()
            # if message != None:
                # log.debug(message)
                # data = json.loads(message)
                # log.debug("US: received data:")
                # log.debug(data)
                # action = data['action']
                # if not (us is None):
                    # execute_action(us, action, broker)
                # else:
                    # log.error("servos were not initialized not performing action!")
            # else:
                # background_job(us, broker)
            # time.sleep(1)
        
    except Exception as ex:
        log.error("exception in USController")
        log.error(ex, exc_info=True)
        us.clean_up()
