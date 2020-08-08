# Informational Reports
All of the following methods are synchronous. The methods
block until they return.


 
## get_firmware_version
```python
  def get_firmware_version(self)

    This method retrieves the Firmata firmware version

    :returns: Firmata firmware version
```
**Example:** 

1. [retrieve_firmware_version.py](https://github.com/MrYsLab/pymata_rh/blob/master/examples/retrieve_firmware_version.py)

**Notes:**

This report will return the major and minor numbers of the release and 
the firmware name.


## get_pin_state
```python
def get_pin_state(self, pin):
    """
    This method retrieves a pin state report for the specified pin.
    Pin modes reported:
    INPUT   = 0x00  # digital input mode
    OUTPUT  = 0x01  # digital output mode
    ANALOG  = 0x02  # analog input mode
    PWM     = 0x03  # digital pin in PWM output mode
    SERVO   = 0x04  # digital pin in Servo output mode
    I2C     = 0x06  # pin included in I2C setup
    PULLUP  = 0x0b  # digital pin in input pullup mode
    SONAR   = 0x0c  # digital pin in SONAR mode
    DHT     = 0x0f

    :param pin: Pin of interest

    :returns: pin state report
    """
```
**Example:** 

1. [retrieve_pin_state.py](https://github.com/MrYsLab/pymata_rh/blob/master/examples/retrieve_pin_state.py)

**Notes:**

Refer to the [Firmata Protocol specification](https://github.com/firmata/protocol/blob/master/protocol.md#pin-state-query)
 for an explanation of the report data.]

## get_protocol_version
```python
 def get_protocol_version(self)

    This method returns the major and minor values 
    for the protocol version, i.e. 2.5

    :returns: Firmata protocol version
```
**Example:**

1. [retrieve_protocol_version.py](https://github.com/MrYsLab/pymata_rh/blob/master/examples/retrieve_protocol_version.py)


## get_pymata_version
```python
  def get_pymata_version(self)

    This method retrieves the PyMata Express version number

    :returns: PyMata Express version number.
```
**Example:** 

1. [retrieve_pymata_version.py](https://github.com/MrYsLab/pymata_rh/blob/master/examples/retrieve_pymata_version.py)

<br>
<br>

Copyright (C) 2020 Alan Yorinks. All Rights Reserved.
