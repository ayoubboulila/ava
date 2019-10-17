# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
 
# initialize the camera and grab a reference to the raw camera capture
print("init cam")
camera = PiCamera()
print("raw capture")
rawCapture = PiRGBArray(camera)
print("sleep to warmup")
# allow the camera to warmup
time.sleep(0.1)
print("grabbing image")
# grab an image from the camera
camera.capture(rawCapture, format="bgr")
print("grabbing image 2")
image = rawCapture.array
print("grabbed image")
# display the image on screen and wait for a keypress
cv2.imshow("Image", image)
cv2.waitKey(0)
