#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 5.4
#  in conjunction with Tcl version 8.6
#    Aug 22, 2020 07:56:29 PM EDT  platform: Linux
#    Aug 23, 2020 09:50:15 AM EDT  platform: Linux
#    Aug 23, 2020 10:26:02 AM EDT  platform: Linux
#    Aug 23, 2020 10:35:53 AM EDT  platform: Linux
#    Aug 23, 2020 10:55:41 AM EDT  platform: Linux
#    Aug 23, 2020 11:52:39 AM EDT  platform: Linux
#    Aug 23, 2020 01:27:19 PM EDT  platform: Linux
#    Aug 23, 2020 01:32:01 PM EDT  platform: Linux
#    Aug 23, 2020 01:46:51 PM EDT  platform: Linux
#    Aug 23, 2020 03:33:05 PM EDT  platform: Linux
#    Aug 23, 2020 03:44:20 PM EDT  platform: Linux
#    Aug 23, 2020 03:45:05 PM EDT  platform: Linux
#    Aug 23, 2020 04:20:00 PM EDT  platform: Linux
#    Aug 23, 2020 04:30:56 PM EDT  platform: Linux
#    Aug 24, 2020 06:51:01 PM EDT  platform: Linux
#    Aug 24, 2020 06:58:00 PM EDT  platform: Linux
#    Aug 25, 2020 07:56:00 AM EDT  platform: Linux

import sys
from python_banyan.banyan_base import BanyanBase

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

def set_Tk_var():
    global dummy
    dummy = tk.StringVar()
    global ina_bus_current
    ina_bus_current = tk.StringVar()
    global ina_bus_voltage
    ina_bus_voltage = tk.StringVar()
    global ina_shunt_voltage
    ina_shunt_voltage = tk.StringVar()
    global ina_supply_voltage
    ina_supply_voltage = tk.StringVar()
    global ina_power
    ina_power = tk.StringVar()
    global mpu_temp
    mpu_temp = tk.StringVar()
    global gyro_x
    gyro_x = tk.StringVar()
    global gyro_y
    gyro_y = tk.StringVar()
    global gyro_z
    gyro_z = tk.StringVar()
    global mag_x
    mag_x = tk.StringVar()
    global mag_y
    mag_y = tk.StringVar()
    global mag_z
    mag_z = tk.StringVar()
    global acc_x
    acc_x = tk.StringVar()
    global acc_y
    acc_y = tk.StringVar()
    global acc_z
    acc_z = tk.StringVar()
    global triggerr_Pin
    triggerr_Pin = tk.StringVar()
    global echo_pin
    echo_pin = tk.StringVar()
    global sonar_distance
    sonar_distance = tk.StringVar()
    global dht1_Pin
    dht1_Pin = tk.StringVar()
    global dht1_type
    dht1_type = tk.StringVar()
    global dht1_humidity
    dht1_humidity = tk.StringVar()
    global dht1_temp
    dht1_temp = tk.StringVar()
    global dht2_Pin
    dht2_Pin = tk.StringVar()
    global dht2_type
    dht2_type = tk.StringVar()
    global dht2_humidity
    dht2_humidity = tk.StringVar()
    global dht2_temp
    dht2_temp = tk.StringVar()
    global dht1_combobox
    dht1_combobox = tk.StringVar()
    global combobox
    combobox = tk.StringVar()
    global rcc1_in_value
    rcc1_in_value = tk.StringVar()
    global rcc2_in_value
    rcc2_in_value = tk.StringVar()
    global rcc3_in_value
    rcc3_in_value = tk.StringVar()
    global rcc4_in_value
    rcc4_in_value = tk.StringVar()
    global neopixel_in_value
    neopixel_in_value = tk.StringVar()
    global servo_1mode
    servo_1mode = tk.StringVar()
    global servo3_in_value
    servo3_in_value = tk.StringVar()
    global servo4_in_value
    servo4_in_value = tk.StringVar()
    global servo5_in_value
    servo5_in_value = tk.StringVar()
    global servo6_in_value
    servo6_in_value = tk.StringVar()
    global servo7_in_value
    servo7_in_value = tk.StringVar()
    global servo8_in_value
    servo8_in_value = tk.StringVar()
    global servo2_in_value
    servo2_in_value = tk.StringVar()
    global servo_mode
    servo_mode = tk.StringVar()
    global servo1_in_value
    servo1_in_value = tk.StringVar()
    global rcc1_output_value
    rcc1_output_value = tk.DoubleVar()
    global rcc1_mode
    rcc1_mode = tk.StringVar()
    global rcc2_output_value
    rcc2_output_value = tk.DoubleVar()
    global rcc2_mode
    rcc2_mode = tk.StringVar()
    global rcc3_output_value
    rcc3_output_value = tk.DoubleVar()
    global rcc3_mode
    rcc3_mode = tk.StringVar()
    global rcc4_output_value
    rcc4_output_value = tk.DoubleVar()
    global rcc4_mode
    rcc4_mode = tk.StringVar()
    global neopixel_output_value
    neopixel_output_value = tk.DoubleVar()
    global neopixel_mode
    neopixel_mode = tk.StringVar()
    global led_output_value
    led_output_value = tk.DoubleVar()
    global led_mode
    led_mode = tk.StringVar()
    global servo1_output_value
    servo1_output_value = tk.DoubleVar()
    global servo1_mode
    servo1_mode = tk.StringVar()
    global servo2_output_value
    servo2_output_value = tk.DoubleVar()
    global servo2_mode
    servo2_mode = tk.StringVar()
    global servo3_output_value
    servo3_output_value = tk.DoubleVar()
    global servo3_mode
    servo3_mode = tk.StringVar()
    global servo4_output_value
    servo4_output_value = tk.DoubleVar()
    global servo4_mode
    servo4_mode = tk.StringVar()
    global servo5_output_value
    servo5_output_value = tk.DoubleVar()
    global servo5_mode
    servo5_mode = tk.StringVar()
    global servo6_output_value
    servo6_output_value = tk.DoubleVar()
    global servo6_mode
    servo6_mode = tk.StringVar()
    global servo7_output_value
    servo7_output_value = tk.DoubleVar()
    global servo7_mode
    servo7_mode = tk.StringVar()
    global servo8_output_value
    servo8_output_value = tk.DoubleVar()
    global servo8_mode
    servo8_mode = tk.StringVar()

