#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, time, os
sys.path.append('/home/pi/ava')
from utils.RabbitCtl import BROKER
from utils import Logger
import types
from datetime import datetime

log = Logger.RCLog('CamStreamer')
try:
    from picamera.array import PiRGBArray
    from picamera import PiCamera
    from threading import Thread
    import numpy as np
    import cv2
except ImportError:
    log.error("Camera not installed or detected")


class PiVideoStream:
    camera = None
    stream = None
    rawCapture = None
    USE_RABBIT = False
    broker = None
    frame_size=(320,320)
    def __init__(self, frame_size=(320,320), resolution=(1280, 720), framerate=32, USE_RABBIT=False, cal=False):
        self.frame_size = frame_size
        # initialize the camera and stream
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.camera.awb_mode = 'auto'
        self.camera.exposure_mode = 'auto'

        # As a safey in case the awb_mode is set to off before these values are set will break the camera driver
        self.camera.awb_gains = (1.0, 1.0) 
        
        #self.camera.rotation = 90
        self.camera.vflip = False
        self.camera.hflip = True
        self.rawCapture = PiRGBArray(self.camera, size=self.frame_size)
        self.stream = self.camera.capture_continuous(self.rawCapture, format="bgr", resize=self.frame_size, use_video_port=True)

        # initialize the frame and the variable used to indicate
        # if the thread should be stopped
        self.frame = None
        self.stopped = False

        # Set the vaiables used to control the White balance
        self.cali = cal
        self.rGain = 1.0
        self.bGain = 1.0
        self.str = 'EMPTY'
		
		# USE_RABBIT
        self.USE_RABBIT = USE_RABBIT
        if self.USE_RABBIT == True:
            self.broker = BROKER()
            
            

    def custom_awb(self):
        # get r,g,b values from the image
        b,g,r = cv2.split(self.frame)
        b = np.mean(b)
        g = np.mean(g)
        r = np.mean(r)

        # Adjust R and B relative to G, but only if they're significantly
        # different (delta +/- 2)
        if( abs(r - g) > 4):
            if (r > g):
                if (self.rGain > 0.5):
                    self.rGain -= 0.01
            else:
                if (self.rGain < 7.98):
                    self.rGain += 0.01
        if (abs(b - g) > 4):
            if (b > g):
                if (self.bGain > 0.5):
                    self.bGain -= 0.01
            else:
                if (self.bGain < 7.98):
                    self.bGain += 0.01
        if g < 95:
            if(self.camera.brightness <= 99):
                self.camera.brightness += 1
        elif g > 105:
            if(self.camera.brightness >= 2):
                self.camera.brightness -= 1

        camera.awb_gains = (self.rGain, self.bGain)
        self.str = 'rGain: %f\tbGain: %f\tBrightness %i R: %i, G: %i, B: %i\n' % (self.rGain, self.bGain, self.camera.brightness, r, g, b)
        log.debug(self.str)


    def debug(self):
        # debug info
       return self.str


    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.update).start()
        log.debug("Waiting  for camera to warm up.")
        time.sleep(2) ## wait for camera to warm up !!
        log.debug("Done! - Camera is read to use")
        return self ## do we need this?


    def update(self):
        # keep looping infinitely until the thread is stopped
        for f in self.stream:

            # grab the frame from the stream and clear the stream in
            # preparation for the next frame
            self.frame = f.array

            # if we init with options act on them
            if(self.USE_RABBIT == True):
                PiVideoStream.pub_image(self)
            # if the thread indicator variable is set, stop the thread
            # and release camera resources
            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                return
            #time.sleep(1/(self.camera.framerate - 2)) ## time to sleep dependant on framrate
            self.rawCapture.truncate(0)


    def read(self):
        # return the frame most recently read
        return self.frame


    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
        log.debug("PiCam_thread stopped!")


    def set_params(self, data):

        if(data.red_gain >= 1.0 and data.red_gain <= 8.0):
            self.rGain = data.red_gain

        if(data.blue_gain >= 1.0 and data.blue_gain <= 8.0):
            self.bGain = data.blue_gain

        self.camera.brightness = data.brightness
        self.camera.iso =  data.iso
        self.camera.awb_mode = data.awb_mode
        self.camera.exposure_mode = data.exposure_mode
        self.camera.awb_gains = (self.rGain, self.bGain)
        self.str = '\n\tawb_mode: %s\n\texposure_mode: %s\n\trGain: %d  bGain: %d\n\tiso: %i\n\tBrightness %i' % (self.camera.awb_mode, self.camera.exposure_mode, self.rGain, self.bGain, self.camera.iso, self.camera.brightness)
        log.debug(self.str)


    def pub_image(self):

        if self.USE_RABBIT == False:
            str0 = "USE_RABBIT not initialised"
            log.debug(str0)

        else:
            # Create image object
            msg = types.SimpleNamespace(header=lambda: {'frame_id': None, 'stamp':None}, data=None)
            
            #msg = Image()
            msg.header.frame_id = 'base_link'
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            msg.header.stamp = current_time

            # Encode image 
            msg.data = np.array(cv2.imencode('.jpg', self.frame)[1]).tostring()

            # Publish new image
            self.broker.publish('stream',msg.data)


if __name__ == '__main__':

    vs = PiVideoStream(resolution=(640, 480), framerate=30, USE_RABBIT=True, cal=False).start() # start picamera using defaults with USE_RABBIT node

    while True:
        time.sleep(1) ## sleep for 1 second
    vs.stop()
