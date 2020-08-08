# Retrieving The Latest Input Data Values
As was mentioned earlier, 
[callbacks](../polling/#using-callbacks-instead-of-polling) are preferred over 
polling for input data change notifications.

That being said, your application may dictate using polling over callbacks. This section
describes the API methods to retrieve the latest cached input data values.

## analog_read
```python
 def analog_read(self, pin)

    Retrieve the last data update for the specified analog pin.

    :param pin: Analog pin number (ex. A2 is specified as 2)

    :returns: A list = [last value change, time_stamp]
```

**Examples:**

1. [analog_input_with_time_stamps.py](https://github.com/MrYsLab/pymata_rh/blob/master/examples/analog_input_with_time_stamps.py)

## dht_read
```python
def dht_read(self, pin):
    """
    Retrieve the last data update for the specified dht pin.

    :param pin: digital pin number

    :return: A list = [humidity, temperature  time_stamp]

             ERROR CODES: If either humidity or temperature value:
                          == -1 Configuration Error
                          == -2 Checksum Error
                          == -3 Timeout Error

    """
```
**Examples:**

1. [dht.py](https://github.com/MrYsLab/pymata_rh/blob/master/examples/dht.py)

## digital_read
```python
 def digital_read(self, pin)

    Retrieve the last data update for the specified digital pin.

    :param pin: Digital pin number

    :returns: A list = [last value change, time_stamp]

``` 
**Examples:**

1. [digital_input.py](https://github.com/MrYsLab/pymata_rh/blob/master/examples/digital_input.py)
2. [digital_input_debounce.py](https://github.com/MrYsLab/pymata_rh/blob/master/examples/digital_input_debounce.py)
3. [digital_input_pullup.py](https://github.com/MrYsLab/pymata_rh/blob/master/examples/digital_input_pullup.py) 

## i2c_read_saved_data
```python
 def i2c_read_saved_data(self, address)

    This method retrieves cached i2c data to support a polling mode.

    :param address: I2C device address

    :returns: Last cached value reported This contains the number of bytes requested followed by the time_stamp.
```
**Example:**

1. [i2c_adxl345_accelerometer.py](https://github.com/MrYsLab/pymata_rh/blob/master/examples/i2c_adxl345_accelerometer.py)


## sonar_read
```python
 def sonar_read(self, trigger_pin)

    This is a FirmataExpress feature

    Retrieve Ping (HC-SR04 type) data. The data is presented as a dictionary.

    The 'key' is the trigger pin specified in sonar_config() and the 'data' is the current measured distance (in centimeters) for that pin. If there is no data, the value is set to None.

    :param trigger_pin: key into sonar data map

    :returns: A list = [last value, raw time_stamp]
```
**Example:**
1. [hc-sr04_distance_sensor.py](https://github.com/MrYsLab/pymata_rh/blob/master/examples/hc-sr04_distance_sensor.py)

## Polling the MPU9250 and INA219

To poll the stored values for these devices, please see
[Configuring And Reading The MPU9250 9DOF Device](mpu9250.md) and 
[Configuring And Reading The INA219 Current, Shunt, And Power Monitor.](ina219.md)

<br>
<br>
Copyright (C) 2020 Alan Yorinks. All Rights Reserved.
