import RPi.GPIO as GPIO
import time
import threading

from constants import *

reset = False

class ResetThread(threading.Thread):
    def __init__(self, time=10):
        super(ResetThread, self).__init__()
        global reset
        self.running = False
        reset = False
        self.time = time

    def start(self):
        self.running = True
        super(ResetThread, self).start()

    def run(self):
        global reset
        time.sleep(self.time)
        if self.running:
            reset = True
        return 

    def stop(self):
        self.running = False

def setUpGPIO():
    GPIO.setmode(GPIO.BCM)

    TRASH_PIN = 20
    RECYCLE_PIN = 16
    COMPOST_PIN = 21

    GPIO.setup(TRASH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(RECYCLE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(COMPOST_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def getButtonFeedback():
    global reset
    reset_thread = ResetThread(10)
    reset_thread.start()

    mode = None

    while True:
        if reset:
            return None
        if GPIO.input(RECYCLE_PIN) and mode != 'Recycle':
            print('RECYCLE')
            mode = "Recycle"
            reset_thread.stop()
            return mode
        elif GPIO.input(TRASH_PIN) and mode != 'Trash':
            print("TRASH")
            mode = "Trash"
            reset_thread.stop()
            return mode
        elif GPIO.input(COMPOST_PIN) and mode != 'Compost':
            print("COMPOST")
            mode = "Compost"
            reset_thread.stop()
            return mode
        time.sleep(0.15)
    #if not(GPIO.input(COMPOST_PIN)):
        #print_mode("COMPOST")
#getButtonFeedback(i)
# GPIO.cleanup()