def init(top, gui, *args, **kwargs):
    global w, top_level, root, bgs
    w = gui
    top_level = top
    root = top
    bgs = BanyanGuiSupport()

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


def mpu_start():
    print('pymata_rh_support.mpu_start')
    sys.stdout.flush()

def mpu_stop():
    print('pymata_rh_support.mpu_stop')
    sys.stdout.flush()

def ina_read():
    print('pymata_rh_support.ina_read')
    sys.stdout.flush()

def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None

class BanyanGuiSupport(BanyanBase):
    def __init__(self):
        if len(sys.argv) > 1:
            super(BanyanGuiSupport, self).__init__(back_plane_ip_address=sys.argv[1])
        else:
            super(BanyanGuiSupport, self).__init__()
        self.set_subscriber_topic('from_robohat_gateway')
        root.after(1000, self.incoming)
        self.pin_mode_command_map = {'1': 'set_mode_digital_output',
                                     '2': 'set_mode_pwm',
                                     '3': 'set_mode_servo',
                                     '4': 'set_mode_digital_input',
                                     '5': 'set_mode_digital_input_pullup',
                                     '6': 'set_mode_analog_input',
                                     '7': 'set_mode_dht',
                                     '8': 'set_mode_sonar'}

    def incoming(self):
        print('incoming')
        root.after(1000, self.incoming)

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
            # build pin mode message and transmit it
            payload = {'command': self.pin_mode_command_map[mode], 'pin': int(pin)}
            # print(payload)
            self.publish_payload(payload, 'to_robohat_gateway')
            print('s')
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




