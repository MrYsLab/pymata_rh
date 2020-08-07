import sys
import time

from pymata_rh import pymata_rh

"""
Setup a pin for digital output 
and toggle the pin forever.
"""

# some globals
DIGITAL_PIN = 13  # the board LED

# Create a pymata_rh instance.
board = pymata_rh.PymataRh()

# Set the DIGITAL_PIN as an output pin
board.set_pin_mode_digital_output(DIGITAL_PIN)

# Blink the LED and provide feedback as
# to the LED state on the console.
while True:
    # When hitting control-c to end the program
    # in this loop, we are likely to get a KeyboardInerrtupt
    # exception. Catch the exception and exit gracefully.
    try:
        print('ON')
        board.digital_write(DIGITAL_PIN, 1)
        time.sleep(1)
        print('OFF')
        board.digital_write(DIGITAL_PIN, 0)
        time.sleep(1)
    except KeyboardInterrupt:
        board.shutdown()
        sys.exit(0)

