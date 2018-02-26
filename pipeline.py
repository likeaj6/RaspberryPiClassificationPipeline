from __future__ import division
import time
import picamera
import numpy as np
import datetime

#If we use this, we'd replace camera.capture with:
# camera.start_recording(
#         # Throw away the video data, but make sure we're using H.264
#         '/dev/null', format='h264',
#         # Record motion data to our custom output object
#         motion_output=FrameMotionDetector(camera)
#         )
from motion_detection import FrameMotionDetector

WIDTH = 299
HEIGHT = 299

def setUpCamera(camera):
    camera.flash_mode = 'auto'
    camera.resolution = (WIDTH, HEIGHT)

def getDateTime():
    now = datetime.datetime.now()
    return now.year + '-' + now.month + '-' + now.day + '_' + now.hour + ':' + now.minute + '-' now.second

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
    stream = open(getDateTime() + '.data', 'w+b')
    with picamera.PiCamera() as camera:
        setUpCamera(camera)
        camera.start_preview()
        time.sleep(2)
        camera.capture(stream, 'rgb')
