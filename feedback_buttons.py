import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

TRASH_PIN = 20
RECYCLE_PIN = 16
COMPOST_PIN = 21

GPIO.setup(TRASH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(RECYCLE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(COMPOST_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

prev = None

while True:
    if GPIO.input(RECYCLE_PIN) and mode != "RECYCLE":
        print_mode('RECYCLE')
        mode = "RECYCLE"
    elif GPIO.input(TRASH_PIN) and mode != "TRASH":
        print_mode("TRASH")
        mode = "TRASH"
    else:
        mode = None
    #if not(GPIO.input(COMPOST_PIN)):
        #print_mode("COMPOST")
GPIO.cleanup()
