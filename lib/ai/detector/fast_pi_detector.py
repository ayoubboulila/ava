from __future__ import print_function
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import argparse
import imutils
from os import path
import time
import logging
import sys
import numpy as np
import cv2

from object_detector_detection_api import ObjectDetectorDetectionAPI
from object_detector_detection_api_lite import ObjectDetectorLite
from utils.utils import Models


logging.basicConfig(
    stream=sys.stdout,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt=' %I:%M:%S ',
    level="INFO"
)
logger = logging.getLogger('detector')


basepath = path.dirname(__file__)

if __name__ == '__main__':


    # initialize detector
    logger.info('Model loading...')
#    Models.from_string('tf_lite')
    predictor = ObjectDetectorLite()
#    predictor = ObjectDetectorDetectionAPI(path.join(basepath, "frozen_inference_graph.pb"))

    print("[INFO] sampling THREADED frames from webcam...")
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

        logger.info("FPS: {0:.2f}".format(frame_rate_calc))
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
            logger.info('coordinates: {} {}. class: "{}". confidence: {:.2f}'.
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
#        logger.info('approx. FPS: {:.2f}'.format(fps.fps()))
        fps.update()

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
    fps.stop()
    cv2.destroyAllWindows()
    vs.stop()
