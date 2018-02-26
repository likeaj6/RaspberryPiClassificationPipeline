import numpy as np
import picamera

# In case getting Ultrasonic Sensors to work is too much of a hassle, we'll use built in crude analysis based on frames

class FrameMotionDetector(picamera.array.PiMotionAnalysis):
    def analyse(self, a):
        a = np.sqrt(
            np.square(a['x'].astype(np.float)) +
            np.square(a['y'].astype(np.float))
            ).clip(0, 255).astype(np.uint8)
        # If there're more than 10 vectors with a magnitude greater
        # than 60, then say we've detected motion
        if (a > 60).sum() > 10:
            print('Motion detected!')
            stream = open('image' + '.data', 'w+b')
            camera.capture(stream, 'rgb')
