'''
Created on 14 févr. 2018

@author: AYB
'''
import redis
from datetime import datetime


r = redis.StrictRedis()

now = datetime.now()
r.publish('test', now)

