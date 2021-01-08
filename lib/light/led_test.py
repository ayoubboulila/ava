from time import sleep
from Led import LED

led = LED()



try:
	led.blink()
except KeyboardInterrupt:
    print("interrupt")
except:
    print("exception")
finally:
    led.clean_up()
