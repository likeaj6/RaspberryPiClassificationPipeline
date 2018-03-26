from __future__ import division

import RPi.GPIO as GPIO
import time
import picamera
import numpy as np
from datetime import datetime
# from uploadFile import upload
from motion_detection import run_average
from constants import *
import server_requests
import feedback_buttons
# from label_image import infer_image, prep_numpy

import boto3

s3 = boto3.client('s3')
bucket_name = 'trashdataset'

def upload(filename):
    s3.upload_file('images/' + filename, bucket_name, 'images/{}'.format(filename))

#If we use this, we'd replace camera.capture with:
# camera.start_recording(
#         # Throw away the video data, but make sure we're using H.264
#         '/dev/null', format='h264',
#         # Record motion data to our custom output object
#         motion_output=FrameMotionDetector(camera)
#         )
# from motion_detection import FrameMotionDetector

WIDTH = 299
HEIGHT = 299
IMAGE_DIRECTORY = './images/'

def setUpCamera(camera):
    camera.flash_mode = 'on'
    camera.resolution = (WIDTH, HEIGHT)

def getDateTime():
    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

def convertStreamToNumpy(stream):
    # Rewind the stream for reading
    stream.seek(0)
    # Calculate the actual image size in the stream (accounting for rounding
    # of the resolution)
    fwidth = (WIDTH + 31) // 32 * 32
    fheight = (HEIGHT + 15) // 16 * 16
    # Load the data in a three-dimensional array and crop it to the requested
    # resolution
    image = np.fromfile(stream, dtype=np.uint8).\
            reshape((fheight, fwidth, 3))[:HEIGHT, :WIDTH, :]
    # If you wish, the following code will convert the image's bytes into
    # floating point values in the range 0 to 1 (a typical format for some
    # sorts of analysis)
    image = image.astype(np.float32, copy=False)
    image = image / 255.0
    print(type(image))
    return image

def setUpGPIO():
    GPIO.setmode(GPIO.BCM)
    # set up the SPI interface pins
    GPIO.setup(SPIMOSI, GPIO.OUT)
    GPIO.setup(SPIMISO, GPIO.IN)
    GPIO.setup(SPICLK, GPIO.OUT)
    GPIO.setup(SPICS, GPIO.OUT)
    GPIO.setup(TRASH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(RECYCLE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(COMPOST_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def main():
    print('Setting up GPIO')
    setUpGPIO()

    IMAGE_DETECTED = False

    # Capture the image in RGB format
    filename = getDateTime() + '.jpg'
    stream = open(IMAGE_DIRECTORY + filename, 'w+b')
    #with tf.Session(graph=graph) as sess:
    while True:
        print('in loop!')
        # with picamera.PiCamera() as camera:
            # setUpCamera(camera)
            # camera.start_preview()
            # livestream mode:
        if run_average() <= 60 and not IMAGE_DETECTED:
            print('Motion Detected!')
            IMAGE_DETECTED = True
            # camera.capture(stream)

            server_requests.motionDetectedRequest()
            print('Sending request!')
            # upload(filename)
            # print('Uploading image')
            time.sleep(2) 
            classification = feedback_buttons.getButtonFeedback()
            print('GETTING USER FEEDBACK')
            print(classification)
            server_requests.buttonFeedbackRequest(classification)

            IMAGE_DETECTED = False

            # npImage = convertStreamToNumpy(stream)
            # preprocessed = prep_numpy(npImage)
            # infer_image(sess, input_operation, output_operation, preprocessed, WIDTH, HEIGHT)

main()
