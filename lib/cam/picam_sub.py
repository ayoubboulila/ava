#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import cv2
import sys 
sys.path.append('/home/pi/ava')
from utils.RabbitCtl import BROKER

def callback(ch, method, properties, body):
    
    # create int values from sting
    np_arr = np.frombuffer(body, np.uint8)

    # convert data from .jpg encoded image to cv2 format
    image = cv2.imdecode(np_arr, 1)
    cv2.imshow('image', image)

    #print("frame header stamp: {}".format(body.header.stamp))
    # show images and delay for 10ms
    cv2.waitKey(10)
    

if __name__ == '__main__':
    br = BROKER()
    br.subscribe(callback, "stream")
