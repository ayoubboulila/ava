'''
Created on 11/12/2020

@author: AYB
'''
import traceback
from time import sleep

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO! This is probably because you need superuser privileges. "
          "You can achieve this by using 'sudo' to run your script")
except Exception as ex:
    print("exception importing GPIO lib")
    traceback.print_exc()
class LED:
	_PIN_ = 12
	
	
	
	
	def __init__(self, pin=12, use_board=False):
		try:
			if use_board:
				GPIO.setmode(GPIO.BOARD)
				print("PIN numbering: BOARD")
			else:
				GPIO.setmode(GPIO.BCM)
				print("PIN numbering: BCM")
			
			self._PIN_ = pin
			GPIO.setup(self._PIN_, GPIO.OUT, initial=GPIO.LOW)
		except Exception as ex:
			print("could not setup led pin")
			traceback.print_exc()
	def __enter__(self):
		return self
	def __exit__(self, exc_type, exc_val, exc_tb):
		try:
			print("cleaning GPIO")
			GPIO.cleanup()
		except RuntimeWarning:
			return True
	
	def clean_up(self):
		try:
			GPIO.cleanup()
		except RuntimeWarning:
			return True
	def lights_on(self):
		try:
			GPIO.output(self._PIN_, GPIO.HIGH)
		except Exception as ex:
			traceback.print_exc()
	def lights_off(self):
		try:
			GPIO.output(self._PIN_, GPIO.LOW)
		except Exception as ex:
			traceback.print_exc()		
	def blink(self, speed=1):
		try:
			while True:
				self.lights_on()
				sleep(speed)
				self.lights_off()
				sleep(speed)
		except Exception as ex:
			traceback.print_exc()
