'''
Created on 5 feb. 2018

@author: AYB
'''

from AMSpi import AMSpi
import time

if __name__ == '__main__':
    # Calling AMSpi() we will use default pin numbering: BCM (use GPIO numbers)
    # if you want to use BOARD numbering do this: "with AMSpi(True) as amspi:"
    with AMSpi() as amspi:
        # Set PINs for controlling shift register (GPIO numbering) add D7 -> pin 12 (GPIO 26)
        # pin 21 [GPIO 29] -> D12
        # pin 20 [GPIO 28] -> D4
        # pin 16 [GPIO 27] -> D8
        # pin 12 [GPIO 26] -> D7
        amspi.set_74HC595_pins(21, 20, 16)
        # Set PINs for controlling all 4 motors (GPIO numbering)
        
        # pin 5 [GPIO 21] -> D11 (PMW motor 1)
        # pin 6 [GPIO 22] -> D3 (PMW motor 2)
        amspi.set_L293D_pins(PWM2A=5, PWM2B=6)
        print("GO: clockwise")
        amspi.run_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2])
        time.sleep(2)

        print("Stop")
        amspi.stop_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2])
        time.sleep(1)

        print("GO: counterclockwise")
        amspi.run_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2], clockwise=False)
        time.sleep(2)

        print("Stop")
        amspi.stop_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2])
        time.sleep(1)

        print("Turn right")
        amspi.run_dc_motors([amspi.DC_Motor_1])
        amspi.run_dc_motors([amspi.DC_Motor_2], clockwise=False)
        time.sleep(1)

        print("Stop")
        amspi.stop_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2])
        time.sleep(1)

        print("Turn left")
        amspi.run_dc_motors([amspi.DC_Motor_1], clockwise=False)
        amspi.run_dc_motors([amspi.DC_Motor_2])
        time.sleep(1)

        print("Stop and Exit")
amspi.stop_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2])