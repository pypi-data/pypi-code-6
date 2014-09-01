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

    def _write(self, data):
        self.serial.write(data)

    def set_frame(self, frame):
        self._frame = frame

    def write_frame(self, frame=None):
        self._frame_check(frame)
        self.serial.write([255])
        for i in range(10):
            for j in range(4):
                if self._frame.data[i][j] >= 255:
                    self._frame.data[i][j] = 254
            self.serial.write(self._frame.data[i])

    def _frame_check(self, frame):
        if not frame and not self._frame:
            raise AttributeError('Frame required!')
        if frame:
            self.set_frame(frame)

    def glow(self, color='green', length=20, period=1, interval=.05, frame=None, **kwargs):
        self._frame_check(frame)
        steps = int(length / interval)
        for i in range(steps):
            brightness = 50 + 50 * math.cos(period/math.pi * i)
            self._frame.set_color_by_name(color)
            self._frame.set_brightness(brightness)
            self.write_frame()
            time.sleep(interval)

    def rotate(self, length=20, interval=.05, frame=None, **kwargs):
        self._frame_check(frame)
        steps = int(length / interval)
        for i in range(steps):
            self._frame.shift(1)
            self.write_frame()
            time.sleep(interval)

    def back_and_forth(self, length=20, interval=.05, frame=None, **kwargs):
        self._frame_check(frame)
        steps = int(length / interval)
        stepper = 1
        for i in range(steps):
            if not i % 10:
                stepper *= -1
                continue
            self._frame.shift(stepper)
            self.write_frame()
            time.sleep(interval)

    def random(self, length=20, interval=.1, frame=None):
        self._frame_check(frame)
        steps = int(length / interval)
        for i in range(steps):
            self._frame.random()
            self.write_frame()
            time.sleep(interval)

    def blink(self, color='white', length=5, interval=.3, frame=None):
        self._frame_check(frame)
        steps = int(length / interval / 2)
        for i in range(steps):
            self._frame.set_color_by_name(color)
            self.write_frame()
            time.sleep(interval)
            self._frame.set_color_by_name('black')
            self.write_frame()
            time.sleep(interval)

    def rise_and_fall(self, color='red', height=10, length=5, interval=.3,
                      background='blue', frame=None):
        self._frame_check(frame)
        stepper = 1
        height_counter = 1
        steps = int(length / interval)
        for i in range(steps):
            self._frame.set_color_by_name(background)
            self._frame.set_height(color, height_counter)
            self.write_frame()
            height_counter += stepper
            if height_counter == height or height_counter == 0:
                stepper = stepper * -1

            time.sleep(interval)

    def clear(self):
        self.write_frame(Frame())

    def wait(self, seconds):
        time.sleep(seconds)

    def frame_method(self, method, *args, **kwargs):
        """Call a frame method on the current frame."""
        self._frame_check(None)
        getattr(self._frame, method)(*args, **kwargs)
        self.write_frame()
