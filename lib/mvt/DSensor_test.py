'''
Created on 9 feb. 2018

@author: AYB
'''

from DSensor import DSensor

import traceback
from time import sleep


sensor = DSensor()


try:
    while True:
        sensor.get_status()
    
        
    
except Exception as ex:
    print("exception in test sensor")
    traceback.print_exc()
    sensor.clean_up()
finally:
    sensor.clean_up()    