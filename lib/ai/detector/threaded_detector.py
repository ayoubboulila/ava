'''
Created on 18 oct. 2019

@author: AYB
'''
from __future__ import print_function
from imutils.video import WebcamVideoStream
from imutils.video import FPS
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

sys.path.append("/home/pi/ava")
from lib.cam.camera_threaded.CountsPerSec import CountsPerSec
from lib.cam.camera_threaded.VideoGet import VideoGet
from lib.cam.camera_threaded.VideoShow import VideoShow


logging.basicConfig(
    stream=sys.stdout,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt=' %I:%M:%S ',
    level="INFO"
)
logger = logging.getLogger('detector')


basepath = path.dirname(__file__)


def putIterationsPerSec(frame, iterations_per_sec):
    """
    Add iterations per second text to lower-left corner of a frame.
    """

    cv2.putText(frame, "{:.0f} iterations/sec".format(iterations_per_sec),
        (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255))
    return frame
def detect(predictor, image):
    result = predictor.detect(image)

    for obj in result:
        logger.info('coordinates: {} {}. class: "{}". confidence: {:.2f}'.
                        format(obj[0], obj[1], obj[3], obj[2]))

        cv2.rectangle(image, obj[0], obj[1], (0, 255, 0), 2)
        cv2.putText(image, '{}: {:.2f}'.format(obj[3], obj[2]),
                        (obj[0][0], obj[0][1] - 5),
                        cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
    return image

def CameraThreads(predictor, source=0):
    """
    Dedicated thread for grabbing video frames with VideoGet object.
    Dedicated thread for showing video frames with VideoShow object.
    Main thread serves only to pass frames between VideoGet and
    VideoShow objects/threads.
    """

    video_getter = VideoGet(source).start()
    video_shower = VideoShow(video_getter.frame).start()
    cps = CountsPerSec().start()
    fps = FPS().start()
    frame_rate_calc = 1
    freq = cv2.getTickFrequency()

    while True:
        t1 = cv2.getTickCount()
        if video_getter.stopped or video_shower.stopped:
            video_shower.stop()
            video_getter.stop()
            break
        frame = video_getter.frame
        logger.info("FPS: {0:.2f}".format(frame_rate_calc))
        cv2.putText(frame, "FPS: {0:.2f}".format(frame_rate_calc), (20, 20),
                    cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0), 2, cv2.LINE_AA)

        
#        frame = putIterationsPerSec(frame, cps.countsPerSec())
        out_frame = detect(predictor, frame)
        video_shower.frame = out_frame
        t2 = cv2.getTickCount()
        time1 = (t2 - t1) / freq
        frame_rate_calc = 1 / time1
#        logger.info('approx. FPS: {:.2f}'.format(fps.fps()))
        fps.update()
#        cps.increment()
    fps.stop()





if __name__ == "__main__":
        # initialize detector
    logger.info('Model loading...')
#    Models.from_string('tf_lite')
    predictor = ObjectDetectorLite()
#    predictor = ObjectDetectorDetectionAPI(path.join(basepath, "frozen_inference_graph.pb"))

    print("[INFO] sampling THREADED frames from webcam...")
    CameraThreads(predictor)