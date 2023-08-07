import os, struct, array
from fcntl import ioctl

import serial
import sys
import time

f = open("Maze 3.txt", "w")

print('Devices available')

for fn in os.listdir('/dev/input'):
    if fn.startswith('js'):
        print(' /dev/input/%s' % (fn))

serialPort = "/dev/ttyACM0" 
ser = serial.Serial(serialPort, 115200)
ser.flush()

axis_states = {}
button_states = {}
axis_names = {}
axis_map = []



fn = '/dev/input/js1'
print('Opening %s ...' % fn)
try: 
    jsdev = open(fn, 'rb')
except: 
    print("Could not find Xbox controller, please turn on")

buf = array.array('B', [0])  # Getting number of axes
ioctl(jsdev, 0x80016a11, buf)
num_axes = buf[0]

buf = array.array('B', [0])
ioctl(jsdev, 0x80016a12, buf)  # JSIOCGBUTTONS
num_buttons = buf[0]

buf = array.array('B', [0] * 0x40)
ioctl(jsdev, 0x80406a32, buf)

for axis in buf[:num_axes]:
    axis_name = axis_names.get(axis, 'unknown(0x%02x)' % axis)
    axis_map.append(axis_name)
    axis_states[axis_name] = 0.0

prev_time = time.time()  # Initialize previous time variable

while True:
    f = open("Maze 3.txt", "a")
    evbuf = jsdev.read(8)

    if evbuf:
        time1, value, ev_type, number = struct.unpack('IhBB', evbuf)

        if ev_type & 0x02:
            axis = axis_map[number]

            if number == 1:
                fvalue = int((value / 32767) * 100 - 200)
                ser.write(str(fvalue).encode())
                ser.read_all()
                axis_states[axis] = fvalue
                print("%s: %.3f" % (axis, fvalue))

            elif number == 0:
                fvalue = int((value / 32767) * 100 - 700)
                ser.write(str(fvalue).encode())
                ser.read_all()
                axis_states[axis] = fvalue
                print("%s: %.3f" % (axis, fvalue))

            curr_time = time.time()  # Get current time
            time_diff = curr_time - prev_time  # Calculate time difference
            print("Time between inputs: %.3f seconds" % time_diff)
            prev_time = curr_time  # Update previous time

            f.write(f"{fvalue} {time_diff}\n")  #Writing to file, Format:  actuator_possition (space) time_diff

    f.close()
