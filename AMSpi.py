#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------
# Project:  AMSpi class
# Author:   Jan Lipovský, 2016
# E-mail:   janlipovsky@gmail.com
# Licence:  MIT
# Description: Python class for controlling
# Arduino Motor Shield L293D from Raspberry Pi
# ---------------------------------------------
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO! This is probably because you need superuser privileges. You can achieve this by using 'sudo' to run your script")


class AMSpi:
    """
    Main class for controlling Arduino Motor Shield L293D
    via Raspberry Pi GPIO
    """
    # Motor numbering
    DC_Motor_1 = 1
    DC_Motor_2 = 2
    DC_Motor_3 = 3
    DC_Motor_4 = 4

    # Shift register
    __DIR_LATCH = None
    __DIR_CLK = None
    __DIR_SER = None

    # DC Motors states and settings
    __MOTORS = {
        DC_Motor_1: {"pin": None, "direction": [4, 8], "is_running": False, "running_direction": None},
        DC_Motor_2: {"pin": None, "direction": [2, 16], "is_running": False, "running_direction": None},
        DC_Motor_3: {"pin": None, "direction": [32, 128], "is_running": False, "running_direction": None},
        DC_Motor_4: {"pin": None, "direction": [1, 64], "is_running": False, "running_direction": None}
    }

    def __init__(self, use_board=False):
        """
        Initialize function for AMSpi class
        :param boolean use_board: True if GPIO.BOARD numbering will be used
        :return:
        """
        if use_board:
            GPIO.setmode(GPIO.BOARD)
            print("PIN numbering: BOARD")
        else:
            GPIO.setmode(GPIO.BCM)
            print("PIN numbering: BCM")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.__shift_write(0)
            self.stop_dc_motors([self.DC_Motor_1, self.DC_Motor_2, self.DC_Motor_3, self.DC_Motor_4])
            GPIO.cleanup()
        except RuntimeWarning:
            return True

    def __test_shift_pins(self):
        """
        Test if PINs of shift register were set
        :return: boolean True if test passed
        """
        if self.__DIR_LATCH is None:
            return False
        if self.__DIR_CLK is None:
            return False
        if self.__DIR_SER is None:
            return False

        return True

    def __shift_write(self, value):
        """
        Write given value to the shift register
        :param int value: value which you want to write to shift register
        :return:
        """
        if self.__test_shift_pins() is False:
            print("ERROR: PINs for shift register were not set properly.")
            self.__exit__(None, None, None)

        GPIO.output(self.__DIR_LATCH, GPIO.LOW)
        for x in range(0, 8):
            temp = value & 0x80
            GPIO.output(self.__DIR_CLK,  GPIO.LOW)
            if temp == 0x80:
                # data bit HIGH
                GPIO.output(self.__DIR_SER, GPIO.HIGH)
            else:
                # data bit LOW
                GPIO.output(self.__DIR_SER, GPIO.LOW)
            GPIO.output(self.__DIR_CLK, GPIO.HIGH)
            value <<= 0x01  # shift left

        GPIO.output(self.__DIR_LATCH, GPIO.HIGH)

    def set_74HC595_pins(self, DIR_LATCH, DIR_CLK, DIR_SER):
        """
        Set PINs used on Raspberry Pi to connect with 74HC595 module on
        Arduino Motor Shield
        :param int DIR_LATCH: LATCH PIN number
        :param int DIR_CLK: CLK PIN number
        :param int DIR_SER: SER  PIN number
        :return:
        """
        self.__DIR_LATCH = DIR_LATCH
        self.__DIR_CLK = DIR_CLK
        self.__DIR_SER = DIR_SER

        GPIO.setup(self.__DIR_LATCH, GPIO.OUT)
        GPIO.setup(self.__DIR_CLK, GPIO.OUT)
        GPIO.setup(self.__DIR_SER, GPIO.OUT)

    def set_L293D_pins(self, PWM0A=None, PWM0B=None, PWM2A=None, PWM2B=None):
        """
        Set PINs used on Raspberry Pi to connect with 74HC595 module on
        Arduino Motor Shield
        :param int PWM0A: PWM0A PIN number
        :param int PWM0B: PWM0B PIN number
        :param int PWM2A: PWM2A PIN number
        :param int PWM2B: PWM2B PIN number
        :return:
        """
        # self.PWM0A = PWM0A
        self.__MOTORS[self.DC_Motor_4]["pin"] = PWM0B
        # self.PWM0B = PWM0B
        self.__MOTORS[self.DC_Motor_3]["pin"] = PWM0A
        # self.PWM2A = PWM2A
        self.__MOTORS[self.DC_Motor_1]["pin"] = PWM2A
        # self.PWM2B = PWM2B
        self.__MOTORS[self.DC_Motor_2]["pin"] = PWM2B

        if PWM0A is not None:
            GPIO.setup(PWM0A, GPIO.OUT)
        if PWM0B is not None:
            GPIO.setup(PWM0B, GPIO.OUT)
        if PWM2A is not None:
            GPIO.setup(PWM2A, GPIO.OUT)
        if PWM2B is not None:
            GPIO.setup(PWM2B, GPIO.OUT)

    def run_dc_motor(self, dc_motor, clockwise=True):
        """
        Run motor with given direction
        :param int dc_motor:
        :param boolean clockwise: True for clockwise False for counterclockwise
        :return:
        """
        if self.__MOTORS[dc_motor]["pin"] is None:
            print("WARNING: Pin for DC_Motor_{} is not set. Can not run motor.".format(dc_motor))
            return False

        direction_value = self.__MOTORS[dc_motor]["direction"][int(not clockwise)]
        all_motors_direction = direction_value
        for tmp_dc_motor in [self.DC_Motor_1, self.DC_Motor_2, self.DC_Motor_3, self.DC_Motor_4]:
            if tmp_dc_motor == dc_motor:
                continue
            if self.__MOTORS[tmp_dc_motor]["running_direction"] is not None:
                all_motors_direction += self.__MOTORS[tmp_dc_motor]["running_direction"]

        # set motors direction
        self.__shift_write(all_motors_direction)

        # turn the motor on
        GPIO.output(self.__MOTORS[dc_motor]["pin"], GPIO.HIGH)
        self.__MOTORS[dc_motor]["is_running"] = True
        self.__MOTORS[dc_motor]["running_direction"] = direction_value

    def run_dc_motors(self, dc_motors, clockwise=True):
        """
        Run motors with given direction
        :param list dc_motors: list of dc motors
        :param boolean clockwise:
        :return:
        """
        for dc_motor in dc_motors:
            self.run_dc_motor(dc_motor, clockwise)

    def stop_dc_motor(self, dc_motor):
        """
        Stop running motor
        :param dc_motor: 
        :return: 
        """
        if self.__MOTORS[dc_motor]["pin"] is None:
            # print("WARNING: Pin for DC_Motor_{} is not set. Stopping motor could not be done".format(dc_motor))
            return False

        GPIO.output(self.__MOTORS[dc_motor]["pin"], GPIO.LOW)
        self.__MOTORS[dc_motor]["is_running"] = False
        self.__MOTORS[dc_motor]["running_direction"] = None

    def stop_dc_motors(self, dc_motors):
        """
        Stop motors set in list
        :param list dc_motors:
        :return:
        """
        for dc_motor in dc_motors:
            self.stop_dc_motor(dc_motor)
