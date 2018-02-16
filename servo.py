'''
Created on 5 feb. 2018

@author: AYB
'''
import traceback

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO! This is probably because you need superuser privileges. "
          "You can achieve this by using 'sudo' to run your script")
except Exception as ex:
    print("exception importing GPIO lib")
    traceback.print_exc()
    
    



class Servo:
    """
    Main class for controlling servos
    
    
    """
    # UP/DOWN servo control pin
    _UD_ = 13
    # RIGHT/LEFT servo control pin
    _LR_ = 19
    
    FREQ = 50
    PWM_UD = None
    PWM_LR = None
    MAX_UP = None
    MAX_DOWN = None
    MAX_LEFT = None
    MAX_RIGHT = None
    
    def __init__(self, UD_=13, LR_=19, use_board=False):
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
            
            self._UD_ = UD_
            self._LR_ = LR_
            
            GPIO.setup(self._UD_, GPIO.OUT)
            GPIO.setup(self._LR_, GPIO.OUT)
            self.PWM_UD = GPIO.PWM(self._UD_, self.FREQ)
            self.PWM_LR = GPIO.PWM(self._LR_, self.FREQ)
            self.PWM_UD.start(0)
            self.PWM_LR.start(0)
            
        except Exception as ex:
            print("GPIO could not be set")
            traceback.print_exc()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.PWM_UD.stop()
            self.PWM_LR.stop()
            GPIO.cleanup()
        except RuntimeWarning:
            return True
    def stop(self):
        try:
            self.PWM_UD.stop()
            self.PWM_LR.stop()
        except Exception as ex:
            print("exception stopping the PWM")
            traceback.print_exc()
    
    def clean_up(self):
        try:
            print("cleaning up pins")
            self.PWM_UD.stop()
            self.PWM_LR.stop()
            GPIO.cleanup()
            
        except Exception as ex:
            print("exception cleaning up pins")
            traceback.print_exc()
    
    def set_duty_cycle(self, pwm, cycle):
        try:
            pwm.ChangeDutyCycle(cycle)
        except Exception as ex:
            print("exception")
            
    def countAngle(self, angle):
        """
        returns duty cycle from given angle
        """
        return float(angle) / 10.0 + 2.5
    
    def move_UD(self, angle):
        self.set_duty_cycle(self._UD_, self.countAngle(angle))
    
    def move_LR(self, angle):
        self.set_duty_cycle(self._LR_, self.countAngle(angle))
    
    def move_up(self, angle):
        #self.PWM_UD
        pass
    def move_down(self, angle):
        #self.PWM_UD
        pass
    def move_right(self, angle):
        #self.PWM_LR
        pass
    def move_left(self, angle):
        #self.PWM_LR
        pass
    
    def move_x(self, direction, angle):
        #self.PWM_LR
        pass
    
    def move_y(self, direction, angle):
        #self.PWM_UD
        pass
    
    
    
    
    
    
    
    

    