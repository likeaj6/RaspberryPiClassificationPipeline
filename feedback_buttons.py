import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)



GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    button1 = GPIO.input(16)
    if (not prev_input and button1):
        print(button1)
    if not(GPIO.input(20)):
        print("20")
    if not(GPIO.input(21)):
        print("21")
    prev_input = button1

GPIO.cleanup()
