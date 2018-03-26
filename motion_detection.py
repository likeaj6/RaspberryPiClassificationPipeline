#!/usr/bin/env python

# Written by Limor "Ladyada" Fried for Adafruit Industries, (c) 2015
# This code is released into the public domain

import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
DEBUG = 0

# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1

        GPIO.output(cspin, True)

        adcout >>= 1       # first bit is 'null' so drop it
        return adcout

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

# 10k trim pot connected to adc #0
ultra_adc = 0;


def read_ultra_inches():
    return readadc(ultra_adc, SPICLK, SPIMOSI, SPIMISO, SPICS) / 9.8

def measure_distance(tolerance=20):
    last_read
    last_read = 0       # this keeps track of the last potentiometer value
    # volume when the pot has moved more than 5 'counts'
    # assume no change
    changed = False

    # read the analog pin
    read = readadc(ultra_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
    # how much has it changed since the last read?
    pot_adjust = abs(read - last_read)

    if DEBUG:
        print("read:", read)
        print("pot_adjust:", pot_adjust)
        print("last_read", last_read)

        if ( pot_adjust > tolerance ):
            changed = True

            if DEBUG:
                print("changed", changed)

            if ( changed or True):
                adjusted = read / 10.24             # convert 10bit adc0 (0-1024) read into 0-100
                adjusted = round(adjusted)          # round out decimal value
                adjusted = int(adjusted)            # cast as integer

                print(read)

                # save the potentiometer reading for the next loop
                last_read = read

                return read
                # hang out and do nothing for a half second
def run_average():
    distance1=measure_distance()
    time.sleep(0.3)
    distance2=measure_distance()
    time.sleep(0.3)
    distance3=measure_distance()
    distance = distance1 + distance2 + distance3
    distance = distance / 3
    return distance

if __name__ == "__main__":
        while True:
