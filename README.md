# AMSpi
Python class for controlling Arduino Motor Shield L293D from Raspberry Pi (using RPi.GPIO)

### Requirements
- RPi.GPI, on Raspbian you can install it typing this command:
```
sudo aptitude install python3-rpi.gpio
```  

### Connecting Arduino Motor Shield L293D to Raspberry Pi
You can wire it up as I did. Just look at the colors :-]  
![Wiring](http://janlipovsky.cz/wiring.jpg "Wiring Motor Shield with Raspberry Pi")

### Example
 For complex example please have a look to *example.py* source code.   
```python
from AMSpi import AMSpi

with AMSpi() as amspi:
    # Set PINs for controlling shift register (GPIO numbering)
    amspi.set_74HC595_pins(21, 20, 16)
    # Set PINs for controlling all 4 motors (GPIO numbering)
    amspi.set_L293D_pins(5, 6, 13, 19)
    # Run motors
    amspi.run_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4])
```

### License
This piece of code is licensed under The MIT License.
