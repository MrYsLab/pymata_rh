"""
 Copyright (c) 2020 Alan Yorinks All rights reserved.

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU AFFERO GENERAL PUBLIC LICENSE
 Version 3 as published by the Free Software Foundation; either
 or (at your option) any later version.
 This library is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 General Public License for more details.

 You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
 along with this library; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""

import sys
import time

from pymata_rh import pymata_rh

"""
Setup a pin with an LED for PWM and fade the pin intensity
"""


def fade(my_board, pin):
    """
    This function will set an LED and set it to
    several PWM intensities.

    :param my_board: an PymataExpress instance
    :param pin: pin to be controlled
    """

    brightness = 0
    fade_amount = 5
    # set the pin mode
    print('fade example')
    my_board.set_pin_mode_pwm_output(pin)

    while True:
        my_board.pwm_write(pin, brightness)
        brightness = brightness + fade_amount
        if (brightness <= 0 or brightness >= 255):
            fade_amount = -fade_amount
        time.sleep(.03)


board = pymata_rh.PymataRh()
fade(board, 2)

# here we clean up after the program completes.
board.shutdown()
sys.exit(0)
