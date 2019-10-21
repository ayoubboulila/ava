'''
Created on 9 feb. 2018

@author: AYB

distance sensor
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


class DSensor:
    '''
    Main class for controlling the ultrasonic sensor
    
    
    '''
    # Trigger
    _TRG_ = 26
    
    # Echo
    _ECHO_ = 11
    
    # warning distance
    _WARN_DIST_ = 30
    
    # Stop distance
    _STOP_DIST_ = 15
    
    
    def __init__(self, TRG_=26, ECHO_=11, use_board=False):
        """
        Initialize function for servo class

        :param bool use_board: True if GPIO.BOARD numbering will be used
        """
        try:
            
            if use_board:
                GPIO.setmode(GPIO.BOARD)
                print("PIN numbering: BOARD")
            else:
                GPIO.setmode(GPIO.BCM)
                print("PIN numbering: BCM")
            
            self._TRG_ = TRG_
            self._LR_ = ECHO_
            
            GPIO.setup(self._TRG_, GPIO.OUT)
            GPIO.setup(self._ECHO_, GPIO.IN)
            
            
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
    
    def get_distance(self):
        try:
            GPIO.output(self._TRG_, True)
            time.sleep(0.0001)
            GPIO.output(self._TRG_, False)
            while GPIO.input(self._ECHO_) == False:
                start_time = time.time()
            while GPIO.input(self._ECHO_)  == True:
                end_time = time.time()
        
            signal_time = end_time - start_time
        
            # claculate cm distance
            distance = signal_time / 0.000058
        
        
            return distance
        except Exception as ex:
            print("exception in get distance")
            traceback.print_exc()
            return -1
            
            
    
    def get_status(self):
        d = self.get_distance()
        print('distance: '+ str(d))
        if d > self._WARN_DIST_:
            print("every thing is fine")
        elif (d < self._WARN_DIST_ and d > self._STOP_DIST_):
            print("warning distance, slow down")
        else:
            print("danger, stop right now")
             
    
    

