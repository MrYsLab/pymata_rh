"""
 Copyright (c) 2020 Alan Yorinks All rights reserved.

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU AFFERO GENERAL PUBLIC LICENSE
 Version 3 as published by the Free Software Foundation; either
 or (at your option) any later version.
 This library is distributed in the hope that it will be useful,f
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 General Public License for more details.

 You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
 along with this library; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

Based on:
https://github.com/Intelligent-Vehicle-Perception/MPU-9250-Sensors-Data-Collect
"""

import time
from pymata_rh.mpu_9250_constants import *


# noinspection PyMethodMayBeStatic
class MPU9250:
    """
    This class encapsulates the mpu_9250 device.

    All sensors and measurement units of the MPU-9250 are described below:

    Sensor              Unit
    ------              ----
    Accelerometer       g (1g = 9.80665 m/s²)
    Gyroscope           degrees per second (°/s)
    Magnetometer        microtesla (μT)
    Temperature         celsius degrees (°C)
    """

    # Address Settings
    address_ak = None
    address_mpu = None

    # Sensor Full Scale
    g_fs = None  # Gyroscope
    a_fs = None  # Accelerometer
    m_fs = None  # Magnetometer
    mode = None  # Magnetometer Mode

    # Sensor Resolution - Scale Factor
    g_res = None  # Gyroscope
    a_res = None  # Accelerometer
    m_res = None  # Magnetometer

    # Factory Magnetometer Calibration and Bias
    mag_calibration = [0, 0, 0]

    # Magnetometer Soft Iron Distortion
    mag_scale = [1, 1, 1]

    # Biases
    g_bias = [0, 0, 0]  # Gyroscope Bias
    a_bias = [0, 0, 0]  # Accelerometer Bias
    m_bias = [0, 0, 0]  # Magnetometer Hard Iron Distortion

    def __init__(self, board, address_ak=AK8963_ADDRESS, address_mpu=MPU9250_ADDRESS_68,
                 g_fs=GFS_2000, a_fs=AFS_16G, m_fs=AK8963_BIT_16, mode=AK8963_MODE_C8HZ,
                 mag_scale=(1, 1, 1), g_bias=(0, 0, 0),
                 a_bias=(0, 0, 0), m_bias=(0, 0, 0)):
        """
        :param: board: instance of pymata_rh

        :param address_ak: AK8963 I2C address (default:AK8963_ADDRESS[0x0C]).

        :param address_mpu:  MPU-9250 I2C address (default:MPU9050_ADDRESS_68[0x68]).

        :param g_fs: Gyroscope full scale select (default:GFS_2000[2000dps]).

        :param a_fs: Accelerometer full scale select (default:AFS_16G[16g]).

        :param m_fs: Magnetometer scale select (default:AK8963_BIT_16[16bit])

        :param mode: Magnetometer mode select (default:AK8963_MODE_C8HZ)

        :param mag_scale: Magnetometer Soft Iron Distortion

        :param g_bias: Gyroscope Bias

        :param a_bias: Accelerometer Bias

        :param m_bias: Magnetometer Hard Iron Distortion
        """
        self.board = board
        self.board.set_pin_mode_i2c()
        self.address_ak = address_ak
        self.address_mpu = address_mpu
        self.g_fs = g_fs
        self.a_fs = a_fs
        self.m_fs = m_fs
        self.mode = mode
        self.mag_scale = mag_scale
        self.a_bias = a_bias
        self.g_bias = g_bias
        self.m_bias = m_bias
        self.configure()

    def configure(self, retry=3):
        """
        Configure MPU-9250

        :param retry: number of retries.

        """
        try:
            self.configure_mpu6500(self.g_fs, self.a_fs)
            self.configure_ak8963(self.m_fs, self.mode)

        except OSError:
            if retry > 1:
                self.configure(retry - 1)
            else:
                raise RuntimeError('Configure retries exceeded maximum.')

    def configure_mpu6500(self, g_fs, a_fs):
        """
        Configure the mpu6500
        :param g_fs: Gyroscope full scale select.

        :param a_fs: Accelerometer full scale select.

        """

        if g_fs == GFS_250:
            self.g_res = GYRO_SCALE_MODIFIER_250DEG
        elif g_fs == GFS_500:
            self.g_res = GYRO_SCALE_MODIFIER_500DEG
        elif g_fs == GFS_1000:
            self.g_res = GYRO_SCALE_MODIFIER_1000DEG
        elif g_fs == GFS_2000:
            self.g_res = GYRO_SCALE_MODIFIER_2000DEG
        else:
            raise RuntimeError('Gyroscope scale modifier not found.')

        if a_fs == AFS_2G:
            self.a_res = ACCEL_SCALE_MODIFIER_2G
        elif a_fs == AFS_4G:
            self.a_res = ACCEL_SCALE_MODIFIER_4G
        elif a_fs == AFS_8G:
            self.a_res = ACCEL_SCALE_MODIFIER_8G
        elif a_fs == AFS_16G:
            self.a_res = ACCEL_SCALE_MODIFIER_16G
        else:
            raise RuntimeError('Accelerometer scale modifier not found.')

        # sleep off
        self.write_mpu(PWR_MGMT_1, 0x00, 0.1)

        # auto select clock source
        self.write_mpu(PWR_MGMT_1, 0x01, 0.1)

        # digital low pass filter config
        self.write_mpu(DLPF_CONFIG, 0x00)

        # sample rate divider
        self.write_mpu(SMPLRT_DIV, 0x00)

        # gyro full scale select
        self.write_mpu(GYRO_CONFIG, g_fs << 3)

        # accelerometer full scale select
        self.write_mpu(ACCEL_CONFIG, a_fs << 3)

        # Accelerometer digital low pass filter configuration
        self.write_mpu(ACCEL_CONFIG_2, 0x00)

        # BYPASS_EN enable
        self.write_mpu(INT_PIN_CFG, 0x02, 0.1)

        # Disable device
        self.write_mpu(USER_CTRL, 0x00, 0.1)

    def configure_ak8963(self, m_fs, mode):
        """
        Configure the AK8963

        :param m_fs: Magnetometer full scale select.

        :param mode: Magnetometer mode select.

        """
        if m_fs == AK8963_BIT_14:
            self.m_res = MAGNOMETER_SCALE_MODIFIER_BIT_14
        elif m_fs == AK8963_BIT_16:
            self.m_res = MAGNOMETER_SCALE_MODIFIER_BIT_16
        else:
            raise Exception('Magnetometer scale modifier not found.')

        # set power down mode
        self.write_ak(AK8963_CNTL1, 0x00, 0.1)

        # set read FuseROM mode
        self.write_ak(AK8963_CNTL1, 0x0F, 0.1)

        # read coefficient data
        data = self.read_ak(AK8963_ASAX, 3, 0.4)

        # set power down mode
        self.write_ak(AK8963_CNTL1, 0x00, 0.1)

        # set scale and continuous mode
        self.write_ak(AK8963_CNTL1, (m_fs << 4 | mode), 0.1)

        self.mag_calibration = [
            (data[0] - 128) / 256.0 + 1.0,
            (data[1] - 128) / 256.0 + 1.0,
            (data[2] - 128) / 256.0 + 1.0
        ]

    def reset(self, retry=3):
        """
        Reset the device

        :param retry: number of retries.
        """
        try:
            self.reset_mpu9250()
        except OSError:
            if retry > 1:
                self.reset(retry - 1)
            else:
                raise RuntimeError('Reset retries exceeded maximum.')

    def reset_mpu9250(self):
        """
        Reset all register values to defaults

        """
        self.write_mpu(PWR_MGMT_1, 0x80, 0.1)

    def read_accelerometer(self):
        """
        Read the accelerometer

        :return: [x, y, z] - acceleration data.
        """

        try:
            data = self.read_mpu(ACCEL_OUT, 6, 0.4)
            return self.convert_accelerometer(data, self.a_bias)

        except OSError:
            return self.get_data_error()

    def convert_accelerometer(self, data, a_bias):
        """
        Convert accelerometer byte block to apply scale factor and biases.

        :param data: accelerometer 6-byte block.

        :param a_bias: biases.

        :return: [x, y, z] - acceleration data.
        """

        x = (self.data_convert(data[1], data[0]) * self.a_res) - a_bias[0]
        y = (self.data_convert(data[3], data[2]) * self.a_res) - a_bias[1]
        z = (self.data_convert(data[5], data[4]) * self.a_res) - a_bias[2]
        return [x, y, z]

    def read_gyroscope(self):
        """
        Read gyroscope

        :return: [x, y, z] - gyroscope data.
        """
        try:
            data = self.read_mpu(GYRO_OUT, 6, 0.4)
            return self.convert_gyroscope(data, self.g_bias)
        except OSError:
            return self.get_data_error()

    def convert_gyroscope(self, data, g_bias):
        """

        :param data: gyroscope 6-byte block.

        :param g_bias: biases.

        :return: [x, y, z] - gyroscope data.
        """
        try:
            x = (self.data_convert(data[1], data[0]) * self.g_res) - g_bias[0]
            y = (self.data_convert(data[3], data[2]) * self.g_res) - g_bias[1]
            z = (self.data_convert(data[5], data[4]) * self.g_res) - g_bias[2]
            return [x, y, z]
        except IndexError:
            return self.get_data_error()

    def read_magnetometer(self):
        """
        Read magnetometer.

        :return: [x, y, z] - magnetometer data.
        """
        try:
            data = self.read_ak(AK8963_MAGNET_OUT, 7, 0.4)
            return self.convert_magnetometer(data)
        except OSError:
            return self.get_data_error()

    def convert_magnetometer(self, data):
        """
        Convert magnetometer byte block to apply scale factor, biases and coefficient.
        
        :param data: magnetometer 7-byte block.

        :return: [x, y, z] - magnetometer data.  

        """

        # check overflow
        if (data[6] & 0x08) != 0x08:
            x = (self.data_convert(data[0], data[1]) * self.m_res * self.mag_calibration[0]) - self.m_bias[0]
            y = (self.data_convert(data[2], data[3]) * self.m_res * self.mag_calibration[1]) - self.m_bias[1]
            z = (self.data_convert(data[4], data[5]) * self.m_res * self.mag_calibration[2]) - self.m_bias[2]
            x *= self.mag_scale[0]
            y *= self.mag_scale[1]
            z *= self.mag_scale[2]
            return [x, y, z]
        else:
            return self.get_data_error()

    def read_temperature(self):
        """
        Read temperature.
        
        :return: temperature(degrees C).
        """

        try:
            data = self.read_mpu(TEMP_OUT, 2, 0.4)
            return self.convert_temperature(data)
        except OSError:
            return 0

    def convert_temperature(self, data):
        """
        Convert temperature byte block to degrees Centigrade (º C).
        
        :param data: temperature 2-byte block.
        
        :return:  temperature in degrees C.
        """
        temp = self.data_convert(data[1], data[0])
        temp = (temp / 333.87 + 21.0)
        return temp

    def get_all_data(self):
        """
        Get array with data from all sensors obtained at same time.
        
        :return: [accelerometer x axis, accelerometer y axis, accelerometer z axis,
                  gyroscope x axis, gyroscope y axis, gyroscope z axis,
                  magnetometer x axis, magnetometer y axis, magnetometer z axis,
                  temperature]
        """

        try:
            data_mpu = self.read_mpu(FIRST_DATA_POSITION, 28, 0.7)
            data_ak = self.read_magnetometer()
            acc_data = self.convert_accelerometer(data_mpu[0:6], self.a_bias)
            temp_data = self.convert_temperature(data_mpu[6:8])
            gyro_data = self.convert_gyroscope(data_mpu[8:14], self.g_bias)
            return acc_data + gyro_data + data_ak + [temp_data]
        except OSError:
            return self.get_data_error() + self.get_data_error() + \
                   self.get_data_error() + self.get_data_error() + \
                   self.get_data_error() + [0, 0]

    # noinspection PyMethodMayBeStatic
    def get_data_error(self):
        """
        When data is not available/error when read, is returned an array with 0.
        
        :return: [0, 0, 0]
        """
        return [0, 0, 0]

    def data_convert(self, data1, data2):
        """
        Convert 2 8 bit values into a single integer.
        :param data1: LSB
        
        :param data2: LSB
        
        :return: MSB+LSB(int 16bit)
        """

        value = data1 | (data2 << 8)
        if value & (1 << 16 - 1):
            value -= (1 << 16)
        return value

    def search_for_mpu_device(self):
        """
        Look for active MPU device
        
        :return: True - device found, False - device not found
        """
        who_am_i = self.read_mpu(WHO_AM_I, 1, 0.4)[0]
        return who_am_i == DEVICE_ID

    def check_mpu_ready(self):
        """
        Check if mpu data is available.
        
        :return: True - data is ready, False - not ready.
        """
        data_ready = self.read_mpu(INT_STATUS, 1, 0.4)[0]
        return data_ready & 0x01

    def check_ak_data_ready(self):
        """
        Check if AK data is ready.
        
        :return: True - data is ready, False - not ready.
        """
        data_ready = self.read_ak(AK8963_ST1, 0.4)[0]
        return data_ready & 0x01

    def calibrate(self, retry=3):
        """
        Calibrate all sensors - this will take about a minute.

        :param retry: number of retries.

        """
        try:
            print("Calibrating ", hex(self.address_mpu), "- AK8963, please wait")
            self.calibrate_ak8963()
            print("Calibrating", hex(self.address_mpu), "- MPU6500, please wait")
            self.calibrate_mpu_6500()
        except OSError:
            if retry > 1:
                self.calibrate(retry - 1)
            else:
                raise RuntimeError('calibrate retries exceeded.')

    def calibrate_mpu_6500(self):
        """
        This function calibrates the MPU6500 and loads the biases to class parameters.

        To calibrate, you must correctly position the MPU so that gravity is all along the z
        axis of the accelerometer.

        This function accumulates gyro and accelerometer data after device initialization.
        It calculates the average of the at-rest readings and then loads the resulting
        offsets into accelerometer and gyro bias registers.

        This function resets the sensor registers so you must call the configure_mpu6500() after
        calling this method.
        """

        # reset device
        self.reset()

        # get stable time source; Auto select clock source to be PLL gyroscope 
        # reference if ready, else use the internal oscillator, bits 2:0 = 001
        self.write_mpu(PWR_MGMT_1, 0x01)
        self.write_mpu(PWR_MGMT_2, 0x00, 0.2)

        # Configure device for bias calculation
        self.write_mpu(INT_ENABLE, 0x00)  # Disable all interrupts
        self.write_mpu(FIFO_EN, 0x00)  # Disable FIFO
        self.write_mpu(PWR_MGMT_1, 0x00)  # Turn on internal clock source
        self.write_mpu(I2C_CTRL, 0x00)  # Disable I2C
        self.write_mpu(USER_CTRL, 0x00)  # Disable FIFO and I2C modes
        self.write_mpu(USER_CTRL, 0x0C, 0.015)  # Reset FIFO and DMP

        # Configure MPU6500 gyro and accelerometer for bias calculation
        self.write_mpu(DLPF_CONFIG, 0x01)  # Set low-pass filter to 188 Hz
        self.write_mpu(SMPLRT_DIV, 0x00)  # Set sample rate to 1 kHz
        self.write_mpu(GYRO_CONFIG, 0x00)  # Set gyro full-scale to 250 degrees per second, maximum sensitivity
        self.write_mpu(ACCEL_CONFIG, 0x00)  # Set accelerometer full-scale to 2G, maximum sensitivity

        # Configure FIFO to capture accelerometer and gyro data for bias calculation
        self.write_mpu(USER_CTRL, 0x40)  # Enable FIFO
        self.write_mpu(FIFO_EN, 0x78, 0.04)  # Enable gyro and accelerometer sensors for 
        # FIFO  (max size 512 bytes in MPU-9150) # 0.4 - accumulate 40 samples in 40 milliseconds = 480 bytes

        # At end of sample accumulation, turn off FIFO sensor read
        self.write_mpu(FIFO_EN, 0x00)  # Disable gyro and accelerometer sensors for FIFO

        # read FIFO sample count
        data = self.read_mpu(FIFO_COUNTH, 2, 0.4)
        fifo_count = self.data_convert(data[1], data[0])
        packet_count = int(fifo_count / 12)  # How many sets of full gyro and accelerometer data for averaging

        index = 0
        accel_bias = [0, 0, 0]
        gyro_bias = [0, 0, 0]

        while index < packet_count:
            print(f"\rIterations to go:    ", end='')
            print(f"\rIterations to go: {packet_count - index}", end='')

            # read data for averaging
            data = self.read_mpu(FIFO_R_W, 12, 0.4)

            # Form signed 16-bit integer for each sample in FIFO
            # Sum individual signed 16-bit biases to get accumulated signed 32-bit biases
            try:
                accel_bias[0] += self.data_convert(data[1], data[0])
                accel_bias[1] += self.data_convert(data[3], data[2])
                accel_bias[2] += self.data_convert(data[5], data[4])
                gyro_bias[0] += self.data_convert(data[7], data[6])
                gyro_bias[1] += self.data_convert(data[9], data[8])
                gyro_bias[2] += self.data_convert(data[11], data[10])
            except IndexError:
                raise RuntimeError('calibrate_mpu_6500: Error - re-power the board and try again')
            index += 1

        # Normalize sums to get average count biases
        accel_bias[0] /= packet_count
        accel_bias[1] /= packet_count
        accel_bias[2] /= packet_count
        gyro_bias[0] /= packet_count
        gyro_bias[1] /= packet_count
        gyro_bias[2] /= packet_count

        # Remove gravity from the z-axis accelerometer bias calculation
        if accel_bias[2] > 0:
            accel_bias[2] -= ACCEL_SCALE_MODIFIER_2G_DIV
        else:
            accel_bias[2] += ACCEL_SCALE_MODIFIER_2G_DIV

        # Output scaled gyro biases for display in the main program
        self.g_bias = [
            (gyro_bias[0] / GYRO_SCALE_MODIFIER_250DEG_DIV),
            (gyro_bias[1] / GYRO_SCALE_MODIFIER_250DEG_DIV),
            (gyro_bias[2] / GYRO_SCALE_MODIFIER_250DEG_DIV)
        ]

        # Output scaled accelerometer biases for manual subtraction in the main program
        self.a_bias = [
            (accel_bias[0] / ACCEL_SCALE_MODIFIER_2G_DIV),
            (accel_bias[1] / ACCEL_SCALE_MODIFIER_2G_DIV),
            (accel_bias[2] / ACCEL_SCALE_MODIFIER_2G_DIV)
        ]

        self.reset()
        print()
        print('mpu_6500 complete.')

    def calibrate_ak8963(self):
        """
        This function calibrates the AK8963 and loads biases to params in this class.
        The configure_ak8963() method must be called after to activate the new values.
        """

        self.configure_ak8963(self.m_fs, self.mode)

        # index = 0
        sample_count = 0
        mag_bias = [0, 0, 0]
        mag_scale = [0, 0, 0]
        mag_max = [-32767, -32767, -32767]
        mag_min = [32767, 32767, 32767]

        # shoot for ~fifteen seconds of mag data
        if self.mode == AK8963_MODE_C8HZ:
            sample_count = 128  # at 8 Hz ODR, new mag data is available every 125 ms

        if self.mode == AK8963_MODE_C100HZ:
            sample_count = 1500  # at 100 Hz ODR, new mag data is available every 10 ms

        index = 0

        while index < sample_count:
            print(f"\rIterations to go:    ", end='')
            print(f"\rIterations to go: {sample_count - index}", end='')
            index += 1
            # data = None

            data = self.read_ak(AK8963_MAGNET_OUT, 7, 0.4)

            # check overflow
            try:
                if (data[6] & 0x08) != 0x08:

                    mag_temp = [
                        self.data_convert(data[0], data[1]),
                        self.data_convert(data[2], data[3]),
                        self.data_convert(data[4], data[5])
                    ]

                else:
                    mag_temp = self.get_data_error()
            except IndexError:
                raise RuntimeError('calibrate_ak8963: Error - re-power the board and try again')

            index_axes = 0

            while index_axes < 3:

                if mag_temp[index_axes] > mag_max[index_axes]:
                    mag_max[index_axes] = mag_temp[index_axes]

                if mag_temp[index_axes] < mag_min[index_axes]:
                    mag_min[index_axes] = mag_temp[index_axes]

                index_axes += 1

            if self.mode == AK8963_MODE_C8HZ:
                time.sleep(0.135)  # at 8 Hz ODR, new mag data is available every 125 ms

            if self.mode == AK8963_MODE_C100HZ:
                time.sleep(0.012)  # at 100 Hz ODR, new mag data is available every 10 ms

        # Get hard iron correction
        mag_bias[0] = (mag_max[0] + mag_min[0]) / 2  # get average x mag bias in counts
        mag_bias[1] = (mag_max[1] + mag_min[1]) / 2  # get average y mag bias in counts
        mag_bias[2] = (mag_max[2] + mag_min[2]) / 2  # get average z mag bias in counts

        # save mag biases in G for main program
        self.m_bias = [
            mag_bias[0] * self.m_res * self.mag_calibration[0],
            mag_bias[1] * self.m_res * self.mag_calibration[1],
            mag_bias[2] * self.m_res * self.mag_calibration[2]
        ]

        # Get soft iron correction estimate
        mag_scale[0] = (mag_max[0] - mag_min[0]) / 2  # get average x axis max chord length in counts
        mag_scale[1] = (mag_max[1] - mag_min[1]) / 2  # get average y axis max chord length in counts
        mag_scale[2] = (mag_max[2] - mag_min[2]) / 2  # get average z axis max chord length in counts

        avg_rad = mag_scale[0] + mag_scale[1] + mag_scale[2]
        avg_rad /= 3.0

        self.mag_scale = [
            avg_rad / mag_scale[0],
            avg_rad / mag_scale[1],
            avg_rad / mag_scale[2]
        ]
        print()
        print('ak8963 complete.')

    def get_all_settings(self):
        """
        Get array with settings from all sensors obtained at same time.

        :return: [address_mpu, address_ak, gyroscope resolution,
                  accelerometer resolution, magnetic resolution,
                  gyroscope bias, accelerometer bias,
                  magnetic calibration, magnetic scale,
                  magnetic bias]
        """

        data = [
                   None if self.address_mpu is None else str(hex(self.address_mpu)),
                   None if self.address_ak is None else str(hex(self.address_ak)),
                   self.g_res, self.a_res, self.m_res,
               ] + list(self.g_bias) + list(self.a_bias) + list(self.mag_calibration) + \
               list(self.mag_scale) + list(self.m_bias)

        return data

    # i2c methods
    def write_ak(self, register, value, sleep=0.0):
        """
        This method writes a value to an ak register.

        :param register:  device register value

        :param value: value to write

        :param sleep: sleep time
        """
        self.board.i2c_write(self.address_ak, [register, value])
        if sleep > 0:
            time.sleep(sleep)

    def read_ak(self, register, quantity, sleep=0.0):
        """
        This method reads the specified number of bytes at the ak register.

        :param register:  device register value

        :param quantity: number of bytes to read

        :param sleep: sleep time

        :return: returns the requested number of bytes read in a list
        """
        self.board.i2c_read(self.address_ak, register, quantity, None)
        if sleep > 0:
            time.sleep(sleep)
        data = self.board.i2c_read_saved_data(self.address_ak)

        return data

    def write_mpu(self, register, value, sleep=0.0):
        """
        This method writes a value to an mpu register.

        :param register: device register value

        :param value: value to write

        :param sleep: sleep time

        """
        self.board.i2c_write(self.address_mpu, [register, value])
        if sleep > 0:
            time.sleep(sleep)

    def read_mpu(self, register, quantity, sleep):
        """
        This method reads the specified number of bytes at the mpu register.

        :param register: device register value

        :param quantity: number of bytes to read

        :param sleep: sleep time

        :return: returns the requested number of bytes read in a list
        """
        self.board.i2c_read(self.address_mpu, register, quantity, None)
        if sleep > 0:
            time.sleep(sleep)
            # time.sleep(1)
        data = self.board.i2c_read_saved_data(self.address_mpu)
        return data
