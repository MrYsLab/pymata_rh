# Introduction
Independent of what the Robot HAT MM1 pin names suggest, pins may be able to be configured to operate in one of several modes.
The modes available to any given pin is dependent upon pin type.
For the pin modes available to a given pin, please refer to the pin table on the 
[first page of this document.](index.md)


For example, 
a digital pin may be configured for input, output, and for some digital pins, PWM output operation.

When setting a pin mode, a validity check is performed for the specified pin.
If not, a RuntimeError exception is raised.

Analog input pins
are even more flexible.
They may be configured for analog input, digital input, or digital output operation.

PymataRh requires that before using a pin, its mode must be explicitly set. This is accomplished using one of
the pymata_rh mode setting methods.


In this section, the methods to set pin modes are presented. For each API method, a link to an example is
provided. 

## ANALOG PIN MODE

### set_pin_mode_analog_input

```python
 def set_pin_mode_analog_input(self, pin_number, callback=None, differential=1)

    Set a pin as an analog input.

    :param pin_number: arduino pin number

    :param callback: callback function

    :param differential: This value needs to be met for a callback to be invoked.

    callback returns a data list:

    [pin_type, pin_number, pin_value, raw_time_stamp]

    The pin_type for analog input pins = 2
```
**Examples:**

1. [analog_input_with_time_stamps.py](https://github.com/MrYsLab/pymata_rh/blob/master/examples/analog_input_with_time_stamps.py)

**Notes:** 

1. When an analog input message is received from Firmata, the current reported
data value is compared with that of the previously reported value. If the difference, either positive or negative,
is greater than the differential parameter, then the callback is invoked. This is useful when you have a "noisy"
input that may constantly fluctuate by a small value, and you wish to ignore the noise.
2. PymataRh refers to analog pins using the numeric portion of the pin number only. 
For example, pin A3 is referred to as pin 3.
3. Data reporting via callbacks for this pin begins immediately after this method is called. 




## DIGITAL PIN MODES

### set_pin_mode_digital_input
```python
 def set_pin_mode_digital_input(self, pin_number, callback=None)

    Set a pin as a digital input.

    :param pin_number: arduino pin number

    :param callback: callback function

    callback returns a data list:

    [pin_type, pin_number, pin_value, raw_time_stamp]

    The pin_type for digital input pins = 0
```

**Examples:** 

1. [digital_input.py](https://github.com/MrYsLab/pymata_rh/blob/master/examples/digital_input.py)
2. [digital_input_debounce.py](https://github.com/MrYsLab/pymata_rh/blob/master/examples/digital_input_debounce.py)

**Notes:** 

Data reporting via callbacks for this pin begins immediately after this method is called. 


### set_pin_mode_digital_input_pullup

```python
 def set_pin_mode_digital_input_pullup(self, pin_number, callback=None)

    Set a pin as a digital input with pullup enabled.

    :param pin_number: arduino pin number

    :param callback: callback function

    callback returns a data list:

    [pin_type, pin_number, pin_value, raw_time_stamp]

    The pin_type for digital input pins with pullups enabled = 11

```
**Example:** 

1. [digital_input_pullup.py](https://github.com/MrYsLab/pymata_rh/blob/master/examples/digital_input_pullup.py) 

**Notes:** 

Data reporting via callbacks for this pin begins immediately after this method is called. 

### set_pin_mode_digital_output
```python
 def set_pin_mode_digital_output(self, pin_number)

    Set a pin as a digital output pin.

    :param pin_number: arduino pin number

```
**Examples:** 

1. [digital_output.py](https://github.com/MrYsLab/pymata_rh/blob/master/examples/digital_output.py)

### set_pin_mode_pwm_output

```python
 def set_pin_mode_pwm_output(self, pin_number)

    Set a pin as a pwm (analog output) pin.

    :param pin_number:arduino pin number
```

**Example:**
1. [fade.py](https://github.com/MrYsLab/pymata_rh/blob/master/examples/fade.py)

**Notes:** 

Only specific digital pins support PWM mode. Check with the Arduino documentation
to determine which pins support PWM for your board.

## DEVICE TYPE PIN MODES

### set_pin_mode_dht

```python
def set_pin_mode_dht(self, pin_number, sensor_type=22, differential=.1, callback=None):
    """
    Configure a DHT sensor prior to operation.
    Up to 6 DHT sensors are supported

    :param pin_number: digital pin number on arduino.

    :param sensor_type: type of dht sensor
                        Valid values = DHT11, DHT12, DHT22, DHT21, AM2301

    :param differential: This value needs to be met for a callback
                         to be invoked.

    :param callback: callback function

    callback: returns a data list:

    [pin_type, pin_number, DHT type, humidity value, temperature raw_time_stamp]

    The pin_type for DHT input pins = 15

            ERROR CODES: If either humidity or temperature value:
                          == -1 Configuration Error
                          == -2 Checksum Error
                          == -3 Timeout Error
    """
```
**Examples:** 

1. [dht.py](https://github.com/MrYsLab/pymata_rh/blob/master/examples/dht.py)

**Notes:** 

You may reset the differential value by calling this method again with a new differential value.

### set_pin_mode_i2c
```python
def set_pin_mode_i2c(self, read_delay_time=0)

    Establish the standard Arduino i2c pins for i2c utilization.

    NOTE: THIS METHOD MUST BE CALLED BEFORE ANY I2C REQUEST IS MADE:
          This method initializes Firmata for I2c operations.

    :param read_delay_time (in microseconds): an optional parameter, default is 0

    NOTE: Callbacks are set within the individual i2c read methods of this API. 
          See i2c_read, i2c_read_continuous, or i2c_read_restart_transmission.
```

**Example:**
1. [i2c_adxl345_accelerometer.py](https://github.com/MrYsLab/pymata_rh/blob/master/examples/i2c_adxl345_accelerometer.py)

### set_pin_mode_servo
```python
 def set_pin_mode_servo(self, pin, min_pulse=544, max_pulse=2400)

    Configure a pin as a servo pin. Set pulse min, max in ms.

    :param pin: Servo Pin.

    :param min_pulse: Min pulse width in ms.

    :param max_pulse: Max pulse width in ms.
```
**Example:**
1. [servo.py](https://github.com/MrYsLab/pymata_rh/blob/master/examples/servo.py)

### set_pin_mode_sonar
```python
 def set_pin_mode_sonar(self, trigger_pin, echo_pin, callback=None, timeout=80000)

    This is a FirmataExpress feature.

    Configure the pins, ping interval and maximum distance for 
    an HC-SR04 type device.

    Up to a maximum of 6 SONAR devices is supported. 
    If the maximum is exceeded a message is sent to the console and 
    the request is ignored.

    NOTE: data is measured in centimeters. Callback is 
    called only when the latest value received is different than the previous.

    :param trigger_pin: The pin number of for the trigger (transmitter).

    :param echo_pin: The pin number for the received echo.

    :param callback: optional callback function to report sonar data changes

    :param timeout: a tuning parameter. 80000UL equals 80ms.

    callback returns a data list:

    [pin_type, trigger_pin_number, distance_value (in cm), raw_time_stamp]

    The pin_type for sonar pins = 12

```
**Example:**
1. [hc-sr04_distance_sensor.py](https://github.com/MrYsLab/pymata_rh/blob/master/examples/hc-sr04_distance_sensor.py)

### The MPU9250 and INA219 Devices

To initialize these devices, please see
[Configuring And Reading The MPU9250 9DOF Device](mpu9250.md) and 
[Configuring And Reading The INA219 Current, Shunt, And Power Monitor.](ina219.md)

<br>
<br>

Copyright (C) 2020 Alan Yorinks. All Rights Reserved.
