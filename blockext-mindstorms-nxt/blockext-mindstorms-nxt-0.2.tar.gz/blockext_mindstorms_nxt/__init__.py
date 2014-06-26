from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from future.builtins import *

import blockext
from blockext import needs_connection, get_blocks_from_class
from blockext import command, reporter, predicate

import threading
import time

import nxt
from nxt.motor import *
from nxt.sensor import *
from nxt.sensor.hitechnic import *
try:
    from usb import USBError
except ImportError:
    USBError = None

__version__ = '0.2'



class MindstormsNXT(object):
    def __init__(self):
        self.brick = None
        self.last_ping = 0
        self.needs_reset = False

        self.sensor_types = {
            'port 1': None,
            'port 2': None,
            'port 3': None,
            'port 4': None,
        }
        self.sensors = {
            'port 1': None,
            'port 2': None,
            'port 3': None,
            'port 4': None,
        }

    def _is_connected(self):
        if self.brick:
            # Ping the brick.
            # Do this by trying a boring command (battery level)
            try:
                self.brick.get_battery_level()
            except USBError:
                self.disconnected()
            self.last_ping = time.time()

        if not self.brick:
            try:
                self.brick = nxt.locator.find_one_brick(silent=True)
            except nxt.locator.BrickNotFoundError:
                pass
            else:
                self.connected()

        return bool(self.brick)

    def _problem(self):
        if not self.brick:
            return "The Mindstorms brick is not connected."

    def _on_reset(self):
        for port in self.sensors:
            self.sensors[port] = None
        if self.brick:
            self.reset_motors()
        else:
            self.needs_reset = True
            # We'll reset motors when the brick is reconnected

    def reset_motors(self):
        print('reset')
        for port in PORT_A, PORT_B, PORT_C:
            Motor(self.brick, port).reset_position(False)
            Motor(self.brick, port).idle() # TODO how best to stop?

    def disconnected(self):
        print("Disconnected")

        self.brick = None
        for port in self.sensors:
            self.sensors[port] = None

    def connected(self):
        print("Connected")

        # Re-create sensors
        for port, cls in self.sensor_types.items():
            if cls:
                self.make_sensor(port)

        # Stop motors if a reset command was sent while disconnected
        if self.needs_reset:
            self.reset_motors()
            self.needs_reset = False

    def make_sensor(self, port):
        cls = self.sensor_types[port]
        self.sensors[port] = cls(self.brick, port_menu[port])

    # Motors

    def get_motor(self, motor):
        ports = motor_menu[motor]
        if len(ports) == 1:
            return Motor(self.brick, ports[0])
        else:
            return SynchronizedMotors(Motor(self.brick, ports[0]),
                                      Motor(self.brick, ports[1]), 1)

    @command('turn %m.nxtMotor by %n degrees at %n% power', is_blocking=True)
    @needs_connection
    def turn_degrees(self, motor='motor A', degrees=360, power=100):
        if degrees < 0:
            power *= -1
        power = min(max(power, -100), 100)
        self.get_motor(motor).turn(power, abs(degrees))

    @command('turn %m.nxtMotor at %n% power')
    @needs_connection
    def turn(self, motor='motor A', power=100):
        power = min(max(power, -100), 100)
        self.get_motor(motor).run(power)

    @command('brake %m.nxtMotor')
    @needs_connection
    def brake(self, motor='motor A'):
        self.get_motor(motor).brake()

    @reporter('rotation of %m.nxtRotation')
    @needs_connection
    def motor_rotation(self, motor='motor A'):
        motor = Motor(self.brick, rotation_menu[motor])
        return motor.get_tacho().rotation_count

    # Sensors

    @command("attach %m.nxtSensor sensor to %m.nxtPort")
    def attach_sensor(self, sensor_type='touch', port='port 1'):
        cls = sensor_menu[sensor_type]
        if self.sensor_types[port] != cls:
            self.sensor_types[port] = cls
            if self.brick:
                self.make_sensor(port)

    @command('switch %m.onoff light on %m.nxtPort')
    @needs_connection
    def illuminate(self, onoff='on', port='port 1'):
        # Not sure which is more confusing:
        # - having to "attach" the sensor first to be able to switch it on and off
        # - having to "attach" the sensor to read its value, but not to switch it
        #   on and off -- that's just inconsistent!

        # Use the existing sensor object if we can, otherwise a temporary one
        sensor = self.sensors[port]
        if not sensor or not isinstance(sensor, Light):
            sensor = Light(brick, port_menu[port])
        sensor.set_illuminated(onoff_menu[onoff])

    @reporter('%m.nxtReporter sensor on %m.nxtPort')
    @needs_connection
    def report_sensor(self, sensor_type='distance', port='port 4'):
        sensor = self.sensors[port]
        if sensor and isinstance(sensor, sensor_menu[sensor_type]):
            return sensor.get_sample()

    @predicate('touch sensor on %m.nxtPort')
    @needs_connection
    def touch_sensor(self, port='port 1'):
        sensor = self.sensors[port]
        if sensor and isinstance(sensor, Touch):
            return sensor.get_sample()

    # Misc

    @command('play tone %d.note for %n seconds', is_blocking=True)
    @needs_connection
    def tone(self, note=60, time=1):
        tone = 440 * 1.059463094359 ** (float(note) - 69)
        print(tone)
        self.brick.play_tone_and_wait(tone, time * 1000)


onoff_menu = {
    'on': True,
    'off': False
}
rotation_menu = {
    'motor A': PORT_A,
    'motor B': PORT_B,
    'motor C': PORT_C
}
motor_menu = {
    'motor A': (PORT_A,),
    'motor B': (PORT_B,),
    'motor C': (PORT_C,),
    'motor A and B': (PORT_A, PORT_B),
    'motor A and C': (PORT_A, PORT_C),
    'motor B and C': (PORT_B, PORT_C)
}
port_menu = {
    'port 1': PORT_1,
    'port 2': PORT_2,
    'port 3': PORT_3,
    'port 4': PORT_4
}
sensor_menu = {
    'light': Light,
    'sound': Sound,
    'distance': Ultrasonic,
    'touch': Touch,
    #'hitechnic compass': Compass,
}
reporter_menu = {
    'light': Light,
    'sound': Sound,
    'distance': Ultrasonic,
    #'compass': Compass,
}


descriptor = blockext.Descriptor(
    name = "Lego Mindstorms NXT",
    port = 1331,
    blocks = get_blocks_from_class(MindstormsNXT),
    menus = dict(
        onoff = ['on', 'off'],
        nxtRotation = sorted(rotation_menu.keys()),
        nxtMotor = ['motor A', 'motor B', 'motor C', 'motor A and B',
                    'motor A and C', 'motor B and C'],
        nxtPort = sorted(port_menu.keys()),
        nxtSensor = sorted(sensor_menu.keys()),
        nxtReporter = sorted(reporter_menu.keys()),
        note = [84, 83, 81, 79, 77, 76, 74, 72, 71, 69, 67, 65, 64, 62, 60, 57],
    ),
)

extension = blockext.Extension(MindstormsNXT, descriptor)

if __name__ == '__main__':
    extension.run_forever(debug=True)

