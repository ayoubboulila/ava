#Program asks for user input to determine color to shine.

import time, sys
from time import sleep
from Rgb import RGB

RGB.get_instance().standby()
#print(rgb)
#rgb.standby()
sleep(5)
print("r")
RGB.get_instance().set_color("r", 5)

print("b")
RGB.get_instance().set_color("b", 5)

print("y")
RGB.get_instance().set_color("y", 5)

print("c")
RGB.get_instance().set_color("c", 5)

print("m")
RGB.get_instance().set_color("m", 5)

print("w")
RGB.get_instance().set_color("w", 5)


RGB.get_instance().clean_up()
