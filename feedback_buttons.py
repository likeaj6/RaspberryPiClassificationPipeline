import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

TRASH_PIN = 20
RECYCLING_PIN = 16
COMPOST_PIN = 21

def trash_callback(channel):
    if channel == TRASH_PIN:
        print('TRASH')
def recycling_callback(channel):
    if channel == RECYCLING_PIN:
        print('RECYCLING')
def compost_callback(channel):
    if channel == COMPOST_PIN:
        print('COMPOST')

GPIO.setup(TRASH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(RECYCLING_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(COMPOST_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(TRASH_PIN,GPIO.RISING,callback=trash_callback)
GPIO.add_event_detect(RECYCLING_PIN,GPIO.RISING,callback=recycling_callback)
GPIO.add_event_detect(COMPOST_PIN,GPIO.RISING,callback=compost_callback)

message = input("Press enter to quit\n\n") # Run until someone presses enter

GPIO.cleanup()
