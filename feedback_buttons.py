import RPi.GPIO as GPIO
from threading import Timer


def debounce(wait):
    """ Decorator that will postpone a functions
        execution until after wait seconds
        have elapsed since the last time it was invoked. """
    def decorator(fn):
        def debounced(*args, **kwargs):
            def call_it():
                fn(*args, **kwargs)
            try:
                debounced.t.cancel()
            except(AttributeError):
                pass
            debounced.t = Timer(wait, call_it)
            debounced.t.start()
        return debounced
return decorator

GPIO.setmode(GPIO.BCM)

TRASH_PIN = 20
RECYCLING_PIN = 16
COMPOST_PIN = 21

@debounce(1)
def print_mode(mode):
    print mode


GPIO.setup(TRASH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(RECYCLING_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(COMPOST_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:
    if GPIO.input(RECYCLING_PIN):
        print_mode('RECYCLING')
    if GPIO.input(TRASH_PIN):
        print_mode("TRASH")
    if not(GPIO.input(COMPOST_PIN)):
        print_mode("COMPOST")
GPIO.cleanup()
