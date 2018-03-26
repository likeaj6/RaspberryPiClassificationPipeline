import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

TRASH_PIN = 20
RECYCLING_PIN = 16
COMPOST_PIN = 21


GPIO.setup(TRASH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RECYCLING_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(COMPOST_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    if not(GPIO.input(RECYCLING_PIN)):
        print('RECYCLING')
    if not(GPIO.input(TRASH_PIN)):
        print("TRASH")
    if not(GPIO.input(COMPOST_PIN)):
        print("COMPOST")
GPIO.cleanup()
