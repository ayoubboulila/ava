from RabbitCtl import BROKER
from time import sleep

br = BROKER()

while True:
	br.publish("TTSC", '{"action": "speak",  "sentence": "hello"}')
	print("published rescheduling....")
	sleep(13)
