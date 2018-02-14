'''
Created on 14 feb. 2018

@author: AYB
'''

import redis
from datetime import datetime

r = redis.StrictRedis()

sub = r.pubsub()

sub.subscribe('test')

while True:
    message = sub.get_message()
    if message:
        local_now = datetime.now()
        print("local now: {}".format(local_now))
        print("remote time: {}".format(message))