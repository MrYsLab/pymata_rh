# Analog and Digital Input Pin  Reporting

Callback reporting begins immediately upon setting a pin as either a digital or analog
input pin. If your application should unexpectedly exit without an orderly shutdown,
the Robo HAT MM1 may continue to stream data, even though your application has exited.

In this scenario, if you do not re-power the Robo HAT MM1 before restarting your application,
the continuing data stream may cause pymata_rh to fail because the data stream is out
of sync with pymata_rh's state.

One way of making sure that you do not encounter this scenario is to turn off
reporting before exiting your application.


## disable_analog_reporting

```python
 def disable_analog_reporting(self, pin)

    Disables analog reporting for a single analog pin.

    :param pin: Analog pin number. For example for A0, the number is 0.
```

**Example:**

1. [disable_enable_analog_reporting.py](https://github.com/MrYsLab/pymata_rh/blob/master/examples/disable_enable_analog_reporting.py) 

**Notes:**

This method resets the pin mode for the specified pin to a digital input
mode. 


## enable_analog_reporting
```python
 def enable_analog_reporting(self, pin, callback=None, differential=1)

    Enables analog reporting. This is an alias for set_pin_mode_analog_input. 
    Disabling analog reporting sets the pin to a digital input pin, 
    so we need to provide the callback and differential if we wish to specify it.

    :param pin: Analog pin number. For example for A0, the number is 0.

    :param callback: callback function

    :param differential: This value needs to be met for a callback to be invoked.
```

**Example:**

1. [disable_enable_analog_reporting.py](https://github.com/MrYsLab/pymata_rh/blob/master/examples/disable_enable_analog_reporting.py) 

## disable_digital_reporting
```python
 def disable_digital_reporting(self, pin)

    Disables digital reporting. By turning reporting off for this pin, 
    reporting is disabled for all 8 bits in the "port"

    :param pin: Pin and all pins for this port
```
**Example:**

1. [disable_enable_digital_reporting.py](https://github.com/MrYsLab/pymata_rh/blob/master/examples/disable_enable_digital_reporting.py) 

## enable_digital_reporting

```python
 def enable_digital_reporting(self, pin)

    Enables digital reporting. By turning reporting on for all 8 
    bits in the "port" - this is part of Firmata's protocol specification.

    :param pin: Pin and all pins for this port

    :returns: No return value

```
**Example:**

1. [disable_enable_digital_reporting.py](https://github.com/MrYsLab/pymata_rh/blob/master/examples/disable_enable_digital_reporting.py) 

# MPU9250 9DOF Sensor  Reporting
To understand how to enable and disable reporting for this device,
please go to [this page.](mpu9250.md)
<br>
<br>

Copyright (C) 2020 Alan Yorinks. All Rights Reserved.
