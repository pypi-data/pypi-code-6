import RPi.GPIO as GPIO
import time

class DAC16:
    
    def __init__(self, SYNCpin, SCLKpin, DINpin):
        self.SYNCpin = SYNCpin
        self.SCLKpin = SCLKpin
        self.DINpin = DINpin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(SYNCpin, GPIO.OUT)
        GPIO.setup(SCLKpin, GPIO.OUT)
        GPIO.setup(DINpin, GPIO.OUT)
        self.clock(GPIO.HIGH)

    def clock(self, highLow):
        GPIO.output(self.SCLKpin, highLow)
        time.sleep(0.0000001)

    def write(self, dacValue):
        GPIO.output(self.SYNCpin, GPIO.HIGH)
        GPIO.output(self.SYNCpin, GPIO.LOW)
        for i in range(23, -1, -1):
            GPIO.output(self.DINpin, (dacValue >> i) & 1)
            self.clock(GPIO.LOW)
            self.clock(GPIO.HIGH)
