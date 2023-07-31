# Auto Maze

![Auto Maze Logo]([/path/to/logo.png](https://upload.wikimedia.org/wikipedia/commons/thumb/6/62/National-Oilwell-Varco-Logo.svg/1920px-National-Oilwell-Varco-Logo.svg.png))

## Description

The Auto Maze GUI is a graphical user interface designed to control and interact with an automated maze-solving system. The system uses an Arduino-based controller to manipulate actuators and sensors to navigate through mazes autonomously or under manual control.

The GUI offers three main modes of operation:
1. Manual Control: Allows the user to manually control the maze-solving system using an Xbox controller.
2. Auto Control: Enables the system to autonomously solve a detected maze using pre-defined maze-solving algorithms.
3. AI Control (Future Implementation): A mode that is currently under development, which will employ AI algorithms to optimize maze-solving strategies.

## Features

- User-friendly graphical interface.
- Manual control mode with Xbox controller support.
- Auto control mode for autonomous maze solving.
- AI control mode (in development).
- Override mode to manually control actuators from the GUI.
- Automatic maze detection and display of detected maze information.
- Quit button to close the application.

## Requirements

- Python 3.x
- tkinter
- customtkinter
- pySerialTransfer
- opencv-python (cv2)
- PIL (Python Imaging Library)

## Installation

1. Clone this repository to your local machine.
2. Install the required libraries using pip:
3. Connect the Arduino-based controller to the serial port specified in the GUI code (`serial_port = "/dev/ttyACM0"`). Make sure the controller is properly configured and communicating. (This is on linux, different on windows or mac)

## Usage

1. Run the GUI application:
2. Upon startup, the main menu will be displayed, showing three buttons: "Manual," "Auto," and "AI" (currently not implemented). Click on the desired button to select the mode of operation.
3. In "Manual" mode, the Xbox controller should be connected to the system to control the maze-solving system manually.
4. In "Auto" mode, the system will automatically detect a maze (if present) and display the detected maze information. Click the "Run Auto Control" button to start the autonomous maze-solving process.
5. In "AI" mode (currently not implemented), AI algorithms will be used to optimize maze-solving strategies.
6. The "Override" button allows manual control of actuators from the GUI, regardless of the Xbox controller's presence.
7. The "MazeSolutions" folder contains text files with solutions fore the different mazes, so they are always saved there. But if you would like to make a new solution or make other mazes, you can use the "WriteToFileWithTimestamp.py" program to make new solutions.

## Known Issues

- The AI mode is not yet implemented.
- It won't always start a connection with the Xbox controller when going into manual control
- When clicking "the return to menu" button in manual control, then it won't go back befor after getting an input from the Xbox controller
- The GUI can open with wrong graphics
- The sensor is not perfectly calibrated, this can lead to the elevator going of or not go of when it is suppose to it(happen less then 1 prosent of the time).

## Contributors

- Vebjørn Lyngstad
- Daniel Kokai
- Simon Chabab
- Emil Dien Tran
- Lise Valvik
- Jakob Finnvold

## License

This project is licensed under the MIT License. See the [LICENSE](/path/to/LICENSE) file for details.

## Acknowledgments

Special thanks to the NOV organization for supporting this project.
