import traceback
import time

try:
	import RPi.GPIO as GPIO
except RuntimeError:
	print("Error importing RPi.GPIO! This is probably because you need superuser privileges. "
          "You can achieve this by using 'sudo' to run your script")
except Exception as ex:
    print("exception importing GPIO lib")
    traceback.print_exc()

class RGB:
	__instance__ = None
	_RED_ = None
	_BLUE_ = None
	_GREEN_ = None
	
	def __init__(self, red=25, blue=7, green=8):
		if RGB.__instance__ is None:
			try:
				
				self._RED_ = red
				self._BLUE_ = blue
				self._GREEN_ = green
				RGB.__instance__ = self
				GPIO.setmode(GPIO.BCM)
				GPIO.setwarnings(False)
				GPIO.setup(self._RED_, GPIO.OUT)
				GPIO.setup(self._BLUE_, GPIO.OUT)
				GPIO.setup(self._GREEN_, GPIO.OUT)
				self.led_off()
				self.standby()
				
			except Exception as ex:
				print("exception in init RGB")
				traceback.print_exc()
				
		else:
			raise Exception("You cannot create another RGB class")
	@staticmethod
	def get_instance():
		""" Static method to fetch the current instance.
		"""
		if not RGB.__instance__:
			print("RGB: Initialysing instance")
			RGB()
		return RGB.__instance__
		
	def clean_up(self):
		try:
			print("cleaning up pins")
			GPIO.cleanup()
			self.__instance__ = None
		except Exception as ex:
			print("exception cleaning up pins")
			traceback.print_exc()
	def led_off(self):
		GPIO.output(self._RED_, GPIO.HIGH)
		GPIO.output(self._BLUE_, GPIO.HIGH)
		GPIO.output(self._GREEN_, GPIO.HIGH)
	def set_color(self, color, duration=0):
		self.led_off()
		if color == "r":
			GPIO.output(self._RED_, GPIO.LOW)
		elif color == "b":
			GPIO.output(self._BLUE_, GPIO.LOW)
		elif color == "g":
			GPIO.output(self._GREEN_, GPIO.LOW)
		elif color == "y":
			GPIO.output(self._RED_, GPIO.LOW)
			GPIO.output(self._GREEN_, GPIO.LOW)
		elif color == "c":
			GPIO.output(self._GREEN_, GPIO.LOW)
			GPIO.output(self._BLUE_, GPIO.LOW)
		elif color == "m":
			GPIO.output(self._RED_, GPIO.LOW)
			GPIO.output(self._BLUE_, GPIO.LOW)
		elif color == "w":
			GPIO.output(self._RED_, GPIO.LOW)
			GPIO.output(self._BLUE_, GPIO.LOW)
			GPIO.output(self._GREEN_, GPIO.LOW)
		if duration != 0:
			time.sleep(duration)
			self.led_off()
			self.standby()

	def standby(self):
		self.set_color("g")
		
