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
https://github.com/chrisb2/pi_ina219/
"""
import logging
import time
from math import trunc


# noinspection PyMethodMayBeStatic,PyMethodMayBeStatic,PyMethodMayBeStatic
class INA219:
    """Class containing the INA219 functionality."""

    RANGE_16V = 0  # Range 0-16 volts
    RANGE_32V = 1  # Range 0-32 volts

    GAIN_1_40MV = 0  # Maximum shunt voltage 40mV
    GAIN_2_80MV = 1  # Maximum shunt voltage 80mV
    GAIN_4_160MV = 2  # Maximum shunt voltage 160mV
    GAIN_8_320MV = 3  # Maximum shunt voltage 320mV
    GAIN_AUTO = -1  # Determine gain automatically

    ADC_9BIT = 0  # 9-bit conversion time  84us.
    ADC_10BIT = 1  # 10-bit conversion time 148us.
    ADC_11BIT = 2  # 11-bit conversion time 2766us.
    ADC_12BIT = 3  # 12-bit conversion time 532us.
    ADC_2SAMP = 9  # 2 samples at 12-bit, conversion time 1.06ms.
    ADC_4SAMP = 10  # 4 samples at 12-bit, conversion time 2.13ms.
    ADC_8SAMP = 11  # 8 samples at 12-bit, conversion time 4.26ms.
    ADC_16SAMP = 12  # 16 samples at 12-bit,conversion time 8.51ms
    ADC_32SAMP = 13  # 32 samples at 12-bit, conversion time 17.02ms.
    ADC_64SAMP = 14  # 64 samples at 12-bit, conversion time 34.05ms.
    ADC_128SAMP = 15  # 128 samples at 12-bit, conversion time 68.10ms.

    # identifiers for returned data type
    BUS_VOLTAGE = 0
    BUS_CURRENT = 1
    SUPPLY_VOLTAGE = 2
    SHUNT_VOLTAGE = 3
    POWER = 4

    __ADDRESS = 0x40

    __REG_CONFIG = 0x00
    __REG_SHUNTVOLTAGE = 0x01
    __REG_BUSVOLTAGE = 0x02
    __REG_POWER = 0x03
    __REG_CURRENT = 0x04
    __REG_CALIBRATION = 0x05

    __RST = 15
    __BRNG = 13
    __PG1 = 12
    __PG0 = 11
    __BADC4 = 10
    __BADC3 = 9
    __BADC2 = 8
    __BADC1 = 7
    __SADC4 = 6
    __SADC3 = 5
    __SADC2 = 4
    __SADC1 = 3
    __MODE3 = 2
    __MODE2 = 1
    __MODE1 = 0

    __OVF = 1
    __CNVR = 2

    __BUS_RANGE = [16, 32]
    __GAIN_VOLTS = [0.04, 0.08, 0.16, 0.32]

    __CONT_SH_BUS = 7

    __AMP_ERR_MSG = ('Expected current %.3fA is greater '
                     'than max possible current %.3fA')
    __RNG_ERR_MSG = ('Expected amps %.2fA, out of range, use a lower '
                     'value shunt resistor')
    __VOLT_ERR_MSG = ('Invalid voltage range, must be one of: '
                      'RANGE_16V, RANGE_32V')

    __LOG_FORMAT = '%(asctime)s - %(levelname)s - INA219 %(message)s'
    __LOG_MSG_1 = ('shunt ohms: %.3f, bus max volts: %d, '
                   'shunt volts max: %.2f%s, '
                   'bus ADC: %d, shunt ADC: %d')
    __LOG_MSG_2 = ('calibrate called with: bus max volts: %dV, '
                   'max shunt volts: %.2fV%s')
    __LOG_MSG_3 = ('Current overflow detected - '
                   'attempting to increase gain')

    __SHUNT_MILLIVOLTS_LSB = 0.01  # 10uV
    __BUS_MILLIVOLTS_LSB = 4  # 4mV
    __CALIBRATION_FACTOR = 0.04096
    __MAX_CALIBRATION_VALUE = 0xFFFE  # Max value supported (65534 decimal)
    # In the spec (p17) the current LSB factor for the minimum LSB is
    # documented as 32767, but a larger value (100.1% of 32767) is used
    # to guarantee that current overflow can always be detected.
    __CURRENT_LSB_FACTOR = 32800

    def __init__(self, board, shunt_ohms, max_expected_amps=None,
                 address=__ADDRESS,
                 log_level=logging.ERROR):
        """
        Construct the class.

        Pass in the resistance of the shunt resistor and the maximum expected
        current flowing through it in your system.

        :param board: instance of pymata_rh

        :param shunt_ohms: value of shunt resistor in Ohms (mandatory).

        :param max_expected_amps: the maximum expected current in Amps (optional).

        :param address: the I2C address of the INA219, defaults to 0x40 (optional).

        :param log_level: set to logging.DEBUG to see detailed calibration
                        calculations (optional).
        """
        self.board = board
        self._voltage_range = None
        self.address = address
        if len(logging.getLogger().handlers) == 0:
            # Initialize the root logger only if it hasn't been done yet by a
            # parent module.
            logging.basicConfig(level=log_level, format=self.__LOG_FORMAT)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)

        # self._i2c = I2C.get_i2c_device(address=address, busnum=busnum)
        self._shunt_ohms = shunt_ohms
        self._max_expected_amps = max_expected_amps
        self._min_device_current_lsb = self._calculate_min_current_lsb()
        self._gain = None
        self._auto_gain_enabled = False

    def configure(self, voltage_range=RANGE_16V, gain=GAIN_4_160MV,
                  bus_adc=ADC_12BIT, shunt_adc=ADC_12BIT):
        """
        Configure and calibrate how the INA219 will take measurements.

        :param voltage_range: The full scale voltage range, this is either 16V
            or 32V represented by one of the following constants;
            RANGE_16V, RANGE_32V (default).
        :param gain: The gain which controls the maximum range of the shunt
            voltage represented by one of the following constants;
            GAIN_1_40MV, GAIN_2_80MV, GAIN_4_160MV,
            GAIN_8_320MV, GAIN_AUTO (default).
        :param bus_adc: The bus ADC resolution (9, 10, 11, or 12-bit) or
            set the number of samples used when averaging results
            represent by one of the following constants; ADC_9BIT,
            ADC_10BIT, ADC_11BIT, ADC_12BIT (default),
            ADC_2SAMP, ADC_4SAMP, ADC_8SAMP, ADC_16SAMP,
            ADC_32SAMP, ADC_64SAMP, ADC_128SAMP
        :param shunt_adc: The shunt ADC resolution (9, 10, 11, or 12-bit) or
            set the number of samples used when averaging results
            represent by one of the following constants; ADC_9BIT,
            ADC_10BIT, ADC_11BIT, ADC_12BIT (default),
            ADC_2SAMP, ADC_4SAMP, ADC_8SAMP, ADC_16SAMP,
            ADC_32SAMP, ADC_64SAMP, ADC_128SAMP
        """
        self.__validate_voltage_range(voltage_range)
        self._voltage_range = voltage_range

        if self._max_expected_amps is not None:
            if gain == self.GAIN_AUTO:
                self._auto_gain_enabled = True
                self._gain = self._determine_gain(self._max_expected_amps)
            else:
                self._gain = gain
        else:
            if gain != self.GAIN_AUTO:
                self._gain = gain
            else:
                self._auto_gain_enabled = True
                self._gain = self.GAIN_1_40MV

        self.logger.info('gain set to %.2fV' % self.__GAIN_VOLTS[self._gain])

        self.logger.debug(
            self.__LOG_MSG_1 %
            (self._shunt_ohms, self.__BUS_RANGE[voltage_range],
             self.__GAIN_VOLTS[self._gain],
             self.__max_expected_amps_to_string(self._max_expected_amps),
             bus_adc, shunt_adc))

        self._calibrate(
            self.__BUS_RANGE[voltage_range], self.__GAIN_VOLTS[self._gain],
            self._max_expected_amps)
        self._configure(voltage_range, self._gain, bus_adc, shunt_adc)

    def voltage(self, display_callback=True):
        """
        Return the bus voltage in volts.

        :return: If there is a callback specified, call it.
                 Update last voltage
        """
        value = self._voltage_register()
        value = float(value) * self.__BUS_MILLIVOLTS_LSB / 1000
        frame = [0x11, self.address, 0, value, 'V', time.time()]
        if display_callback:
            if self.board.ina219_callback:
                self.board.ina219_callback(frame)
        self.board.ina_last_value_bus_voltage = frame

    def supply_voltage(self, display_callback=True):
        """
        Return the bus supply voltage in volts.

        This is the sum of the bus voltage and shunt voltage. A
        DeviceRangeError exception is thrown if current overflow occurs.

        """
        self.voltage(display_callback=False)
        self.shunt_voltage(display_callback=False)
        last_bus_voltage_frame = self.board.ina_read_bus_voltage_last()
        last_bus_voltage = last_bus_voltage_frame[3]
        last_shunt_voltage_frame = self.board.ina_read_shunt_voltage_last()
        last_shunt_voltage = last_shunt_voltage_frame[3]
        value = last_bus_voltage + float(last_shunt_voltage / 1000)
        frame = [0x11, self.address, 2, value, 'V', time.time()]
        if display_callback:
            if self.board.ina219_callback:
                self.board.ina219_callback(frame)
        self.board.ina_last_value_supply_voltage = frame

    def current(self):
        """
        Return the bus current in milliamps.

        A DeviceRangeError exception is thrown if current overflow occurs.

        :return: bus current.
        """
        self._handle_current_overflow()
        value = self._current_register() * self._current_lsb * 1000
        frame = [0x11, self.address, 1, value, 'mA', time.time()]
        if self.board.ina219_callback:
            self.board.ina219_callback(frame)
        self.board.ina_last_value_bus_current = frame

    def power(self):
        """
        Return the bus power consumption in milliwatts.

        A DeviceRangeError exception is thrown if current overflow occurs.

        :return: power
        """
        value = self._current_register() * self._current_lsb * 1000
        frame = [0x11, self.address, 4, value, 'mW', time.time()]
        if self.board.ina219_callback:
            self.board.ina219_callback(frame)
        self.board.ina_last_value_power = frame

        self._handle_current_overflow()
        return self._power_register() * self._power_lsb * 1000

    def shunt_voltage(self, display_callback=True):
        """
        Return the shunt voltage in millivolts.

        A DeviceRangeError exception is thrown if current overflow occurs.

        :return shunt voltage
        """
        self._handle_current_overflow()
        value = self._shunt_voltage_register() * self.__SHUNT_MILLIVOLTS_LSB
        frame = [0x11, self.address, 3, value, 'mV', time.time()]
        if display_callback:
            if self.board.ina219_callback:
                self.board.ina219_callback(frame)
        self.board.ina_last_value_shunt_voltage = frame

    def ina_sleep(self):
        """
        Put the INA219 into power down mode."""

        configuration = self._read_configuration()
        self._configuration_register(configuration & 0xFFF8)

    def ina_wake(self):
        """
        Wake the INA219 from power down mode.
        """

        configuration = self._read_configuration()
        self._configuration_register(configuration | 0x0007)
        # 40us delay to recover from powerdown (p14 of spec)
        time.sleep(0.00004)

    def current_overflow(self):
        """
        Return true if the sensor has detect current overflow.

        In this case the current and power values are invalid.
        """
        return self._has_current_overflow()

    def ina_reset(self):
        """
        Reset the INA219 to its default configuration.
        """
        self._configuration_register(1 << self.__RST)

    def _handle_current_overflow(self):
        """
        Handle current overflow conditions.
        """
        if self._auto_gain_enabled:
            while self._has_current_overflow():
                self._increase_gain()
        else:
            if self._has_current_overflow():
                raise DeviceRangeError(self.__GAIN_VOLTS[self._gain])

    def _determine_gain(self, max_expected_amps):
        """
        Determine the gain.

        :param max_expected_amps: maximum expected current.

        :return: gain
        """
        shunt_v = max_expected_amps * self._shunt_ohms
        if shunt_v > self.__GAIN_VOLTS[3]:
            raise ValueError(self.__RNG_ERR_MSG % max_expected_amps)
        gain = min(v for v in self.__GAIN_VOLTS if v > shunt_v)
        return self.__GAIN_VOLTS.index(gain)

    def _increase_gain(self):
        """
        Increase the gain.
        """
        self.logger.info(self.__LOG_MSG_3)
        gain = self._read_gain()
        if gain < len(self.__GAIN_VOLTS) - 1:
            gain = gain + 1
            self._calibrate(self.__BUS_RANGE[self._voltage_range],
                            self.__GAIN_VOLTS[gain])
            self._configure_gain(gain)
            # 1ms delay required for new configuration to take effect,
            # otherwise invalid current/power readings can occur.
            time.sleep(0.001)
        else:
            self.logger.info('Device limit reach, gain cannot be increased')
            raise DeviceRangeError(self.__GAIN_VOLTS[gain], True)

    def _configure(self, voltage_range, gain, bus_adc, shunt_adc):
        """
        Set the configuration regsister.

        :param voltage_range: voltage range
        :param gain: gain


        :param bus_adc: bus_adc

        :param shunt_adc: shunt_adc
        """
        configuration = (
                voltage_range << self.__BRNG | gain << self.__PG0 |
                bus_adc << self.__BADC1 | shunt_adc << self.__SADC1 |
                self.__CONT_SH_BUS)
        self._configuration_register(configuration)

    def _calibrate(self, bus_volts_max, shunt_volts_max,
                   max_expected_amps=None):
        """
        Calibrate the device.

        :param bus_volts_max: maximum bus voltage

        :param shunt_volts_max: maximum shunt voltage

        :param max_expected_amps: expected maximum amps
        """
        self.logger.info(
            self.__LOG_MSG_2 %
            (bus_volts_max, shunt_volts_max,
             self.__max_expected_amps_to_string(max_expected_amps)))

        max_possible_amps = shunt_volts_max / self._shunt_ohms

        self.logger.info("max possible current: %.3fA" %
                         max_possible_amps)

        self._current_lsb = \
            self._determine_current_lsb(max_expected_amps, max_possible_amps)
        self.logger.info("current LSB: %.3e A/bit" % self._current_lsb)

        self._power_lsb = self._current_lsb * 20
        self.logger.info("power LSB: %.3e W/bit" % self._power_lsb)

        max_current = self._current_lsb * 32767
        self.logger.info("max current before overflow: %.4fA" % max_current)

        max_shunt_voltage = max_current * self._shunt_ohms
        self.logger.info("max shunt voltage before overflow: %.4fmV" %
                         (max_shunt_voltage * 1000))

        calibration = trunc(self.__CALIBRATION_FACTOR /
                            (self._current_lsb * self._shunt_ohms))
        self.logger.info(
            "calibration: 0x%04x (%d)" % (calibration, calibration))
        self._calibration_register(calibration)

    def _determine_current_lsb(self, max_expected_amps, max_possible_amps):
        """
        Get the current least significant byte.

        :param max_expected_amps: maximum expected current

        :param max_possible_amps: maximum possible current

        :return: current lsb
        """
        if max_expected_amps is not None:
            if max_expected_amps > round(max_possible_amps, 3):
                raise ValueError(self.__AMP_ERR_MSG %
                                 (max_expected_amps, max_possible_amps))
            self.logger.info("max expected current: %.3fA" %
                             max_expected_amps)
            if max_expected_amps < max_possible_amps:
                current_lsb = max_expected_amps / self.__CURRENT_LSB_FACTOR
            else:
                current_lsb = max_possible_amps / self.__CURRENT_LSB_FACTOR
        else:
            current_lsb = max_possible_amps / self.__CURRENT_LSB_FACTOR

        if current_lsb < self._min_device_current_lsb:
            current_lsb = self._min_device_current_lsb
        return current_lsb

    def _configuration_register(self, register_value):
        """
        Set the configuration register

        :param register_value: register value
        """
        self.logger.debug("configuration: 0x%04x" % register_value)
        self.__write_register(self.__REG_CONFIG, register_value)

    def _read_configuration(self):
        """
        Read the configurations register

        :return: configuration register value
        """
        return self.__read_register(self.__REG_CONFIG)

    def _calculate_min_current_lsb(self):
        """
        Calculate the minimum current least significant byte.

        :return: current lsb
        """
        return self.__CALIBRATION_FACTOR / \
               (self._shunt_ohms * self.__MAX_CALIBRATION_VALUE)

    def _read_gain(self):
        """
        Get the gain

        Read the configuration register and calculate the gain.

        :return: gain
        """
        configuration = self._read_configuration()
        gain = (configuration & 0x1800) >> self.__PG0
        self.logger.info("gain is currently: %.2fV" % self.__GAIN_VOLTS[gain])
        return gain

    def _configure_gain(self, gain):
        """
        Set the configuration register gain value.

        :param gain: gain
        """
        configuration = self._read_configuration()
        configuration = configuration & 0xE7FF
        self._configuration_register(configuration | (gain << self.__PG0))
        self._gain = gain
        self.logger.info("gain set to: %.2fV" % self.__GAIN_VOLTS[gain])

    def _calibration_register(self, register_value):
        """
        Write a value to the calibration register.

        :param register_value: value
        """
        self.logger.debug("calibration: 0x%04x" % register_value)
        self.__write_register(self.__REG_CALIBRATION, register_value)

    def _has_current_overflow(self):
        """
        Determine if there is a current overflow.

        :return: True if overflow found
        """
        ovf = self._read_voltage_register() & self.__OVF
        return ovf == 1

    def _voltage_register(self):
        """
        Retrieve the value in the voltage register
        correcting the bit positions.

        :return: voltage value
        """
        register_value = self._read_voltage_register()
        return register_value >> 3

    def _read_voltage_register(self):
        """
        Read the voltage register.

        :return: Voltage register raw value.
        """
        return self.__read_register(self.__REG_BUSVOLTAGE)

    def _current_register(self):
        """
        Read the current register.

        :return: The current register value.
        """
        return self.__read_register(self.__REG_CURRENT, True)

    def _shunt_voltage_register(self):
        """
        Read the shut voltage register value.

        :return: The shunt voltage.
        """
        return self.__read_register(self.__REG_SHUNTVOLTAGE, True)

    def _power_register(self):
        """
        Read the power register.

        :return: The power value.
        """
        return self.__read_register(self.__REG_POWER)

    def __validate_voltage_range(self, voltage_range):
        """
        Validate the voltage range.

        :param voltage_range: range
        """
        if voltage_range > len(self.__BUS_RANGE) - 1:
            raise ValueError(self.__VOLT_ERR_MSG)

    def __write_register(self, register, register_value):
        register_bytes = list(self.__to_bytes(register_value))
        self.logger.debug(
            "write register 0x%02x: 0x%04x 0b%s" %
            (register, register_value,
             self.__binary_as_string(register_value)))
        register_bytes.insert(0, register)
        self.board.i2c_write(self.address, register_bytes)

    def __read_register(self, register, negative_value_supported=False):
        """
        Read a register using Firmata

        :param register: Register value.

        :param negative_value_supported: If True, correct for a signed value.

        :return: register value
        """
        self.board.i2c_read(self.address, register, 2)
        # time.sleep(.1)
        time.sleep(.3)
        register_value = self.board.i2c_read_saved_data(self.address)
        # convert to integer
        register_value = (register_value[0] << 8) + register_value[1]
        if negative_value_supported:
            if register_value > 32767:
                register_value -= 65536

        return register_value

    def __to_bytes(self, register_value):
        """
        Convert a value to bytes.

        :param register_value: integer value

        :return: a list of bytes
        """
        return [(register_value >> 8) & 0xFF, register_value & 0xFF]

    def __binary_as_string(self, register_value):
        """
        Convert a binary value to a string.

        :param register_value: value

        :return: value converted to a string.
        """
        return bin(register_value)[2:].zfill(16)

    def __max_expected_amps_to_string(self, max_expected_amps):
        """
        Convert the maximum expected amps to a string.

        :param max_expected_amps: the maximum expected value.

        :return: value converted to a string.
        """
        if max_expected_amps is None:
            return ''
        else:
            return ', max expected amps: %.3fA' % max_expected_amps


class DeviceRangeError(Exception):
    """
    Class defining the INA219 DeviceRangeError Exception.
    """

    __DEV_RNG_ERR = ('Current out of range (overflow), '
                     'for gain %.2fV')

    def __init__(self, gain_volts, device_max=False):
        """
        Construct a DeviceRangeError.

        :param gain_volts: the voltage gain.

        :param device_max: a flag to indicate if device limit was reached.
        """
        msg = self.__DEV_RNG_ERR % gain_volts
        if device_max:
            msg = msg + ', device limit reached'
        super(DeviceRangeError, self).__init__(msg)
        self.gain_volts = gain_volts
        self.device_limit_reached = device_max
