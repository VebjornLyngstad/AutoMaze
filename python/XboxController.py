import os
import struct
import array
from fcntl import ioctl
import serial
import time
import threading

class XboxController:
    def __init__(self, serial_port="/dev/ttyACM0", joystick_device="/dev/input/js1"):
        # Initialize the XboxController class with default serial and joystick device paths
        self.serial_port = serial_port
        self.joystick_device = joystick_device
        self.ser = serial.Serial(self.serial_port, 115200)
        self.ser.flush()
        self.axis_states = {}
        self.button_states = {}
        self.axis_map = []
        self.button_map = []
        self.jsdev = None
        
        # Mapping of axis and button IDs to their respective names
        self.axis_names = {
            0x00: 'x',
            0x01: 'y',
            0x02: 'z',
            0x03: 'rx',
            0x04: 'ry',
            0x05: 'rz',
            0x06: 'throttle',
            0x07: 'rudder',
            0x08: 'wheel',
            0x09: 'gas',
            0x0a: 'brake',
            0x10: 'hat0x',
            0x11: 'hat0y',
            0x12: 'hat1x',
            0x13: 'hat1y',
            0x14: 'hat2x',
            0x15: 'hat2y',
            0x16: 'hat3x',
            0x17: 'hat3y',
            0x18: 'pressure',
            0x19: 'distance',
            0x1a: 'tilt_x',
            0x1b: 'tilt_y',
            0x1c: 'tool_width',
            0x20: 'volume',
            0x28: 'misc',
        }

        self.button_names = {
            0x120: 'trigger',
            0x121: 'thumb',
            0x122: 'thumb2',
            0x123: 'top',
            0x124: 'top2',
            0x125: 'pinkie',
            0x126: 'base',
            0x127: 'base2',
            0x128: 'base3',
            0x129: 'base4',
            0x12a: 'base5',
            0x12b: 'base6',
            0x12f: 'dead',
            0x130: 'a',
            0x131: 'b',
            0x132: 'c',
            0x133: 'x',
            0x134: 'y',
            0x135: 'z',
            0x136: 'tl',
            0x137: 'tr',
            0x138: 'tl2',
            0x139: 'tr2',
            0x13a: 'select',
            0x13b: 'start',
            0x13c: 'mode',
            0x13d: 'thumbl',
            0x13e: 'thumbr',
            0x220: 'dpad_up',
            0x221: 'dpad_down',
            0x222: 'dpad_left',
            0x223: 'dpad_right',
        }

        self.running = False
        self.thread = None

    def find_xbox_controller(self):
        #print('Devices available')
        # Helper method to find available joystick devices in /dev/input
        for fn in os.listdir('/dev/input'):
            if fn.startswith('js'):
                print('/dev/input/%s' % fn)

    def open_joystick_device(self):
        try:
            # Open the joystick device for reading input events
            self.jsdev = open(self.joystick_device, 'rb')
        except:
            # If the joystick device is not found, handle the error
            print("Could not find Xbox controller. Please turn it on.")

    # Get the number of axes supported by the joystick device
    def get_num_axes(self):
        buf = array.array('B', [0])
        ioctl(self.jsdev, 0x80016a11, buf)  # JSIOCGAXES
        return buf[0]

    # Get the number of buttons supported by the joystick device
    def get_num_buttons(self):
        buf = array.array('B', [0])
        ioctl(self.jsdev, 0x80016a12, buf)  # JSIOCGBUTTONS
        return buf[0]

    # Read and process input events from the joystick device
    def read_controller_state(self):
        evbuf = self.jsdev.read(8)
        if evbuf:
            time1, value, ev_type, number = struct.unpack('IhBB', evbuf)
            if ev_type & 0x01:
                button = self.button_map[number]
                if number == 0:
                    #print("Button A")
                    self.ser.write(str(1000.00).encode())
                elif number == 1:
                    #print("Button B")
                    self.ser.write(str(2000.00).encode())
            if ev_type & 0x02:
                # Axis event
                axis = self.axis_map[number]
                if number == 1:
                    # Left joystick Y-axis
                    fvalue = int((value / 32767) * 100 - 200)
                    self.ser.write(str(fvalue).encode())
                    self.ser.read_all()
                    self.axis_states[axis] = fvalue
                    #print("%s: %.3f" % (axis, fvalue))
                elif number == 0:  # Change to 0 if only left joystick, change to 2 if right joystick as well
                    # Left joystick X-axis
                    fvalue = int((value / 32767) * 100 - 700)
                    self.ser.write(str(fvalue).encode())
                    self.ser.read_all()
                    self.axis_states[axis] = fvalue
                    #print("%s: %.3f" % (axis, fvalue))

    # Setup the joystick device and map axes and buttons
    def setup_joystick(self):
        self.find_xbox_controller()
        print('Opening %s ...' % self.joystick_device)
        self.open_joystick_device()
        num_axes = self.get_num_axes()
        num_buttons = self.get_num_buttons()
        buf = array.array('B', [0] * 0x40)
        ioctl(self.jsdev, 0x80406a32, buf)  # JSIOCGNAME(len)
        for axis in buf[:num_axes]:
            axis_name = self.axis_names.get(axis, 'unknown(0x%02x)' % axis)
            self.axis_map.append(axis_name)
            self.axis_states[axis_name] = 0.0
        for btn in buf[:num_buttons]:
            btn_name = self.button_names.get(btn, 'unknown(0x%03x)' % btn)
            self.button_map.append(btn_name)
            self.button_states[btn_name] = 0

    # Start reading input from the joystick in a separate thread
    def start(self):
            self.running = True
            self.thread = threading.Thread(target=self._run)
            self.thread.start()

    # Stop reading input from the joystick and wait for the thread to finish so this can end thread
    def stop(self):
        self.running = False
        self.thread.join()

    # The main loop for reading and processing input events
    def _run(self):
        self.setup_joystick()
        while self.running:
            self.read_controller_state() 

# End of XboxController class