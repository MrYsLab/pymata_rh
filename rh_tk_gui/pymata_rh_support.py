#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 5.4
#  in conjunction with Tcl version 8.6
"""
robohat_gateway.py

This is the OneGPIO gateway for pymata_rh

Support module partially generated by PAGE version 5.4
in conjunction with Tcl version 8.6

 Copyright (c) 2020 Alan Yorinks All right reserved.

 This software is free software; you can redistribute it and/or
 modify it under the terms of the GNU AFFERO GENERAL PUBLIC LICENSE
 Version 3 as published by the Free Software Foundation; either
 or (at your option) any later version.
 This library is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 General Public License for more details.

 You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
 along with this library; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
import sys
import msgpack
import zmq
from python_banyan.banyan_base import BanyanBase

try:
    # noinspection PyPep8Naming
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk

    py3 = False
except ImportError:
    import tkinter.ttk as ttk

    py3 = True

if py3:
    from tkinter import messagebox
else:
    # noinspection PyUnresolvedReferences
    import tkMessageBox as messagebox


# noinspection PyGlobalUndefined
def set_Tk_var():
    # noinspection PyGlobalUndefined
    global dummy
    dummy = tk.StringVar()
    # noinspection PyGlobalUndefined
    global ina_bus_current
    ina_bus_current = tk.StringVar()
    # noinspection PyGlobalUndefined
    global ina_bus_voltage
    ina_bus_voltage = tk.StringVar()
    # noinspection PyGlobalUndefined
    global ina_shunt_voltage
    ina_shunt_voltage = tk.StringVar()
    # noinspection PyGlobalUndefined
    global ina_supply_voltage
    ina_supply_voltage = tk.StringVar()
    # noinspection PyGlobalUndefined
    global ina_power
    ina_power = tk.StringVar()
    # noinspection PyGlobalUndefined
    global mpu_temp
    mpu_temp = tk.StringVar()
    # noinspection PyGlobalUndefined
    global gyro_x
    gyro_x = tk.StringVar()
    # noinspection PyGlobalUndefined
    global gyro_y
    gyro_y = tk.StringVar()
    # noinspection PyGlobalUndefined
    global gyro_z
    gyro_z = tk.StringVar()
    # noinspection PyGlobalUndefined
    global mag_x
    mag_x = tk.StringVar()
    # noinspection PyGlobalUndefined
    global mag_y
    mag_y = tk.StringVar()
    # noinspection PyGlobalUndefined
    global mag_z
    mag_z = tk.StringVar()
    # noinspection PyGlobalUndefined
    global acc_x
    acc_x = tk.StringVar()
    # noinspection PyGlobalUndefined
    global acc_y
    acc_y = tk.StringVar()
    # noinspection PyGlobalUndefined
    global acc_z
    acc_z = tk.StringVar()
    # noinspection PyGlobalUndefined
    global triggerr_Pin
    # noinspection SpellCheckingInspection
    triggerr_Pin = tk.StringVar()
    # noinspection PyGlobalUndefined
    global echo_pin
    echo_pin = tk.StringVar()
    # noinspection PyGlobalUndefined
    global sonar_distance
    sonar_distance = tk.StringVar()
    # noinspection PyGlobalUndefined
    global dht1_Pin
    dht1_Pin = tk.StringVar()
    # noinspection PyGlobalUndefined
    global dht1_type
    dht1_type = tk.StringVar()
    # noinspection PyGlobalUndefined
    global dht1_humidity
    dht1_humidity = tk.StringVar()
    # noinspection PyGlobalUndefined
    global dht1_temp
    dht1_temp = tk.StringVar()
    # noinspection PyGlobalUndefined
    global dht1_combobox
    dht1_combobox = tk.StringVar()
    # noinspection PyGlobalUndefined
    global combobox
    combobox = tk.StringVar()
    # noinspection PyGlobalUndefined
    global rcc1_in_value
    rcc1_in_value = tk.StringVar()
    # noinspection PyGlobalUndefined
    global rcc2_in_value
    rcc2_in_value = tk.StringVar()
    # noinspection PyGlobalUndefined
    global rcc3_in_value
    rcc3_in_value = tk.StringVar()
    # noinspection PyGlobalUndefined
    global rcc4_in_value
    rcc4_in_value = tk.StringVar()
    # noinspection PyGlobalUndefined
    global neopixel_in_value
    neopixel_in_value = tk.StringVar()
    # noinspection PyGlobalUndefined
    global servo_1mode
    servo_1mode = tk.StringVar()
    # noinspection PyGlobalUndefined
    global servo3_in_value
    servo3_in_value = tk.StringVar()
    # noinspection PyGlobalUndefined
    global servo4_in_value
    servo4_in_value = tk.StringVar()
    # noinspection PyGlobalUndefined
    global servo5_in_value
    servo5_in_value = tk.StringVar()
    # noinspection PyGlobalUndefined
    global servo6_in_value
    servo6_in_value = tk.StringVar()
    # noinspection PyGlobalUndefined
    global servo7_in_value
    servo7_in_value = tk.StringVar()
    # noinspection PyGlobalUndefined
    global servo8_in_value
    servo8_in_value = tk.StringVar()
    # noinspection PyGlobalUndefined
    global servo2_in_value
    servo2_in_value = tk.StringVar()
    # noinspection PyGlobalUndefined
    global servo_mode
    servo_mode = tk.StringVar()
    # noinspection PyGlobalUndefined
    global servo1_in_value
    servo1_in_value = tk.StringVar()
    # noinspection PyGlobalUndefined
    global rcc1_output_value
    rcc1_output_value = tk.DoubleVar()
    # noinspection PyGlobalUndefined
    global rcc1_mode
    rcc1_mode = tk.StringVar()
    # noinspection PyGlobalUndefined
    global rcc2_output_value
    rcc2_output_value = tk.DoubleVar()
    # noinspection PyGlobalUndefined
    global rcc2_mode
    rcc2_mode = tk.StringVar()
    # noinspection PyGlobalUndefined
    global rcc3_output_value
    rcc3_output_value = tk.DoubleVar()
    # noinspection PyGlobalUndefined
    global rcc3_mode
    rcc3_mode = tk.StringVar()
    # noinspection PyGlobalUndefined
    global rcc4_output_value
    rcc4_output_value = tk.DoubleVar()
    # noinspection PyGlobalUndefined
    global rcc4_mode
    rcc4_mode = tk.StringVar()
    # noinspection PyGlobalUndefined
    global neopixel_output_value
    neopixel_output_value = tk.DoubleVar()
    # noinspection PyGlobalUndefined
    global neopixel_mode
    neopixel_mode = tk.StringVar()
    # noinspection PyGlobalUndefined
    global led_output_value
    led_output_value = tk.DoubleVar()
    # noinspection PyGlobalUndefined
    global led_mode
    led_mode = tk.StringVar()
    # noinspection PyGlobalUndefined
    global servo1_output_value
    servo1_output_value = tk.DoubleVar()
    # noinspection PyGlobalUndefined
    global servo1_mode
    servo1_mode = tk.StringVar()
    # noinspection PyGlobalUndefined
    global servo2_output_value
    servo2_output_value = tk.DoubleVar()
    # noinspection PyGlobalUndefined
    global servo2_mode
    servo2_mode = tk.StringVar()
    # noinspection PyGlobalUndefined
    global servo3_output_value
    servo3_output_value = tk.DoubleVar()
    # noinspection PyGlobalUndefined
    global servo3_mode
    servo3_mode = tk.StringVar()
    # noinspection PyGlobalUndefined
    global servo4_output_value
    servo4_output_value = tk.DoubleVar()
    # noinspection PyGlobalUndefined
    global servo4_mode
    servo4_mode = tk.StringVar()
    # noinspection PyGlobalUndefined
    global servo5_output_value
    servo5_output_value = tk.DoubleVar()
    # noinspection PyGlobalUndefined
    global servo5_mode
    servo5_mode = tk.StringVar()
    # noinspection PyGlobalUndefined
    global servo6_output_value
    servo6_output_value = tk.DoubleVar()
    # noinspection PyGlobalUndefined
    global servo6_mode
    servo6_mode = tk.StringVar()
    # noinspection PyGlobalUndefined
    global servo7_output_value
    servo7_output_value = tk.DoubleVar()
    # noinspection PyGlobalUndefined
    global servo7_mode
    servo7_mode = tk.StringVar()
    # noinspection PyGlobalUndefined
    global servo8_output_value
    servo8_output_value = tk.DoubleVar()
    # noinspection PyGlobalUndefined
    global servo8_mode
    servo8_mode = tk.StringVar()


# noinspection PyGlobalUndefined,PyGlobalUndefined,PyGlobalUndefined,PyGlobalUndefined,PyGlobalUndefined,PyGlobalUndefined,PyGlobalUndefined,PyGlobalUndefined
def init(top, gui, *args, **kwargs):
    global w, top_level, root, bgs
    w = gui
    top_level = top
    root = top
    # instantiate the custom class
    bgs = BanyanGuiSupport()


# the following functions are generated by Page and populated by MisterYsLab.
# for each radio button handle its selection and if there is an
# associated slider widget, handle the value change.

def servo1_mode_select():
    bgs.set_pin_mode(2, servo1_mode.get(), servo1_output_value, w.slider_servo1_out)


def servo1_value_change(*args):
    bgs.slider_value_changed(2, servo1_mode.get(), int(args[0]))


def servo2_mode_select():
    bgs.set_pin_mode(3, servo2_mode.get(), servo2_output_value, w.slider_servo2_out)


def servo2_value_change(*args):
    bgs.slider_value_changed(3, servo2_mode.get(), int(args[0]))


def servo3_mode_select():
    bgs.set_pin_mode(4, servo3_mode.get(), servo3_output_value, w.slider_servo3_out)


def servo3_value_change(*args):
    bgs.slider_value_changed(4, servo3_mode.get(), int(args[0]))


def servo4_mode_select():
    bgs.set_pin_mode(5, servo4_mode.get(), servo4_output_value, w.slider_servo4_out)


def servo4_value_change(*args):
    bgs.slider_value_changed(5, servo4_mode.get(), int(args[0]))


def servo5_mode_select():
    bgs.set_pin_mode(6, servo5_mode.get(), servo5_output_value, w.slider_servo5_out)


def servo5_value_change(*args):
    bgs.slider_value_changed(6, servo5_mode.get(), int(args[0]))


def servo6_mode_select():
    bgs.set_pin_mode(7, servo6_mode.get(), servo6_output_value, w.slider_servo6_out)


def servo6_value_change(*args):
    bgs.slider_value_changed(7, servo6_mode.get(), int(args[0]))


def servo7_mode_select():
    bgs.set_pin_mode(8, servo7_mode.get(), servo7_output_value, w.slider_servo7_out)


def servo7_value_change(*args):
    bgs.slider_value_changed(8, servo7_mode.get(), int(args[0]))


def servo8_mode_select():
    bgs.set_pin_mode(9, servo8_mode.get(), servo8_output_value, w.slider_servo8_out)


def servo8_value_change(*args):
    bgs.slider_value_changed(9, servo8_mode.get(), int(args[0]))


def led_mode_select():
    # mode is limited to digital out
    mode = '1'
    bgs.set_pin_mode(13, led_mode.get(), led_output_value, w.slider_led_out)


def led_value_change(*args):
    bgs.slider_value_changed(13, led_mode.get(), int(args[0]))


def neopixel_mode_select():
    bgs.set_pin_mode(11, neopixel_mode.get(), neopixel_output_value, w.slider_neopixel_out)


def neopixel_value_change(*args):
    bgs.slider_value_changed(13, neopixel_mode.get(), int(args[0]))


def rcc1_mode_select():
    bgs.set_pin_mode(14, rcc1_mode.get(), rcc1_output_value, w.slider_rcc1_out)


def rcc1_value_change(*args):
    bgs.slider_value_changed(14, rcc1_mode.get(), int(args[0]))


def rcc2_mode_select():
    bgs.set_pin_mode(15, rcc2_mode.get(), rcc2_output_value, w.slider_rcc2_out)


def rcc2_value_change(*args):
    bgs.slider_value_changed(15, rcc2_mode.get(), int(args[0]))


def rcc3_mode_select():
    bgs.set_pin_mode(16, rcc3_mode.get(), rcc3_output_value, w.slider_rcc3_out)


def rcc3_value_change(*args):
    bgs.slider_value_changed(16, rcc3_mode.get(), int(args[0]))


def rcc4_mode_select():
    bgs.set_pin_mode(17, rcc4_mode.get(), rcc4_output_value, w.slider_rcc4_out)


def rcc4_value_change(*args):
    bgs.slider_value_changed(17, rcc4_mode.get(), int(args[0]))


# mpu start button pressed
# data will be continuously updated.
def mpu_start():
    payload = {'command': 'initialize_mpu'}
    bgs.publish_payload(payload, 'to_robohat_gateway')
    payload = {'command': 'read_mpu'}
    bgs.publish_payload(payload, 'to_robohat_gateway')


# ina start button pressed
# each parameter is queried separately.
def ina_read():
    payload = {'command': 'initialize_ina'}
    bgs.publish_payload(payload, 'to_robohat_gateway')

    payload = {'command': 'get_ina_bus_voltage'}
    bgs.publish_payload(payload, 'to_robohat_gateway')

    payload = {'command': 'get_ina_bus_current'}
    bgs.publish_payload(payload, 'to_robohat_gateway')

    payload = {'command': 'get_supply_voltage'}
    bgs.publish_payload(payload, 'to_robohat_gateway')

    payload = {'command': 'get_shunt_voltage'}
    bgs.publish_payload(payload, 'to_robohat_gateway')

    payload = {'command': 'get_power'}
    bgs.publish_payload(payload, 'to_robohat_gateway')


# start dht reporting
def dht_start():
    bgs.start_dht(dht1_Pin.get(), dht1_type.get())


# start sonar reporting
def read_sonar():
    bgs.start_sonar(triggerr_Pin.get(), echo_pin.get())


# noinspection PyGlobalUndefined,PyGlobalUndefined,PyUnresolvedReferences
def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None


# this is a custom class to interact with the GUI
class BanyanGuiSupport(BanyanBase):
    def __init__(self):
        # remote backplane address to connect to was specified.
        if len(sys.argv) > 1:
            super(BanyanGuiSupport, self).__init__(back_plane_ip_address=sys.argv[1])
        else:
            # use local backplane
            super(BanyanGuiSupport, self).__init__()

        # set the subscription topic
        self.set_subscriber_topic('from_robohat_gateway')

        # start the banyan message handler
        root.after(1000, self.get_message)

        # input modes
        self.pin_mode_command_map = {'1': 'set_mode_digital_output',
                                     '2': 'set_mode_pwm',
                                     '3': 'set_mode_servo',
                                     '4': 'set_mode_digital_input',
                                     '5': 'set_mode_digital_input_pullup',
                                     '6': 'set_mode_analog_input',
                                     '7': 'set_mode_dht',
                                     '8': 'set_mode_sonar'}
        # output value widgets
        self.input_value_map = [{'pin': 2, 'widget': servo1_in_value},
                                {'pin': 3, 'widget': servo2_in_value},
                                {'pin': 4, 'widget': servo3_in_value},
                                {'pin': 5, 'widget': servo4_in_value},
                                {'pin': 6, 'widget': servo5_in_value},
                                {'pin': 7, 'widget': servo6_in_value},
                                {'pin': 8, 'widget': servo7_in_value},
                                {'pin': 9, 'widget': servo8_in_value},
                                {'pin': 11, 'widget': neopixel_in_value},
                                {'pin': 14, 'widget': rcc1_in_value},
                                {'pin': 15, 'widget': rcc2_in_value},
                                {'pin': 16, 'widget': rcc3_in_value},
                                {'pin': 17, 'widget': rcc4_in_value},
                                ]

        self.pin_name_map = {'Servo 1': 2, 'Servo 2': 3, 'Servo 3': 4,
                             'Servo 4': 5, 'Servo 5': 6, 'Servo 6': 7,
                             'Servo 7': 8, 'Servo 8': 9, 'NeoPixel': 11,
                             'RCC 1': 14, 'RCC 2': 15, 'RCC 3': 16,
                             'RCC 4': 17
                             }

        self.pin_mode_variable_map = {'Servo 1': servo1_mode, 'Servo 2': servo2_mode,
                                      'Servo 3': servo3_mode, 'Servo 4': servo4_mode,
                                      'Servo 5': servo5_mode, 'Servo 6': servo6_mode,
                                      'Servo 7': servo7_mode, 'Servo 8': servo_mode,
                                      'NeoPixel': neopixel_mode,
                                      'RCC 1': rcc1_mode, 'RCC 2': rcc2_mode,
                                      'RCC 3': rcc3_mode, 'RCC 4': rcc4_mode
                                      }
        # need this to calculate Arduino type mapped pin numbers
        self.digital_to_analog_pin_map = {14: 0, 15: 1, 16: 2, 17: 3}

        # initialize pin numbers in dht and sonar tabs
        dht1_Pin.set('Servo 1')
        dht1_type.set('DHT 22')
        triggerr_Pin.set('Servo 1')
        echo_pin.set('Servo 2')

    def get_message(self):
        """
        This method is called from the tkevent loop "after" call.
        It will poll for new zeromq messages within the tkinter event loop.
        """
        try:
            # noinspection PyUnresolvedReferences
            data = self.subscriber.recv_multipart(zmq.NOBLOCK)
            self.incoming_message_processing(data[0].decode(),
                                             msgpack.unpackb(data[1],
                                                             raw=False))
            # call this method again
            root.after(1, self.get_message)

        except zmq.error.Again:
            try:
                # call this method again
                root.after(1, self.get_message)
            except KeyboardInterrupt:
                self.publisher.close()
                self.subscriber.close()
                self.context.term()
                root.destroy()
                sys.exit(0)
        except KeyboardInterrupt:
            root.destroy()
            self.publisher.close()
            self.subscriber.close()
            self.context.term()
            sys.exit(0)

    # process the messages received from the gateway
    def incoming_message_processing(self, topic, payload):
        if payload['report'] == 'mpu':

            acc_x.set(payload['Ax'])
            acc_y.set(payload['Ay'])
            acc_z.set(payload['Az'])

            gyro_x.set(payload['Gx'])
            gyro_y.set(payload['Gy'])
            gyro_z.set(payload['Gz'])

            mag_x.set(payload['Mx'])
            mag_y.set(payload['My'])
            mag_z.set(payload['Mz'])

            mpu_temp.set(payload['Temperature'])
            return

        elif payload['report'] == 'ina':
            value = payload['value']
            if payload['param'] == 'V':
                ina_bus_voltage.set(value)
            elif payload['param'] == 'A':
                ina_bus_current.set(value)
            elif payload['param'] == 'Supply':
                ina_supply_voltage.set(value)
            elif payload['param'] == 'Shunt':
                ina_shunt_voltage.set(value)
            elif payload['param'] == 'Power':
                ina_power.set(value)
            return

        elif payload['report'] == 'dht':
            dht1_humidity.set(payload['humidity'])
            dht1_temp.set(payload['temp'])
            return

        elif payload['report'] == 'sonar':
            sonar_distance.set(payload['distance'])
            return

        elif payload['report'] == 'analog_input':
            # readjust pin to digital pin number
            digital_pin = payload['pin'] + 14
            # set the output widget value for this pin
        elif payload['report'] == 'digital_input':
            digital_pin = payload['pin']
        # noinspection PyUnboundLocalVariable
        entry = next(item for item in self.input_value_map if item['pin'] == digital_pin)
        widget = entry['widget']
        # self.input_value_map[digital_pin].set(payload['value'])
        widget.set(payload['value'])

    def start_dht(self, pin, dht_type):
        # get the pin number based on the name
        digital_pin = self.pin_name_map[pin]
        # set pin mode for selected pin
        self.pin_mode_variable_map[pin].set('7')

        if type == 'DHT 11':
            dht_type = 11
        else:
            dht_type = 22
        payload = {'command': 'set_mode_dht', 'pin': digital_pin, 'type': dht_type}
        self.publish_payload(payload, 'to_robohat_gateway')

        payload = {'command': 'dht_read', 'pin': digital_pin}
        self.publish_payload(payload, 'to_robohat_gateway')

    def start_sonar(self, trigger, echo):
        self.pin_mode_variable_map[trigger].set('8')
        self.pin_mode_variable_map[echo].set('8')

        trigger = self.pin_name_map[trigger]
        echo = self.pin_name_map[echo]

        if trigger == echo:
            messagebox.showerror("Pin Selection Error", "Both Pins Cannot Be The Same!")
            return
        payload = {'command': 'set_mode_sonar', 'trigger': trigger, 'echo': echo}
        self.publish_payload(payload, 'to_robohat_gateway')

    # generalized method to set the pin modes
    def set_pin_mode(self, pin, mode, slider_value_variable, slider_control):
        if mode in self.pin_mode_command_map.keys():
            # digital out
            if mode == '1':
                # slider_value_variable.configure(to=1)
                slider_control.configure(to=1)
            elif mode == '2':
                slider_control.configure(to=255)
            elif mode == '3':
                slider_control.configure(to=180)
            # transform digital pin number to analog pin number
            elif mode == '6':
                pin = self.digital_to_analog_pin_map[pin]
            # build pin mode message and transmit it
            payload = {'command': self.pin_mode_command_map[mode], 'pin': int(pin)}
            self.publish_payload(payload, 'to_robohat_gateway')
        # output modes
        if mode in ['1', '2', '3']:
            value = int(slider_value_variable.get())
            self.slider_value_changed(pin, mode, value)

    def slider_value_changed(self, pin, mode, value):
        # digital output
        if mode == '1':
            self.write_digital_out(pin, value)
        # pwm
        elif mode == '2':
            self.write_pwm(pin, value)
        # servo
        elif mode == '3':
            self.set_servo_angle(pin, value)

    def write_digital_out(self, pin, value):
        payload = {'command': 'digital_write', 'pin': pin, 'value': value}
        self.publish_payload(payload, 'to_robohat_gateway')

    def write_pwm(self, pin, value):
        payload = {'command': 'pwm_write', 'pin': pin, 'value': value}
        self.publish_payload(payload, 'to_robohat_gateway')

    def set_servo_angle(self, pin, value):
        payload = {'command': 'servo_position', 'pin': pin, 'position': value}
        self.publish_payload(payload, 'to_robohat_gateway')


if __name__ == '__main__':
    import pymata_rh

    pymata_rh.vp_start_gui()
