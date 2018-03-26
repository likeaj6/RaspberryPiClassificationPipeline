import RPi.GPIO as GPIO

GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
while True:
    if not(GPIO.input(16)):
        print("16")
    if not(GPIO.input(20)):
        print("20")
    if not(GPIO.input(21)):
        print("21")

GPIO.cleanup()
