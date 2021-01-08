'''
Created on 12/12/2020

@author: AYB

PIR motion detection sensor
'''

import traceback
import time

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO! This is probably because you need superuser privileges. "
          "You can achieve this by using 'sudo' to run your script")
except Exception as ex:
    print("exception importing GPIO lib")
    traceback.print_exc()


class PIR:
    '''
    Main class for controlling the PIR sensor
    
    
    '''
    # INPUT PI
    _PIN_ = 16
    
    
    def __init__(self, PIN_=16, use_board=False):
        """
        Initialize function for PIR class

        :param bool use_board: True if GPIO.BOARD numbering will be used
        """
        try:
            
            if use_board:
                GPIO.setmode(GPIO.BOARD)
                print("PIN numbering: BOARD")
            else:
                GPIO.setmode(GPIO.BCM)
                print("PIN numbering: BCM")
            
            self._PIN_ = PIN_
            
            GPIO.setup(self._PIN_, GPIO.IN, GPIO.PUD_DOWN)
            
            
        except Exception as ex:
            print("GPIO could not be set")
            self.clean_up()
            traceback.print_exc()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            
            GPIO.cleanup()
        except RuntimeWarning:
            return True
    
    
    def clean_up(self):
        try:
            print("cleaning up pins")
            GPIO.cleanup()
            
        except Exception as ex:
            print("exception cleaning up pins")
            traceback.print_exc()
    
    def activate_watcher(self):
        pir_in = GPIO.input(self._PIN_)
        time.sleep(0.1)
        if pir_in == 1:
            return "detected"
        elif pir_in == 0:
            return "none"
             
    
    


