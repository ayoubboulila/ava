import traceback
from time import sleep
import pigpio

class SERVO:
	"""
	Main class for controlling servos
	
	
	"""
    # UP/DOWN servo control pin
	_UD_ = 14
    # RIGHT/LEFT servo control pin
	_LR_ = 15
	_UD_MIN_WIDTH = 500
	_UD_MAX_WIDTH = 1600
	_UD_NEUTRAL = 1200
	_LR_MIN_WIDTH = 500
	_LR_MAX_WIDTH = 2300
	_LR_NEUTRAL = 1400
	_PI_ = None
	_servo_min = [_UD_MIN_WIDTH, _LR_MIN_WIDTH]
	_servo_max = [_UD_MAX_WIDTH, _LR_MAX_WIDTH]
	
	
	def __init__(self, UD_=14, LR_=15):
		try:
			self._UD_ = UD_
			self._LR_ = LR_
			self._PI_ = pigpio.pi()
			if not self._PI_.connected:
				print("Could not connect to pigpio Daemon")
				self.__exit__()
            
			self.reset()
            
            
		except Exception as ex:
			print("servo init: GPIO could not be set")
			traceback.print_exc()
    
	def __enter__(self):
		return self
	
	def __exit__(self, exc_type, exc_val, exc_tb):
		try:
			self.clean_up()
		except RuntimeWarning:
			return True
	def clean_up(self):
		try:
			print("cleaning up servo pins")
			self._PI_.set_servo_pulsewidth(self._UD_, 0)
			self._PI_.set_servo_pulsewidth(self._LR_, 0)
			self._PI_.stop()
			
			
		except Exception as ex:
			print("exception cleaning up servo pins")
			traceback.print_exc()
	def reset(self):
		try:
			self._PI_.set_servo_pulsewidth(self._UD_, self._UD_NEUTRAL)
			self._PI_.set_servo_pulsewidth(self._LR_, self._LR_NEUTRAL)
			
			
		except Exception as ex:
			print("servo reset: could not reset")
			traceback.print_exc()
	
	def _check_int_range(self, value, value_min, value_max):
		"""Check the type and bounds check an expected int value."""
		
		if type(value) is not int:
			raise TypeError("Value should be an integer")
		if value < value_min or value > value_max:
			raise ValueError("Value {value} should be between {min} and {max}".format(
                value=value,
                min=value_min,
                max=value_max))
    
	def _check_range(self, value, value_min, value_max):
		"""Check the type and bounds check an expected int value."""
		
		if value < value_min or value > value_max:
			raise ValueError("Value {value} should be between {min} and {max}".format(
                value=value,
                min=value_min,
                max=value_max))

	def _servo_us_to_degrees(self, us, us_min, us_max):
		"""Converts pulse time in microseconds to degrees
		:param us: Pulse time in microseconds
		:param us_min: Minimum possible pulse time in microseconds
		:param us_max: Maximum possible pulse time in microseconds
		"""
		
		self._check_range(us, us_min, us_max)
		servo_range = us_max - us_min
		angle = (float(us - us_min) / float(servo_range)) * 180.0
		return int(round(angle, 0)) - 90

	def _servo_degrees_to_us(self, angle, us_min, us_max):
		"""Converts degrees into a servo pulse time in microseconds
		:param angle: Angle in degrees from -90 to 90
		"""
		
		self._check_range(angle, -90, 90)
		angle += 90
		servo_range = us_max - us_min
		us = (servo_range / 180.0) * angle
		return us_min + int(us)

	def _servo_range(self, servo_index):
		"""Get the min and max range values for a servo"""
		
		return (self._servo_min[servo_index], self._servo_max[servo_index])
	def current_pan(self):
		pan_us =  self._PI_.get_servo_pulsewidth(self._UD_)
		range_us = self._servo_range(0)
		pan_angle = self._servo_us_to_degrees(pan_us, range_us[0], range_us[1])
		return pan_angle
	def current_tilt(self):
		tilt_us =  self._PI_.get_servo_pulsewidth(self._LR_)
		range_us = self._servo_range(1)
		tilt_angle = self._servo_us_to_degrees(tilt_us, range_us[0], range_us[1])
		return tilt_angle
	def get_current_position(self,servo):
		result = {'UD': -1, 'LR': -1}
		if servo == "all":
			result['UD'] = self.current_pan()
			result['LR'] = self.current_tilt()
		elif servo == "pan":
			result['UD'] = self.current_pan()
		elif servo == "tilt":
			result['LR'] = self.current_tilt()
		return result
			
	def tilt(self, angle):
		range_us = self._servo_range(1)
		pulse = self._servo_degrees_to_us(angle, range_us[0], range_us[1])
		print("angle: {}, move_angle_x pulse: {}".format(angle, pulse))
		self._PI_.set_servo_pulsewidth(self._LR_, pulse)
		sleep(0.1)
		
	def pan(self, angle):
		range_us = self._servo_range(0)
		pulse = self._servo_degrees_to_us(angle, range_us[0], range_us[1])
		print("angle: {}, move_angle_x pulse: {}".format(angle, pulse))
		self._PI_.set_servo_pulsewidth(self._UD_, pulse)
		sleep(0.1)
	def play_motion(self):
		for i in range(-90, 90, 10):
			print("moving to angle: {}".format(i))
			self.pan(i)
			self.tilt(i)
			sleep(0.8)
	
	def look_up(self):
		self._PI_.set_servo_pulsewidth(self._UD_, self._UD_MAX_WIDTH)
	def look_down(self):
		self._PI_.set_servo_pulsewidth(self._UD_, self._UD_MIN_WIDTH)
	def look_left(self):
		self._PI_.set_servo_pulsewidth(self._LR_, self._LR_MIN_WIDTH)
	def look_right(self):
		self._PI_.set_servo_pulsewidth(self._LR_, self._LR_MAX_WIDTH)
		
		
