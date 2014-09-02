import math
import os
import time

import serial

from Frame import Frame


class LightWriter(object):

    def __init__(self, port=None, baud=115200, timeout=1):
        if not port:
            possible_devices = [
                dev for dev in os.listdir('/dev/')
                if ('usb' in dev or 'ACM' in dev)
                and dev.startswith('tty')
            ]
            if len(possible_devices) == 1:
                device = possible_devices.pop()
            else:
                print "Possible devices:"
                print possible_devices
                device = raw_input("Please enter your usb device for the ardunio: ")
            port = os.path.join('/dev', device)
        self.port = port
        self.baud = baud
        self.timeout = timeout
        print "Initializing..."
        time.sleep(3)
        self.serial = serial.Serial(port, baud, timeout=timeout)
        print "USB connection established..."
        time.sleep(3)
        self._frame = Frame()
        self.write_frame()
        print "Lights reset"

    def write_frame(self, frame=None):
        if frame:
            self._frame = frame
        self.serial.write([255])
        for i in range(10):
            for j in range(4):
                if self._frame.data[i][j] >= 255:
                    self._frame.data[i][j] = 254
            self.serial.write(self._frame.data[i])

    def glow(self, color='green', length=2, period=1, interval=.05, brightness=100, **kwargs):
        steps = int(length / interval)
        half_max_brightness = brightness / 2
        for i in range(steps):
            brightness = half_max_brightness + half_max_brightness * math.cos(period/math.pi * i)
            self._frame.set_color_by_name(color)
            self._frame.set_brightness(brightness)
            self.write_frame()
            time.sleep(interval)

    def rotate(self, length=2, interval=.05, **kwargs):
        steps = int(length / interval)
        for i in range(steps):
            self._frame.shift(1)
            self.write_frame()
            time.sleep(interval)

    def back_and_forth(self, color='red', length=2, interval=.1, brightness=100,
                       background='black', **kwargs):
        self._frame.set_color_by_name(background)
        self._frame.set_color_by_name(color, node=9)
        self._frame.set_brightness(brightness, allow_zero=True)
        steps = int(length / interval)
        stepper = 1
        for i in range(steps):
            if not i % 10:
                stepper *= -1
                continue
            self._frame.shift(stepper)
            self.write_frame()
            time.sleep(interval)

    def random(self, length=2, interval=.1, brightness=100, **kwargs):
        steps = int(length / interval)
        for i in range(steps):
            self._frame.random()
            self._frame.set_brightness(brightness)
            self.write_frame()
            time.sleep(interval)

    def blink(self, color='white', length=2, interval=.3, brightness=100, **kwargs):
        steps = int(length / interval / 2)
        for i in range(steps):
            self._frame.set_color_by_name(color)
            self._frame.set_brightness(brightness)
            self.write_frame()
            time.sleep(interval)
            self._frame.set_color_by_name('black')
            self.write_frame()
            time.sleep(interval)

    def rise_and_fall(self, color='red', height=10, length=2, interval=.1,
                      background='blue', brightness=100, **kwargs):
        stepper = 1
        height_counter = 1
        steps = int(length / interval)
        for i in range(steps):
            self._frame.set_color_by_name(background)
            self._frame.set_brightness(brightness)
            self.set_height(color=color, height=height_counter, brightness=brightness)
            height_counter += stepper
            if height_counter == height or height_counter == 0:
                stepper = stepper * -1

            time.sleep(interval)

    def clear(self, **kwargs):
        self.write_frame(Frame())

    def wait(self, seconds=1, **kwargs):
        time.sleep(seconds)

    def set_height(self, color='blue', height=5, brightness=100, **kwargs):
        for i in range(height):
            self._frame.set_color_by_name(color, node=i)
        self._frame.set_brightness(brightness, allow_zero=True)
        self.write_frame()

    def frame_method(self, frame_method=None, write=True, *args, **kwargs):
        """Call a method from Frame on the current frame."""
        if frame_method:
            getattr(self._frame, frame_method)(*args, **kwargs)
            if write:
                self.write_frame()
