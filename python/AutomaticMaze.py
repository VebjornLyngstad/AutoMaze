import serial
import time
import cv2
from MazeDetector import MazeDetector

class AutomaticMaze:
    # Initialize AutomaticMaze with the specified serial port for Arduino communication
    def __init__(self, serial_port):
        self.serial_port = serial_port
        self.ser = None

    # Connect to the Arduino via serial communication
    def connect(self, baud_rate=115200, timeout=2):
        self.ser = serial.Serial(self.serial_port, baud_rate)
        self.ser.flush()
        time.sleep(timeout)

    # Disconnect from the Arduino
    def disconnect(self):
        if self.ser:
            self.ser.close()

    # Send data to the Arduino from a file
    def send_data_from_file(self, file_path):
        with open(file_path, "r") as file:
            lines = file.readlines()

        if self.ser:
            num2 = 0.01
            for line in lines:
                parts = line.strip().split()
                if len(parts) == 2:
                    time.sleep(num2)
                    num1 = int(parts[0])
                    num2 = float(parts[1])
                    self.ser.write(str(num1).encode())
                    self.ser.read_all()

    # Create an instance of AutomaticMaze, connect to Arduino, send data, and disconnect
    @classmethod
    def from_file(cls, serial_port, maze_name, baud_rate=115200):
        maze = cls(serial_port)
        maze.connect(baud_rate)

        # Determine the file path based on the detected maze name
        file_path = f"{maze_name}.txt"

        maze.send_data_from_file(file_path)
        maze.disconnect()

#End of AutomaticMaze class

# Example usage:
'''
if __name__ == "__main__":
   serial_port = "/dev/ttyACM0"  # Replace with your Arduino's serial port

    maze_detector = MazeDetector()
    detected_maze = None

    # Continuously detect the maze until found
    while detected_maze is None:
        detected_maze = maze_detector.detect_maze()

    maze_detector.release()  # Release the video capture

    AutomaticMaze.from_file(serial_port, detected_maze)

    if detected_maze:
        print(f"Maze detected: {detected_maze}")
'''

