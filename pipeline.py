from __future__ import division
import time
import picamera
import numpy as np
from datetime import datetime
# from uploadFile import upload

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
    camera.flash_mode = 'auto'
    camera.resolution = (WIDTH, HEIGHT)

def getDateTime():
    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

def convertStreamToNumpy(stream):
    # Rewind the stream for reading
    stream.seek(0)
    # Calculate the actual image size in the stream (accounting for rounding
    # of the resolution)
    fwidth = (width + 31) // 32 * 32
    fheight = (height + 15) // 16 * 16
    # Load the data in a three-dimensional array and crop it to the requested
    # resolution
    image = np.fromfile(stream, dtype=np.uint8).\
            reshape((fheight, fwidth, 3))[:height, :width, :]
    # If you wish, the following code will convert the image's bytes into
    # floating point values in the range 0 to 1 (a typical format for some
    # sorts of analysis)
    image = image.astype(np.float, copy=False)
    image = image / 255.0
    return image

def main():
    # Capture the image in RGB format
    filename = getDateTime() + '.jpg'
    stream = open(IMAGE_DIRECTORY + filename, 'w+b')
    #while True:
    with picamera.PiCamera() as camera:
        setUpCamera(camera)
        camera.start_preview()
        #while True:
        time.sleep(5)
        camera.capture(stream)
        upload(filename)

main()
