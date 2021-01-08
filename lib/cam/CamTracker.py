import sys
sys.path.append('/home/pi/ava')
from lib.mvt.Servo import SERVO
from utils.RabbitCtl import BROKER
from utils import Logger
import cv2
from time import sleep
log = Logger.RCLog('CamTracker')
class Tracker:
	FRAME_W = 320
	FRAME_H = 320
	USE_RABBIT = False
	srv = None
	broker = None
	SC_CH = 'SC'
	CURRENT_PAN = 0
	CURRENT_TILT = 25
	NEUTRAL_PAN = 0
	NEUTRAL_TILT = 25
	PAN_TILT_THRESHOLD = 10
	PAN_TILT_ERROR = 10
	def __init__(self, frame_w=320, frame_h=320, use_rabbit=False):
		self.FRAME_W = frame_w
		self.FRAME_H = frame_h
		self.USE_RABBIT = use_rabbit
		if not self.USE_RABBIT:
			self.srv = SERVO()
		else:
			self.broker = BROKER()
	
	def track_object(self, xmin, ymin, xmax, ymax, frame):
		xmin = int(xmin * self.FRAME_W)
		xmax = int(xmax * self.FRAME_W)
		ymin = int(ymin * self.FRAME_H)
		ymax = int(ymax * self.FRAME_H)
		obj_x = int(xmin+((xmax - xmin) / 2))
		obj_y = int(ymin+((ymax - ymin) / 2))
		cv2.circle(frame,(obj_x,obj_y), 4, (251,255,0), -1)
		cv2.line(frame, (0, obj_y), (obj_x,obj_y), (251,255,0), 1)
		cv2.line(frame, (obj_x, 0), (obj_x,obj_y), (251,255,0), 1)
		cv2.line(frame, (160, 160), (obj_x,obj_y), (251,255,0), 1)
		# pixels to move
		pix_move_x= obj_x - (self.FRAME_W / 2)
		pix_move_y= obj_y - (self.FRAME_H / 2)
        #convert pixel to angle where angle may vary from -90 to +90
		changex=round((pix_move_x*9)/32)
		changey=round((pix_move_y*9)/32)
		log.debug("changex: {} ---------- changey: {}".format(changex, changey))
		# json = '{"action": "moveX",  "angle": "-1"}'
		if abs(changex) > self.PAN_TILT_THRESHOLD or abs(changey) > self.PAN_TILT_THRESHOLD:
			self.CURRENT_TILT += changex
			self.CURRENT_PAN += changey
			if self.CURRENT_TILT >= 0:
				self.CURRENT_TILT -= self.PAN_TILT_ERROR
			else:
				self.CURRENT_TILT += self.PAN_TILT_ERROR
			
			if self.CURRENT_PAN >= 0:
				self.CURRENT_PAN -= self.PAN_TILT_ERROR
			else:
				self.CURRENT_PAN += self.PAN_TILT_ERROR
			
			if self.CURRENT_TILT > 90:
				self.CURRENT_TILT = 90
			if self.CURRENT_TILT < -90:
				self.CURRENT_TILT = -90
			if self.CURRENT_PAN > 90:
				self.CURRENT_PAN = 90
			if self.CURRENT_PAN < -90:
				self.CURRENT_PAN = -90
			if self.USE_RABBIT and abs(changex) > self.PAN_TILT_THRESHOLD:
				
				json = '{"action": "moveX",  "angle": "'+ str(self.CURRENT_TILT) +'"}'
				self.broker.publish(self.SC_CH, json)
				sleep(0.2)
			if self.USE_RABBIT and abs(changey) > self.PAN_TILT_THRESHOLD:
				json = '{"action": "moveY",  "angle": "'+ str(self.CURRENT_PAN) +'"}'
				self.broker.publish(self.SC_CH, json)
				sleep(0.2)
			if not self.USE_RABBIT and abs(changex) > self.PAN_TILT_THRESHOLD:
				print("not using rabbitmq, tilt: {}".format(self.CURRENT_TILT))
				self.srv.tilt(self.CURRENT_TILT)
				sleep(0.2)
			if not self.USE_RABBIT and abs(changey) > self.PAN_TILT_THRESHOLD:
				print("not using rabbitmq, pan: {}".format(self.CURRENT_PAN))
				self.srv.pan(self.CURRENT_PAN)
				sleep(0.2)
				
			
			
		return frame


	
