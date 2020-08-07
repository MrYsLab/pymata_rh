# Setting Pin and Device Values
In this section, we discuss writing data to:

* Digital pins.
* PWM pins.
* Servo motors.

**Note:** I2C devices are discussed in the [next section](../i2c)
 of this guide. 

## digital_write
```python
 def digital_write(self, pin, value)

    Set the specified pin to the specified value.

    :param pin: arduino pin number

    :param value: pin value (1 or 0)

```
**Example:**

1. [digital_output.py](https://github.com/MrYsLab/pymata_rh/blob/master/examples/digital_output.py) 


## pwm_write
```python
 def pwm_write(self, pin, value)

    Set the selected pwm pin to the specified value.

    :param pin: PWM pin number

    :param value: Pin value (0 - 0x4000)
```

**Example:**

1. [fade.py](https://github.com/MrYsLab/pymata_rh/blob/master/examples/fade.py) 

**Notes:** 

The value parameter is typically set between 0 and 255.


## servo_write
```python
 def servo_write(self, pin, position)

    This is an alias for analog_write to set the position of a servo that has 
    been previously configured using set_pin_mode_servo.

    :param pin: arduino pin number

    :param position: servo position
```
**Example:**

1. [servo.py](https://github.com/MrYsLab/pymata_rh/blob/master/examples/servo.py) 

**Notes:** 

For an angular servo, the position parameter is set between 0 and 180 (degrees).
For a continuous servo, 0 is full-speed in one direction, 
180 is full speed in the other, and a value near 90 is no movement.


<br>
<br>

Copyright (C) 2020 Alan Yorinks. All Rights Reserved.
