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
#from yolo_darfklow import YOLODarkflowDetector
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
    # initiate the parser
    parser = argparse.ArgumentParser(prog='test_models.py')

    # add arguments
    parser.add_argument("--model_name", "-mn", type=Models.from_string,
                        required=False, choices=list(Models),
                        help="name of detection model: {}".format(list(Models)), default=Models.from_string('tf_lite'))
    parser.add_argument("--graph_path", "-gp", type=str, required=False,
                        default=path.join(basepath, "frozen_inference_graph.pb"),
                        help="path to ssdlight model frozen graph *.pb file")
    parser.add_argument("--cfg_path", "-cfg", type=str, required=False,
                        default=path.join(basepath, "tiny-yolo-voc.cfg"),
                        help="path to yolo *.cfg file")
    parser.add_argument("--weights_path", "-w", type=str, required=False,
                        default=path.join(basepath, "tiny-yolo-voc.weights"),
                        help="path to yolo weights *.weights file")

    # read arguments from the command line
    args = parser.parse_args()

    for k, v in vars(args).items():
        logger.info('Arguments. {}: {}'.format(k, v))

    # initialize detector
    logger.info('Model loading...')
    predictor = ObjectDetectorLite()
#    if args.model_name == Models.ssd_lite:
#        predictor = ObjectDetectorDetectionAPI(args.graph_path)
#    elif args.model_name == Models.tiny_yolo:
#        predictor = YOLODarkflowDetector(args.cfg_path, args.weights_path)
#    elif args.model_name == Models.tf_lite:
#        predictor = ObjectDetectorLite()

    print("[INFO] sampling THREADED frames from webcam...")
    vs = WebcamVideoStream(src=0).start()
    fps = FPS().start()
    
    frame_rate_calc = 1
    freq = cv2.getTickFrequency()

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

        result = predictor.detect(image)

        for obj in result:
            logger.info('coordinates: {} {}. class: "{}". confidence: {:.2f}'.
                        format(obj[0], obj[1], obj[3], obj[2]))

            cv2.rectangle(image, obj[0], obj[1], (0, 255, 0), 2)
            cv2.putText(image, '{}: {:.2f}'.format(obj[3], obj[2]),
                        (obj[0][0], obj[0][1] - 5),
                        cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)

        image = cv2.resize(image, (320, 210))
        # show the frame
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
