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

import time
import sys
from pymata_rh import pymata_rh


"""
Run a calibration cycle of the mpu9250
"""

def mycb(data):
    print(f'mycb: {data}')

board = pymata_rh.PymataRh()
# board.mpu_9250_calibrate()
# sys.exit(0)
board.mpu_9250_initialize(callback=mycb)
# board.mpu_9250_initialize()

board.mpu_9250_read_data()

while True:
    # print(board.mpu_9250_read_saved_data())

    # print(board.mpu_9250_read_data(mode=board.mpu_constants.MPU9250_READ_CONTINUOUS_OFF))
    time.sleep(3)
    # print(board.mpu_9250_read_data())

    # time.sleep(1)
