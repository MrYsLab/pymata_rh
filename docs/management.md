# Remote Firmata Management
The methods in this section allow your application to 
perform some Firmata management functions remotely.

## send_reset

```python
 def send_reset(self)

    Send a Sysex reset command to the Robot HAT MM1
```

**Examples:**

All examples call shutdown, which in turn calls send_reset.

**Notes:**

This command will reset several Firmata internal data structures. 

* It resets its internal i2c flags to indicate there are no i2c devices present.
* Digital reporting is turned off.
* It resets any analog pin that was set to a digital mode back to analog mode.
* If a pin was configured for tone, the tone is turned off.
* It clears all servo entries from its servo map.
* It sets the number of active sonar devices to zero.

The shutdown method calls *send_reset*.

## shutdown

```python
 def shutdown(self)

    This method attempts an orderly shutdown.
    If any exceptions are thrown, they are ignored.
```
**Examples:**

All the examples call shutdown.

<br>
<br>

Copyright (C) 2020 Alan Yorinks. All Rights Reserved.
