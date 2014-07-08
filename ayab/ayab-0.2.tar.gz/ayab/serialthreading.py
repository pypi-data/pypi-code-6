import serial
import threading
import time

global connected
connected = False
port = '/dev/ttyACM0'
baud = 115200

serial_port = serial.Serial(port, baud, timeout=0)

def handle_data(data):
    print(data)

def read_from_port(ser):
    global connected
    while not connected:
        #serin = ser.read()
        connected = True

        #while True:
        for i in range(10):
           #print("test")
           ser.write("help\n\r")
           reading = ser.readline().decode()
           handle_data(reading)
           time.sleep(1)
           print i

thread = threading.Thread(target=read_from_port, args=(serial_port,))
thread.start()
thread.join()
