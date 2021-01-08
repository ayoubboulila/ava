from lib.sensor.Pir import PIR
from lib.light.Led import LED
import traceback
from time import sleep


sensor = PIR()
led = LED()


try:
    while True:
        test = sensor.activate_watcher()
        if test == "detected":
            print("detected")
            led.lights_on()
        elif test == "none":
            print("not detected")
            led.lights_off()
            sleep(0.5)
        sleep(1)
    
        
    
except Exception as ex:
    print("exception in test sensor")
    traceback.print_exc()
    sensor.clean_up()
finally:
    sensor.clean_up()    
