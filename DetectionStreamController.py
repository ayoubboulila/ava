'''
Created on 18 oct. 2019

@author: AYB
'''
from __future__ import print_function
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import argparse
import imutils
from os import path
import time
from utils import Logger
import sys
import numpy as np
import cv2
import traceback

from lib.ai.detector.object_detector_detection_api_lite import ObjectDetectorLite
from lib.ai.detector.utils.utils import Models





basepath = path.dirname(__file__)
log = Logger.RCLog('DetectionStreamController')


class DestectionStream:
    _prediction_buffer = {}
    _buffer_counter = 0
    _buffer_frames_limit = 20
    _frame_rate_calc = 1
    _buffer_frame = {}
    
    
    def __init__(self):
        try:
            log.info("init Detection stream")
            log.info('Model loading...')
            predictor = ObjectDetectorLite()

            log.info("[INFO] sampling THREADED frames from webcam...")
            vs = WebcamVideoStream(src=0).start()
            fps = FPS().start()
            freq = cv2.getTickFrequency()
            while True:
                t1 = cv2.getTickCount()
                frame = vs.read()
                # grab the raw NumPy array representing the image, then initialize the timestamp
                # and occupied/unoccupied text
                image = frame

                log.info("FPS: {0:.2f}".format(self._frame_rate_calc))
                cv2.putText(image, "FPS: {0:.2f}".format(self._frame_rate_calc), (20, 20),
                    cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0), 2, cv2.LINE_AA)

                # block that consumes time can skip some frames
                if self._buffer_counter == 0 :
                    
                    result = predictor.detect(image)
                    self._prediction_buffer = result
                else:
                    self._buffer_counter = self._buffer_counter + 1
                    result = self._prediction_buffer
                if self._buffer_counter == self._buffer_frames_limit:
                    self._buffer_counter = 0
                    
                for obj in result:
                    #log.info('coordinates: {} {}. class: "{}". confidence: {:.2f}'.
                    #    format(obj[0], obj[1], obj[3], obj[2]))

                    cv2.rectangle(image, obj[0], obj[1], (0, 0, 255), 2)
                    cv2.putText(image, '{} : {:.2f}'.format(obj[3], obj[2]),
                        (obj[0][0], obj[0][1] - 5),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)


                image = cv2.resize(image, (320, 240))
                self._buffer_frame = image
                # show the frame
                #cv2.namedWindow("Stream", cv2.WND_PROP_FULLSCREEN)
                #scv2.setWindowProperty("Stream",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
                cv2.imshow("Stream", image)
                key = cv2.waitKey(1) & 0xFF

                t2 = cv2.getTickCount()
                time1 = (t2 - t1) / freq
                self._frame_rate_calc = 1 / time1
                fps.update()

                # if the 'q' key was pressed, break from the loop
                if key == ord("q"):
                    break
            fps.stop()
            cv2.destroyAllWindows()
            vs.stop()
            
        except Exception as ex:
            print("exception in init detection")
            traceback.print_exc()

    def get_frame(self):
        return self._buffer_frame

def main():
    # initialize detector
    log.info('Model loading...')
    predictor = ObjectDetectorLite()

    log.info("[INFO] sampling THREADED frames from webcam...")
    vs = WebcamVideoStream(src=0).start()
    fps = FPS().start()
    
    frame_rate_calc = 1
    freq = cv2.getTickFrequency()
    prediction_buffer = {}
    buffer_counter = 0
    buffer_frames_limit = 20
    # capture frames from the camera
    while True:

        t1 = cv2.getTickCount()
        frame = vs.read()
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = frame

        log.info("FPS: {0:.2f}".format(frame_rate_calc))
        cv2.putText(image, "FPS: {0:.2f}".format(frame_rate_calc), (20, 20),
                    cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0), 2, cv2.LINE_AA)

# block that consumes time can skip some frames
        if buffer_counter == 0 :
            
            result = predictor.detect(image)
            prediction_buffer = result
        else:
            buffer_counter = buffer_counter + 1
            result = prediction_buffer
        if buffer_counter == buffer_frames_limit:
            buffer_counter = 0
        
        for obj in result:
            log.info('coordinates: {} {}. class: "{}". confidence: {:.2f}'.
                        format(obj[0], obj[1], obj[3], obj[2]))

            cv2.rectangle(image, obj[0], obj[1], (0, 0, 255), 2)
            cv2.putText(image, '{} : {:.2f}'.format(obj[3], obj[2]),
                        (obj[0][0], obj[0][1] - 5),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)


        image = cv2.resize(image, (320, 240))
        # show the frame
        #cv2.namedWindow("Stream", cv2.WND_PROP_FULLSCREEN)
        #scv2.setWindowProperty("Stream",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        cv2.imshow("Stream", image)
        key = cv2.waitKey(1) & 0xFF

        t2 = cv2.getTickCount()
        time1 = (t2 - t1) / freq
        frame_rate_calc = 1 / time1
        fps.update()

        # if the 'q' key was pressed, break from the loop
        if key == ord("q"):
            break
    fps.stop()
    cv2.destroyAllWindows()
    vs.stop()

    
if __name__ == '__main__':
    main()