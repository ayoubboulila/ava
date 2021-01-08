#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import cv2
from picam_pub import PiVideoStream

def main():
    
    vs = PiVideoStream(framerate=20, USE_RABBIT=False, cal=False).start()

    while True:
        image = vs.read()
        cv2.imshow('image2', image)
        cv2.waitKey(10)
    
    vs.stop()


if __name__ == '__main__':
    main()
