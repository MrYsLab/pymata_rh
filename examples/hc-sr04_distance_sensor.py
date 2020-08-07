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
This program continuously monitors an HC-SR04 Ultrasonic Sensor
It reports changes to the distance sensed.
"""
# indices into callback data
DISTANCE_CM = 2
TRIGGER_PIN = 14
ECHO_PIN = 15


# A callback function to display the distance
def the_callback(data):
    """
    The callback function to display the change in distance
    :param data: [pin_type=12, trigger pin number, distance, timestamp]
    """
    print(f'Distance in cm: {data[DISTANCE_CM]}')


def sonar(my_board, trigger_pin, echo_pin, callback):
    """
    Set the pin mode for a sonar device. Results will appear via the
    callback.

    :param my_board: an pymata express instance
    :param trigger_pin: Arduino pin number
    :param echo_pin: Arduino pin number
    :param callback: The callback function
    """

    # set the pin mode for the trigger and echo pins
    my_board.set_pin_mode_sonar(trigger_pin, echo_pin, callback)
    # wait forever
    while True:
        try:
            time.sleep(.01)
            print(f'data read: {my_board.sonar_read(TRIGGER_PIN)}')
        except KeyboardInterrupt:
            my_board.shutdown()
            sys.exit(0)


board = pymata_rh.PymataRh()
try:
    sonar(board, TRIGGER_PIN, ECHO_PIN, the_callback)
    board.shutdown()
except (KeyboardInterrupt, RuntimeError):
    board.shutdown()
    sys.exit(0)
