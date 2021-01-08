'''
Created on 2 JAN. 2021

@author: AYB
'''


from Servo import SERVO
import traceback
from time import sleep

s = SERVO()


try:
    print("sarting")
    neutral_angle_ud = s._servo_us_to_degrees(s._UD_NEUTRAL, s._UD_MIN_WIDTH,s._UD_MAX_WIDTH)
    print("neutral angle UD: {}".format(neutral_angle_ud))
    min_angle_ud = s._servo_us_to_degrees(s._UD_MIN_WIDTH, s._UD_MIN_WIDTH,s._UD_MAX_WIDTH)
    print("min angle UD: {}".format(min_angle_ud))
    max_angle_ud = s._servo_us_to_degrees(s._UD_MAX_WIDTH, s._UD_MIN_WIDTH,s._UD_MAX_WIDTH)
    print("max angle UD: {}".format(max_angle_ud))
    neutral_angle_lr = s._servo_us_to_degrees(s._LR_NEUTRAL, s._LR_MIN_WIDTH,s._LR_MAX_WIDTH)
    print("neutral angle LR: {}".format(neutral_angle_lr))
    min_angle_lr = s._servo_us_to_degrees(s._LR_MIN_WIDTH, s._LR_MIN_WIDTH,s._LR_MAX_WIDTH)
    print("min angle LR: {}".format(min_angle_lr))
    max_angle_lr = s._servo_us_to_degrees(s._LR_MAX_WIDTH, s._LR_MIN_WIDTH,s._LR_MAX_WIDTH)
    print("max angle LR: {}".format(max_angle_lr))
    pulse_min_ud = s._servo_degrees_to_us(-90, s._UD_MIN_WIDTH,s._UD_MAX_WIDTH)
    print("pulse for angle -90 UD: {}".format(pulse_min_ud))
    pulse_max_ud = s._servo_degrees_to_us(90, s._UD_MIN_WIDTH,s._UD_MAX_WIDTH)
    print("pulse for angle 90 UD: {}".format(pulse_max_ud))
    s.tilt(5)
    s.pan(65)
    #s.play_motion()
    #s.tilt(9)
    print("current position : ", s.get_current_position("all"))
    
except Exception as ex:
    print("exception in main")
    traceback.print_exc()
    s.clean_up()
finally:
    s.clean_up()
