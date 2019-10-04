from picamera.array import PiRGBArraypum
from picamera import PiCamera
import time
import cv2

camera = PiCamera
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiGBArray(camera, size=(640, 480))

# Camera warmup
time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True)
  image = frame.array

  cv2.imshow("Frame", image)
  key = cv2.waitKey(1) & 0xFF

  # clear the stream in preparation for the next frame
  rawCapture.truncate(0)