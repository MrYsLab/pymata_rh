# The PymataRh Class

To use the PymataRh class, you must first import it:

```python
from pymata_rh import pymata_rh
```

and then instantiate it:

```python
board = pymata_rh.PymataRh()
```

The *board* variable contains a reference to the PymataRh instance. You use this
reference to access the PymataRh methods of the instance. 

For example, to cleanly shutdown your PymataRh application, you might call
the *shutdown* method:

```python
board.shutdown()
```

Of course, you can name the instance variable, anything that is meaningful to you.
There is nothing *magic* about the name *board*.

NOTE: pymata_rh considers the Robo HAT MM1 as an Arduino device. The term
*Arduino* anywhere in the discussion is referring to the Robo HAT MM1.

## Understanding The PymataRh *\__init__* Parameters
```python
 def __init__(self, com_port=None, baud_rate=115200,
                 arduino_instance_id=1, arduino_wait=4,
                 sleep_tune=0.000001,
                 shutdown_on_exception=True):
```

In most cases, you
 can accept all of the default parameters provided in the \__init__ method.
 
But there are times when you may wish to take advantage of the flexibility provided
by the \__init__ method parameters, so let's explore the definition and purpose
of each parameter:

### The Auto-Discovery Parameters - com_port, baud_rate, and arduino_instance
By accepting the default values for these parameters, pymata_rh assumes you have
flashed your Arduino with FirmataExpress. 

### com_port
The *com_port* parameter specifies a serial com_port, such as COM4 or '/dev/ttyACM0'
 used for PC to Arduino communication. If the default value of _None_ is accepted,
 pymata_rh will attempt to find the connected Arduino automatically.
 
### baud_rate
The default for this parameter is 115200, matching the speed set for the 
FirmataExpress sketch. 

### arduino_instance_id
This parameter
allows pymata_rh to connect to an Arduino with a matching ID.

This is useful if you have multiple Arduino's plugged into your computer,
and you wish to have a specific Arduino selected for connection. 

The default value for the arduino_instance_id for both pymata_rh and FirmataExpress is 1.

Instructions for changing the FirmataExpress value may be found
in the [**Installing FirmataExpress**](../firmata_express) section of this document.

### arduino_wait
This parameter specifies the amount of time that pymata_rh assumes it takes for an Arduino 
to reboot the FirmataExpress (or StandardFirmata) sketch from a power-up or reset.

The default is 4 seconds. If the Arduino is not fully booted when com_port auto-discovery begins,
auto-discovery will fail.

### sleep_tune
This is the sleep value expressed in seconds, that is used at several strategic
points in pymata_rh. For example, the serial receiver continuously checks the serial port receive
buffer for an available
character to process. If there is no character in the
buffer, pymata_rh sleeps for the sleep_tune period before checking again.

The default value is 0.000001 seconds.

### shutdown_on_exception
When this parameter is set to True, the shutdown method is automatically
called when an exception is detected. This disables reporting for both digital and analog pins, 
in addition to closing the serial port.

By setting this parameter to False, the Arduino may continue to send data to
your application even after restarting it.

The default is True and recommended to be used.


### Examples
   Each [example on GitHub](https://github.com/MrYsLab/pymata_rh/tree/master/examples) 
   demonstrates instantiating the Pymata_rh class.
   
<br>
<br>

Copyright (C) 2020 Alan Yorinks. All Rights Reserved.
