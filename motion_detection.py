# import numpy as np
# import picamera
import RPi.GPIO as GPIO

import time

def measure():
  # This function measures a distance
  GPIO.output(TRIGGER, True)
  time.sleep(0.00001)
  GPIO.output(TRIGGER, False)
  start = time.time()

  while GPIO.input(ECHO)==0:
    start = time.time()

  while GPIO.input(ECHO)==1:
    stop = time.time()

  elapsed = stop-start
  distance = (elapsed * 34300)/2

  return distance

GPIO.setmode(GPIO.BCM)

TRIGGER = 29
ECHO = 27

GPIO.setup(TRIGGER,GPIO.OUT)  # Trigger
GPIO.setup(ECHO,GPIO.IN)      # Echo

# Set trigger to False (Low)
GPIO.output(TRIGGER, False)

# Wrap main content in a try block so we can
# catch the user pressing CTRL-C and run the
# GPIO cleanup function. This will also prevent
# the user seeing lots of unnecessary error
# messages.
try:
  while True:
    distance = measure()
    print("Distance: ", distance)
    time.sleep(1)

except KeyboardInterrupt:
  # User pressed CTRL-C
  # Reset GPIO settings
  GPIO.cleanup()

# In case getting Ultrasonic Sensors to work is too much of a hassle, we'll use built in crude analysis based on frames

# class FrameMotionDetector(picamera.array.PiMotionAnalysis):
#     def analyse(self, a):
#         a = np.sqrt(
#             np.square(a['x'].astype(np.float)) +
#             np.square(a['y'].astype(np.float))
#             ).clip(0, 255).astype(np.uint8)
#         # If there're more than 10 vectors with a magnitude greater
#         # than 60, then say we've detected motion
#         if (a > 60).sum() > 10:
#             print('Motion detected!')
#             stream = open('image' + '.data', 'w+b')
#             camera.capture(stream, 'rgb')
