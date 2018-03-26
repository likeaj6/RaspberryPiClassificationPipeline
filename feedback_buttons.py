import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

TRASH_PIN = 20
RECYCLING_PIN = 16
COMPOST_PIN = 21

def button_callback(channel):
    if channel == TRASH_PIN:
        print('TRASH')
    if channel == RECYCLING_PIN:
        print('RECYCLING')
    if channel == COMPOST_PIN:
        print('COMPOST')

GPIO.setup(TRASH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RECYCLING_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(COMPOST_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(TRASH_PIN,GPIO.RISING,callback=button_callback)
GPIO.add_event_detect(RECYCLING_PIN,GPIO.RISING,callback=button_callback)
GPIO.add_event_detect(COMPOST_PIN,GPIO.RISING,callback=button_callback)

GPIO.cleanup()
