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
from pymata_rh import pymata_rh

"""
ina_219
"""

def mycb(data):
    print(f'mycb: {data}')

board = pymata_rh.PymataRh()
board.ina_initialize(callback=mycb)

board.ina_read_bus_voltage()
board.ina_read_bus_current()
board.ina_read_supply_voltage()
board.ina_read_shunt_voltage()
board.ina_read_power()

while True:
    # poll the previous values
    print(board.ina_read_bus_voltage_last())
    print(board.ina_read_bus_current_last())
    print(board.ina_read_supply_voltage_last())
    print(board.ina_read_shunt_voltage_last())
    print(board.ina_read_power_last())
    board.ina_sleep()
    time.sleep(1)
    board.ina_wake()
    board.ina_read_bus_current()

