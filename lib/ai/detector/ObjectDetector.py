from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import io
import re
import time
import os, sys
sys.path.append('/home/pi/ava')
import numpy as np
import cv2
from PIL import Image
import tensorflow as tf

from lib.cam.picam_streamer import PiVideoStream
from lib.cam.CamTracker import Tracker
from utils.RabbitCtl import BROKER


class Detector:


	CAMERA_WIDTH = 320
	CAMERA_HEIGHT = 320
	threshold = 0.5
	labels_path = None
	model_path = None
	labels = None
	capture_manager = None
	USE_RABBIT = False
	broker = None
	USE_TFT = False
	STREAM_FRAME = None
	
	def __init__(self, threshold = 0.5, CAMERA_WIDTH = 320, CAMERA_HEIGHT = 320, use_rabbit=False, use_tft=False):
		self.CAMERA_WIDTH = CAMERA_WIDTH
		self.CAMERA_HEIGHT = CAMERA_HEIGHT
		self.USE_TFT = use_tft
		self.threshold = threshold
		self.USE_RABBIT = use_rabbit
		self.labels_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "coco_labels.txt")
		self.model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "models", "ssd_mobilenet_v3_small_coco_2020_01_14", "model.tflite")
		self.labels = self.load_labels(self.labels_path)
		if self.USE_RABBIT:
			self.broker = BROKER()
		self.capture_manager = PiVideoStream(resolution=(self.CAMERA_WIDTH, self.CAMERA_HEIGHT), framerate=30, USE_RABBIT=self.USE_RABBIT, cal=False).start()
		self.capture_manager.start()
		# allow the camera to warmup
		time.sleep(0.2)

	def load_labels(self, path):
		"""Loads the labels file. Supports files with or without index numbers."""
		with open(path, 'r', encoding='utf-8') as f:
			lines = f.readlines()
			labels = {}
			for row_number, content in enumerate(lines):
				pair = re.split(r'[:\s]+', content.strip(), maxsplit=1)
				if len(pair) == 2 and pair[0].strip().isdigit():
					labels[int(pair[0])] = pair[1].strip()
				else:
					labels[row_number] = pair[0].strip()
		return labels

	def set_input_tensor(self, interpreter, image):
		"""Sets the input tensor."""
		tensor_index = interpreter.get_input_details()[0]['index']
		input_tensor = interpreter.tensor(tensor_index)()[0]
		input_tensor[:, :] = image
	
	def get_output_tensor(self, interpreter, index):
		"""Returns the output tensor at the given index."""
		output_details = interpreter.get_output_details()[index]
		tensor = np.squeeze(interpreter.get_tensor(output_details['index']))
		return tensor
	
	
	def detect_objects(self, interpreter, image, threshold):
		"""Returns a list of detection results, each a dictionary of object info."""
		self.set_input_tensor(interpreter, image)
		interpreter.invoke()
		
		# Get all output details
		boxes = self.get_output_tensor(interpreter, 0)
		classes = self.get_output_tensor(interpreter, 1)
		scores = self.get_output_tensor(interpreter, 2)
		count = int(self.get_output_tensor(interpreter, 3))
		
		results = []
		for i in range(count):
			if scores[i] >= threshold:
				result = {
				'bounding_box': boxes[i],
				'class_id': classes[i],
				'score': scores[i]
				}
				results.append(result)
		return results
	
	
	def annotate_objects(self, frame, results, labels):
		"""Draws the bounding box and label for each object in the results."""
		for obj in results:
			# Convert the bounding box figures from relative coordinates
			# to absolute coordinates based on the original resolution
			ymin, xmin, ymax, xmax = obj['bounding_box']
			xmin = int(xmin * self.CAMERA_WIDTH)
			xmax = int(xmax * self.CAMERA_WIDTH)
			ymin = int(ymin * self.CAMERA_HEIGHT)
			ymax = int(ymax * self.CAMERA_HEIGHT)
			# draw the box, label, and score on the frame
			cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 1)
			cv2.putText(frame, '{}: {:.2f}'.format(labels[obj['class_id']], obj['score']),(xmin, ymin - 5), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,251), 2)
		return frame


	def start_detection(self, use_rabbit=False, target=["cup", "chair", "person"]):
		interpreter = tf.lite.Interpreter(self.model_path, num_threads=4)
		interpreter.allocate_tensors()
		_, input_height, input_width, _ = interpreter.get_input_details()[0]['shape']
		
		self.capture_manager = PiVideoStream(resolution=(640, 480), frame_size=(self.CAMERA_WIDTH, self.CAMERA_HEIGHT), framerate=30, USE_RABBIT=use_rabbit, cal=False).start()
		self.capture_manager.start()
		# allow the camera to warmup
		time.sleep(0.2)
		
		# Initialize frame rate calculation
		frame_rate_calc = 1
		freq = cv2.getTickFrequency()
		tr = Tracker(use_rabbit=use_rabbit)
		while not self.capture_manager.stopped:
			
			image = self.capture_manager.read()
			#image = cv2.resize(frame, (320, 320))
			start_time = cv2.getTickCount()
			results = self.detect_objects(interpreter, image, self.threshold)
			elapsed_ms = cv2.getTickCount()
			duration = (elapsed_ms-start_time)/freq
			frame_rate_calc= 1/duration
			result_frame = self.annotate_objects(image, results, self.labels)
			#print("prediction fps : {} ".format(frame_rate_calc))
			#result_frame = cv2.resize(result_frame, (640, 480))
			cv2.putText(result_frame,'FPS: {0:.2f}'.format(frame_rate_calc),(10,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,251),1,cv2.LINE_AA)
			# draw center axis
			cv2.line(result_frame, (100, 160), (160,160), (251,255,0), 1)
			cv2.line(result_frame, (160, 100), (160,160), (251,255,0), 1)
			cv2.circle(result_frame,(160,160), 4, (251,255,0), -1)
			obj = None
			for res in results:
				#print("res: {}".format(res))
				if self.labels[res['class_id']] in target:
					
					print("found")
					ymin, xmin, ymax, xmax = res['bounding_box']
					result_frame = tr.track_object(xmin, ymin, xmax, ymax, result_frame)
					
					
					break
			# show the frame
			cv2.imshow("Frame", result_frame)
			key = cv2.waitKey(1) & 0xFF
			# if the `q` key was pressed, break from the loop
			if key == ord("q"):
				break
	def get_stream_frame(self):
		while True:
			
			yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + self.STREAM_FRAME + b'\r\n')  # concat frame one by one and show result
			
	def start_fast_detection(self, use_rabbit=False, target=["cup", "chair", "person"]):
		interpreter = tf.lite.Interpreter(self.model_path, num_threads=2)
		interpreter.allocate_tensors()
		_, input_height, input_width, _ = interpreter.get_input_details()[0]['shape']
		
		
		
		# Initialize frame rate calculation
		frame_rate_calc = 1
		freq = cv2.getTickFrequency()
		tr = Tracker(use_rabbit=use_rabbit)
		frame_buffer = 0
		frame_buffer_threshhold = 1
		while not self.capture_manager.stopped:
			
			image = self.capture_manager.read()
			#image = cv2.resize(frame, (320, 320))
			start_time = cv2.getTickCount()
			if frame_buffer == 0:
				self.results = self.detect_objects(interpreter, image, self.threshold)
				frame_buffer += 1
			elif frame_buffer < frame_buffer_threshhold:
				frame_buffer += 1
			else:
				frame_buffer = 0
			
			result_frame = self.annotate_objects(image, self.results, self.labels)
			# draw center axis
			cv2.line(result_frame, (100, 160), (160,160), (251,255,0), 1)
			cv2.line(result_frame, (160, 100), (160,160), (251,255,0), 1)
			cv2.circle(result_frame,(160,160), 4, (251,255,0), -1)
			obj = None
			if frame_buffer == 1:
				for res in self.results:
					#print("res: {}".format(res))
					if self.labels[res['class_id']] in target:
						
						print("found")
						ymin, xmin, ymax, xmax = res['bounding_box']
						result_frame = tr.track_object(xmin, ymin, xmax, ymax, result_frame)
						
						break
			
			elapsed_ms = cv2.getTickCount()
			duration = (elapsed_ms-start_time)/freq
			frame_rate_calc= 1/duration
			
			cv2.putText(result_frame,'FPS: {0:.2f}'.format(frame_rate_calc),(10,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,251),1,cv2.LINE_AA)
			
			# show the frame
			cv2.imshow("Detection", result_frame)
			# show the frame on the TFT screen
			if self.USE_TFT:
				cv2.namedWindow("TFT_Detection", cv2.WND_PROP_FULLSCREEN)
				cv2.setWindowProperty("TFT_Detection",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
				cv2.imshow("TFT_Detection", result_frame)
			
			# set frame to streamer
			#self.STREAM_FRAME = cv2.resize(result_frame, (480, 320))
			self.STREAM_FRAME = result_frame
			ret, buffer = cv2.imencode('.jpg', self.STREAM_FRAME)
			self.STREAM_FRAME = buffer.tobytes()
			yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + self.STREAM_FRAME + b'\r\n')  # concat frame one by one and show result
			
			key = cv2.waitKey(1) & 0xFF
			# if the `q` key was pressed, break from the loop
			if key == ord("q"):
				break


if __name__ == '__main__':
	try:
		dt = Detector()
		dt.start_fast_detection()
	except KeyboardInterrupt:
		dt.capture_manager.stop()
