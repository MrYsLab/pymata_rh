# Understanding Input Data Collection And Reporting

## Firmata Input Data Collection and Reporting
FirmataExpress polls all input pins within the *loop method*
of the sketch.

Notification messages containing the pin number, pin type, and current data value
for the pin
are constructed and then transmitted to *pymata_rh*
over the serial link.

## Firmata Polls For Data Changes

### Digital Input
For digital input pins, all the pins are polled with *each* iteration of the FirmataExpress *loop* function,
with no delays. When the state of a pin has changed, Firmata creates a notification message 
and transmits it over the serial link to pymata_rh.

### Analog Input
For analog input pins, each pin is polled, and its current value is reported,
regardless of change. 
All analog input pins are nominally polled every 19 milliseconds.

### I2C Input

Unlike digital and analog inputs, most I2C devices report values only when a read request is issued 
 to the i2c device. For these i2c devices, a read request results in a single reply. 

Some i2c devices may be placed in a continuous read mode. In this
mode, the i2c device automatically sends update notifications,
 usually as quickly as possible. When in continuous i2c mode, 
the Firmata *loop* retrieves cached responses at a nominal polling rate of 19 milliseconds.

### Sonar (HC-SR04) Input
FirmataExpress supports HC-SR04 type distance sensors. The Firmata *loop* polls each device 
and reports its current value regardless of change.
The polling rate is nominally every 40 milliseconds for HC-SR04 type devices.

### DHT Temperature/Humidity Sensor Input
Both DHT 11 and 22 temperature humidity sensors are supported. The polling rate is approximately
2 seconds for each sensor because DHT devices require a long data capture time.

## PymataRh Input Data Processing

### Pymata_rh *Polling* For Input Data Changes
As pymata_rh receives input data notifications, 
it caches the data in internal data structures. These data structures retain
the value reported as well as the time of occurrence.
The application may query or poll these data structures to obtain the
latest data updates for a given pin. 

The pymata_rh API methods that implement polling are:

* analog_read
* digital_read
* i2c_read_saved_data
* dht_read
* sonar_read
* mpu_9250_read_saved_data
* ina_read_bus_voltage_last
* ina_read_bus_current_last
* ina_read_supply_voltage_last
* ina_read_shunt_voltage_last
* ina_read_power_last

### Using *Callbacks* Instead Of Polling
Callback notification is much more efficient than using polling when dealing with input
data. What is a callback? A callback is simply a function or method written by you that is registered
with pymata_rh to automatically and immediately notify your application of data changes.

### Functions That Can Be Registered For Callbacks
You may optionally *register* callback functions when using any of the following pymata_rh API
methods:

* set_pin_mode_analog_input
* set_pin_mode_digital_input
* set_pin_mode_digital_input_pullup
* set_pin_mode_dht
* set_pin_mode_sonar
* enable_analog_reporting (an alias for set_pin_mode_analog_input)
* i2c_read
* i2c_read_continuous
* i2c_read_restart_transmission
* mpu_9250_read_data (callback is established in mpu_9250_initialize)
* ina219 - a single callback is established in ina_initialize and is shared by all of the following:

        * ina_read_bus_voltage
        * ina_read_bus_current
        * ina_read_supply_voltage
        * ina_read_shunt_voltage
        * ina_read_power

## Callback Function Scope
The scope of a callback is extremely flexible. 
You may register a callback function:

* On a one to one basis for the desired input.
* Or you may group pins of a single type, such as analog input
or digital input, 
* Or even have a single callback function handle all input data notifications.

The data that pymata_rh sends to the callback provides all the 
information your program needs to differentiate one callback from another.

You may also use callbacks with some pins while using polling for others. Polling is available
for all input pins whether callbacks are in use or not.

## The Callback Return Values

A callback function is specified to accept a single input parameter, typically named
***data***. The input parameter will be filled with a list when pymata_rh invokes the callback.

A description of what is contained in the list
is provided in the 
[reference API.](https://htmlpreview.github.io/?https://github.com/MrYsLab/pymata_rh/blob/master/html/pymata_rh/index.html) 

```python
def my_callback(data):
    """
    :param data: a list containing pin type, pin number, 
                 data value and time-stamp
    """
# Your code goes here to process the data
```

For example, the callback data for a digital input pin is structured as follows:

```python
[pin_type, pin_number, pin_value, raw_time_stamp]
```
#### Pin Type Identifiers

All callbacks provide a *pin_type* as the first value in the list. A *pin_type* allows you to 
quickly identify the source of the callback. In addition, all callbacks provide a raw time-stamp
as the last entry of the list. Other fields are specific to the callback type.

    INPUT = 0x00  # pin set as input
    OUTPUT = 0x01  # pin set as output
    ANALOG = 0x02  # analog pin in analogInput mode
    PWM = 0x03  # digital pin in PWM output mode
    SERVO = 0x04  # digital pin in Servo output mode
    I2C = 0x06  # pin included in I2C setup
    PULLUP = 0x0b  # Any pin in pullup mode
    SONAR = 0x0c  # Any pin in SONAR mode
    DHT = 0x0f  # DHT sensor
    MPU9250 = 0x10 # mpu
    INA219 = 0x11 # current sensor

**TIP**: You should keep callback functions as short as possible. If processing callback
data within the callback function results in blocking your application, 
you may wish to consider spawning a separate
processing thread.


<br>
<br>

Copyright (C) 2020 Alan Yorinks. All Rights Reserved.
