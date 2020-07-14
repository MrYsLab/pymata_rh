import sys
import time
from pymata4 import pymata4

"""
This example sets up and control an ADXL345 i2c accelerometer.
It will continuously print data the raw xyz data from the device.
"""


# the call back function to print the adxl345 data
def the_callback(data):
    """

    :param data: [pin_type, Device address, device read register, x data pair, y data pair, z data pair]
    :return:
    """
    print(data)


def ina219(my_board):
    # setup ina219
    # device address = 65 (0x41)
    my_board.set_pin_mode_i2c()

    # set up power and control register
    my_board.i2c_write(65, [45, 0])
    time.sleep(.1)
    my_board.i2c_write(65, [45, 8])
    time.sleep(.1)

    # set up the data format register
    my_board.i2c_write(65, [49, 8])
    time.sleep(.1)
    my_board.i2c_write(65, [49, 3])
    time.sleep(1)

    read_count = 20
    while True:
        # read 6 bytes from the data register
        my_board.i2c_read(65, 50, 6, the_callback)
        try:
            time.sleep(.2)
            read_count -= 1
            if not read_count:
                print(f'reading: {my_board.i2c_read_saved_data(65)}')
                read_count = 20
        except KeyboardInterrupt:
            my_board.shutdown()
            sys.exit(0)


board = pymata4.Pymata4()
try:
    adxl345(board)
except KeyboardInterrupt:
    board.shutdown()
    sys.exit(0)
