'''
Created on 5 feb. 2018

@author: AYB
'''
import traceback
from time import sleep

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
    MAX_UP = 9.5      # 50 degree
    MAX_DOWN = 4.5    # 0 degree
    MAX_LEFT = 4.5    # 0 degree
    MAX_RIGHT = 9.5   # 50 degree
    NEUTRAL_Y = 7.5   # 30 degree
    NEUTRAL_X = 7.5   # 30 degree
    CURRENT_UD = 7.5
    CURRENT_LR = 7.5
    
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
            self.PWM_UD.start(self.CURRENT_UD)
            self.PWM_LR.start(self.CURRENT_LR)
            sleep(1)
            self.PWM_UD.stop()
            self.PWM_LR.stop()
            
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
            print("exception in set_duty_cycle")
            
    def countAngle(self, angle):
        """
        returns duty cycle from given angle
        """
        return float(angle) / 10.0 + 4.5
    
    def move_UD(self, angle):
        self.PWM_UD.start(self.CURRENT_UD)
        pwm = self.countAngle(angle)
        if pwm >= self.MAX_DOWN and pwm <= self.MAX_UP:
            self.set_duty_cycle(self._UD_, pwm)
            self.CURRENT_UD = pwm
        else:
            self.set_duty_cycle(self._UD_, self.NEUTRAL_Y)
            self.CURRENT_UD = self.NEUTRAL_Y
        sleep(1)
        self.PWM_UD.stop()
    
    def move_LR(self, angle):
        self.PWM_LR.start(self.CURRENT_UD)
        pwm = self.countAngle(angle)
        if pwm >= self.MAX_LEFT and pwm <= self.MAX_RIGHT:
            self.set_duty_cycle(self._LR_, pwm)
            self.CURRENT_LR = pwm
        else:
            self.set_duty_cycle(self._LR_, self.NEUTRAL_X)
            self.CURRENT_LR = self.NEUTRAL_X
        sleep(1)
        self.PWM_LR.stop()
    def transit_U(self):
        self.PWM_UD.start(self.CURRENT_UD)
        pwm = self.CURRENT_UD + 0.5
        if pwm >= self.MAX_DOWN and pwm <= self.MAX_UP:
            self.set_duty_cycle(self._UD_, pwm)
            self.CURRENT_UD = pwm
        else:
            self.set_duty_cycle(self._UD_, self.NEUTRAL_Y)
            self.CURRENT_UD = self.NEUTRAL_Y
        sleep(1)
        self.PWM_UD.stop()
    def transit_D(self):
        self.PWM_UD.start(self.CURRENT_UD)
        pwm = self.CURRENT_UD - 0.5
        if pwm >= self.MAX_DOWN and pwm <= self.MAX_UP:
            self.set_duty_cycle(self._UD_, pwm)
            self.CURRENT_UD = pwm
        else:
            self.set_duty_cycle(self._UD_, self.NEUTRAL_Y)
            self.CURRENT_UD = self.NEUTRAL_Y
        sleep(1)
        self.PWM_UD.stop()
    def transit_R(self):
        self.PWM_LR.start(self.CURRENT_LR)
        pwm = self.CURRENT_LR + 0.5
        if pwm >= self.MAX_LEFT and pwm <= self.MAX_RIGHT:
            self.set_duty_cycle(self._LR_, pwm)
            self.CURRENT_LR = pwm
        else:
            self.set_duty_cycle(self._LR_, self.NEUTRAL_X)
            self.CURRENT_LR = self.NEUTRAL_X
        sleep(1)
        self.PWM_LR.stop()
    def transit_L(self):
        self.PWM_LR.start(self.CURRENT_LR)
        pwm = self.CURRENT_LR - 0.5
        if pwm >= self.MAX_LEFT and pwm <= self.MAX_RIGHT:
            self.set_duty_cycle(self._LR_, pwm)
            self.CURRENT_LR = pwm
        else:
            self.set_duty_cycle(self._LR_, self.NEUTRAL_X)
            self.CURRENT_LR = self.NEUTRAL_X
        sleep(1)
        self.PWM_LR.stop()
    
                        
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
    
    
    
    
    
    
    
    

    