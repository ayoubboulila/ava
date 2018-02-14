'''
Created on 14 FEB. 2018

@author: AYB
'''


import redis
from datetime import datetime
import traceback


DCM_CH = 'DCMC'




broker = redis.StrictRedis()

sub = broker.pubsub()

sub.subscribe(DCM_CH)



try:
    
    while True:
        message = sub.get_message()
        if message:
            data = message['data']
            action = data['action']
            clockwise = data['clockwise']
            speed = data['speed']
            if action != 'clean':
                print("going "+ action)
            else:
                print("clean up")
            
except Exception as ex:
    print("exception in DCMController")
    traceback.print_exc()

while True:
    message = sub.get_message()
    if message:
        local_now = datetime.now()
        print("local now: {}".format(local_now))
        print("remote time: {}".format(message))
        
        
        
