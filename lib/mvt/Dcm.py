#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
   DCM class - Python class for controlling Motor Driver L298N from Raspberry Pi

.. Licence MIT
.. codeauthor:: Ayoub Boulila <ayoubboulila@gmail.com>
.. contributors: 
"""
import traceback

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO! This is probably because you need superuser privileges. "
          "You can achieve this by using 'sudo' to run your script")
except Exception as ex:
    print("exception importing GPIO lib")
    traceback.print_exc()


class DCM:
    """
    Main class for controlling Motor Driver L298N
    via Raspberry Pi GPIO using RPi.GPIO
    """
    # Motors
    DC_Motors_Right = {"_EN_": None, "_IN1_": None, "_IN2_": None, "_PWM_": None, "_DUTY_CYCLE_": 100}
    
    DC_Motors_Left = {"_EN_": None, "_IN1_": None, "_IN2_": None, "_PWM_": None, "_DUTY_CYCLE_": 100}

   

    # Default GPIO pins 26,19,13,9,6,5

    def __init__(self, Ena=26, In1=19, In2=13, Enb=9, In3=6, In4=5, use_board=False):
        """
        Initialize function for AMSpi class

        :param bool use_board: True if GPIO.BOARD numbering will be used
        """
        try:
            
            if use_board:
                GPIO.setmode(GPIO.BOARD)
                print("PIN numbering: BOARD")
            else:
                GPIO.setmode(GPIO.BCM)
                print("PIN numbering: BCM")
            self.set_L298N_pins(Ena, In1, In2, Enb, In3, In4)
        except Exception as ex:
            print("GPIO could not be set")
            traceback.print_exc()

    def __enter__(self):
        return self

    def __exit__(self):
        try:
            self.stop_dc_motors()
            GPIO.cleanup()
        except RuntimeWarning:
            return True
    
    def clean_up(self):
        try:
            print("cleaning up pins")
            self.stop_dc_motors()
            GPIO.cleanup()
            
        except Exception as ex:
            print("exception cleaning up pins")
            traceback.print_exc()

    

    

    

    def set_L298N_pins(self, Ena=None, In1=None, In2=None, Enb=None, In3=None, In4=None):
        
        if None not in {Ena, In1, In2, Enb, In3, In4}:
            
            self.DC_Motors_Right["_EN_"] = Ena
            self.DC_Motors_Right["_IN1_"] = In1
            self.DC_Motors_Right["_IN2_"] = In2
            self.DC_Motors_Left["_EN_"] = Enb
            self.DC_Motors_Left["_IN1_"] = In3
            self.DC_Motors_Left["_IN2_"] = In4
            
            GPIO.setup(Ena, GPIO.OUT)
            
            GPIO.setup(In1, GPIO.OUT)
            
            GPIO.setup(In2, GPIO.OUT)
            
            GPIO.setup(Enb, GPIO.OUT)
            
            GPIO.setup(In3, GPIO.OUT)
            
            GPIO.setup(In4, GPIO.OUT)
            self.DC_Motors_Right["_PWM_"] = GPIO.PWM(Ena,100)
            self.DC_Motors_Left["_PWM_"] = GPIO.PWM(Enb,100)
            self.DC_Motors_Right["_PWM_"].start(0)
            self.DC_Motors_Left["_PWM_"].start(0)
            
            
        else:
            print("can not setup pins with none value")

    

    

    
    #def get_pwm_duty_cycle(self):
        #"""
        #Returns the current duty cycle lengths for each motor.

        #:return: Length of duty cycle for each motor in dict.
        #:rtype: dict
        #"""

        #return {motor: self._MOTORS[motor][self._PWM_DUTY_CYCLE_] for motor in self._MOTORS.keys()}
    def run_dc_motor(self, dc_motor, clockwise=True, speed=100):
        try:
            print("running dc motor")
            if clockwise == True:
                
                GPIO.output(dc_motor["_IN1_"], GPIO.HIGH)
                GPIO.output(dc_motor["_IN2_"], GPIO.LOW)
                dc_motor["_PWM_"].ChangeDutyCycle(speed)
            else:
                GPIO.output(dc_motor["_IN1_"], GPIO.LOW)
                GPIO.output(dc_motor["_IN2_"], GPIO.HIGH)
                dc_motor["_PWM_"].ChangeDutyCycle(speed)
        except Exception as ex:
            print("exception in run_dc_motor")
            traceback.print_exc()
        

    def run_dc_motors(self, dc_motors, clockwise=True, speed=100):
        
        for dc_motor in dc_motors:
            self.run_dc_motor(dc_motor, clockwise, speed)

    def stop_dc_motor(self, dc_motor):
        try:
            print("stopping motor")
            dc_motor["_PWM_"].ChangeDutyCycle(0)
            return True
        except Exception as ex:
            print("Failed to stop motor")
            traceback.print_exc()
            return False
        
    def stop_dc_motors(self):
        try:
            print("stopping motors")
            self.stop_dc_motor(self.DC_Motors_Right)
            self.stop_dc_motor(self.DC_Motors_Left)
            return True
        except Exception as ex:
            print("Failed to stop motors")
            traceback.print_exc()
            return False
    
    def stop(self):
        self.stop_dc_motors()
        
    
    def go_back(self, speed=100):
        self.stop()
        self.run_dc_motor(self.DC_Motors_Right, False, speed)
        self.run_dc_motor(self.DC_Motors_Left, False, speed)
    
    
    def go(self, speed=100):
        self.stop()
        self.run_dc_motor(self.DC_Motors_Right, True, speed)
        self.run_dc_motor(self.DC_Motors_Left, True, speed)
    
    
    def turn_left(self, speed=100):
        self.stop()
        self.run_dc_motor(self.DC_Motors_Left, True, speed)
        self.run_dc_motor(self.DC_Motors_Right, False, speed)
        
    
    
    def turn_right(self, speed=100):
        self.stop()
        self.run_dc_motor(self.DC_Motors_Right, True, speed)
        self.run_dc_motor(self.DC_Motors_Left, False, speed)
        

        
        
        
