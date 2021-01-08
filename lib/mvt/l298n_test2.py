from time import sleep
from Dcm import DCM

Dcm = DCM(26,19,13,9,6,5)
try:
	Dcm.go_back()
	sleep(4)
	Dcm.go()
	sleep(4)
	Dcm.turn_left()
	sleep(1.1)
	Dcm.stop()
	sleep(4)
	Dcm.turn_left()
	sleep(1.1)
	Dcm.stop()
	sleep(4)
	Dcm.turn_left()
	sleep(1.1)
	Dcm.stop()
	sleep(4)
	Dcm.turn_left()
	sleep(1.1)
	Dcm.stop()
except KeyboardInterrupt:
    print("interrupt")
except:
    print("exception")
finally:
    Dcm.clean_up()
