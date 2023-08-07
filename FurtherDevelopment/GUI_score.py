# Importing necessary libraries
import tkinter as tk
import customtkinter as ctk
from PIL import ImageTk, Image

import serial
import sys
import time
from pySerialTransfer import pySerialTransfer as txfer
import cv2

from XboxController import XboxController
from AutomaticMaze import AutomaticMaze
from MazeDetector import MazeDetector

# Global variable to track the state of button_2 (used for switching frames, and to stop the program running in button_2)
global button_2
button_2 = False

#New serial communication
#time.sleep(7) #Give it time to connect to serial communication when starting the program on boot
serialPort = "/dev/ttyACM0"
ser = serial.Serial(serialPort, 115200)  
ser.flush()

#Setting themes for the window
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

#Defining the main window
window = ctk.CTk()
window.geometry("800x480")
window.title("Auto Maze Project")

title = ctk.CTkLabel(window,
                    text="Welcome to the AutoMaze", 
                    font=("Arial", 60, "bold"),  
                    text_color = "white", 
                    )
title.pack()

#Adding NOV logo to the window
IMAGE_WIDTH = 180
IMAGE_HEIGHT = 90
IMAGE_PATH = '/home/maze/Desktop/Maze_Project/Code/images/nov.png'
nov_image = ctk.CTkImage(light_image=Image.open((IMAGE_PATH)), size=(IMAGE_WIDTH , IMAGE_HEIGHT))
label = ctk.CTkLabel(master = window, image = nov_image, text = "")
label.pack()
#label.place(relx = 0.5, rely = 0.8)



#Frame (This is the main Frame for the main menu)
frame = ctk.CTkFrame(master = window, width = 800, height = 480, fg_color = "transparent")
frame.pack()

#making new frame called "maze", defining hide and show functions for the original frame. Used to hide original frame and show the new frame. Used in button3_function later. 
maze = ctk.CTkFrame(master = window, width = 800,height = 480, fg_color = "transparent")

#Making new frame called "manual"
manual = ctk.CTkFrame(master = window, width = 800, height = 480, fg_color = "transparent")

#Making a new frame called "override", used for the override function with sliders and a button
override = ctk.CTkFrame(master = window, width = 800, height = 480, fg_color = "transparent")

scoreboard = ctk.CTkFrame(master=window, width=800, height=480, fg_color="transparent")
Maze1Score = ctk.CTkFrame(master=window, width=800, height=480, fg_color="transparent")
Maze2Score = ctk.CTkFrame(master=window, width=800, height=480, fg_color="transparent")
Maze3Score = ctk.CTkFrame(master=window, width=800, height=480, fg_color="transparent")

#Definging functions to hide and show the main frame "frame"
def hide_frame():
    frame.pack_forget()
    title.pack_forget()
    label.pack_forget()

def show_frame():
    #title = ctk.CTkLabel(window,
    #            text="Welcome to the auto Maze", 
    #            font=("Arial", 35, "bold"),  
    #            text_color = "white", 
    #           )   
    title.pack()
    label.pack()
    frame.pack()

def quit_application():
    window.destroy()

#Adding the images to the "buttons"
add_gameController_image = ctk.CTkImage(light_image=Image.open("/home/maze/Desktop/Maze_Project/Code/images/Game.png"),
                                        size = (100,100)
                                        )
add_maze_image = ctk.CTkImage(light_image=Image.open("/home/maze/Desktop/Maze_Project/Code/images/maze.png"),
                                size=(100,100)
                                )


controller = XboxController()    

#Defining functions for the return buttons in the different frames
def return_function_maze():
    maze.pack_forget()
    dynamic_text.place_forget()
    global button_2
    button_2 = False
    show_frame()

def return_function_manual():
    manual.pack_forget()
    show_frame()
    controller.stop()

def return_function_override():
    override.pack_forget()
    show_frame()

def return_function_scoreboard():
    scoreboard.pack_forget()
    show_frame()

def return_function_Maze1Score():
    Maze1Score.pack_forget()
    scoreboard.pack()  

def return_function_Maze2Score():
    Maze2Score.pack_forget()
    scoreboard.pack()  

def return_function_Maze3Score():
    Maze3Score.pack_forget()
    scoreboard.pack()  

#Button 1: Manual controll of the game thru a game controller
def button1_function():
    hide_frame()
    manual.pack()                   #Packing the new frame, so that we can add the different functionalitys
    ser.write(str(-200.00).encode())
    ser.write(str(-700.00).encode())
    return_button = ctk.CTkButton(master = manual,
                                text = "Return to main menu",
                                command = return_function_manual,
                                fg_color = "#0000FF",
                                border_color = "black",           
                                border_width = 1,                 
                                corner_radius = 10,
                                width=150,
                                height=50, 
                                hover = True, 
                                hover_color = "#00008B"
                                )


    label1 = ctk.CTkLabel(manual,
            text = "You are now in manual control, use the Xbox controller",
            fg_color = "transparent",
            font=("Arial", 24, "bold"),
            text_color = "white"
      )

    display_text = """
            \n
            • Use the left joystick to tilt the board
            • Button A manualy starts the elevator
            • Button B manualy stops the elevator
            • When returning to main menu, press any Xbox button
            """
    label2 = ctk.CTkLabel(manual,
            text = display_text,
            fg_color = "transparent",
            font=("Arial", 20, "bold"),
            text_color = "white"
      )
    label1.place(x = 50, y = 90)
    label2.place(x = 0, y = 120)

    return_button.place(relx = 0.02, rely = 0.05, anchor = "nw")

    #Starting the xbox controll
    controller.start()

def run_auto_control():
    serial_port = "/dev/ttyACM0"  # Replace with your Arduino's serial port
    # Run auto control code here
    #print(f"Running Auto Control for maze: {detected_maze}")
    file_path = f"{detected_maze}"
    AutomaticMaze.from_file(serial_port, file_path)
    return_function_maze()

# Function to continuously detect the maze and update the dynamic text
def detect_maze_and_update_text():
    global detected_maze  # To use the global variable detected_maze

    maze_detector = MazeDetector()

    while button_2:
        ret, frame = maze_detector.cap.read()
        if not ret:
            break

        maze_detector.detect_maze(frame)  # Process the frame and detect the maze
        detected_maze = maze_detector.maze_name  # Get the detected maze name
        update_dynamic_text()  # Call the function to update 
        
# Function to update the dynamic text based on the detected maze
def update_dynamic_text():
    global detected_maze
    global dynamic_text
    global run_auto_button

    if detected_maze and detected_maze != "None":
        dynamic_text.configure(
            text=f"Maze detected: {detected_maze}",
            fg_color="green",
            font=("Arial", 28, "bold")
        )
        run_auto_button.configure(state=tk.NORMAL)  # Enable the "Run Auto Control" button
    else:
        dynamic_text.configure(
            text="No maze detected, can't run auto control",
            fg_color="red",
            font=("Arial", 28, "bold")
        )
        run_auto_button.configure(state=tk.DISABLED)  # Disable the "Run Auto Control" button

# Button 2: Auto Control
def button2_function():
    global dynamic_text
    global run_auto_button
    global button_2
    button_2 = True

    hide_frame()
    maze.pack()

    #ser.write(str(-200.00).encode())
    #ser.write(str(-700.00).encode())
    
    return_button = ctk.CTkButton(master=maze,
                                  text="Return to main menu",
                                  command=return_function_maze,
                                  fg_color="#0000FF",
                                  border_color="black",
                                  border_width=1,
                                  corner_radius=10,
                                  width=150,
                                  height=50,
                                  hover=True,
                                  hover_color="#00008B"
                                  )

    return_button.place(relx=0.02, rely=0.05, anchor="nw")

    # Dynamic text label to show the detected maze information
    dynamic_text = ctk.CTkLabel(maze,
                                text="",
                                fg_color="transparent",
                                )


    dynamic_text.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

    # Run Auto Control button
    def run_auto_button_click():
        run_auto_control()

    run_auto_button = ctk.CTkButton(master=maze,
                                    text="Run Auto Control",
                                    fg_color="#0000FF",
                                    border_color="black",
                                    border_width=1,
                                    corner_radius=10,
                                    width=250,
                                    height=150,
                                    text_color="white",
                                    hover_color="#00008B",
                                    font=("Arial", 28, "bold"),
                                    hover=True,
                                    command=run_auto_button_click
                                    )
    run_auto_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

    # Start the thread to continuously detect the maze and update the dynamic text
    import threading
    threading.Thread(target=detect_maze_and_update_text).start()

def run_AI():

    return_function_maze()    

#Button 3: AI Control - Needs to be implemented in the future....
def button3_function():
    global dynamic_text
    global run_auto_button
    global button_2 
    button_2 = True

    hide_frame()
    maze.pack()

    return_button = ctk.CTkButton(master=maze,
                                text="Return to main menu",
                                command=return_function_maze,
                                fg_color="#0000FF",
                                border_color="black",
                                border_width=1,
                                corner_radius=10,
                                width=150,
                                height=50,
                                hover=True,
                                hover_color="#00008B"
                                )

    return_button.place(relx=0.02, rely=0.05, anchor="nw")

    # Dynamic text label to show the detected maze information
    dynamic_text = ctk.CTkLabel(maze,
                                text="",
                                fg_color="transparent",
                                font=("Comic Sans MS", 28, "bold"),
                                text_color="white"
                                )
    dynamic_text.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

    # Run AI button              ##when AI is implemented
    def run_AI_click():
        run_AI()

    run_auto_button = ctk.CTkButton(master=maze,
                                    text="Run AI",
                                    fg_color="#0000FF",
                                    border_color="black",
                                    border_width=1,
                                    corner_radius=10,
                                    width=250,
                                    height=150,
                                    text_color="white",
                                    hover_color="#00008B",
                                    font=("Arial", 28, "bold"),
                                    hover=True,
                                    command=run_AI_click
                                    )
    run_auto_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

    # Start the thread to continuously detect the maze and update the dynamic text
    import threading
    threading.Thread(target=detect_maze_and_update_text).start()

#Override button: Sliders and a button to manualy controll the actuators from the GUI (So that the actuators can be moved even if the xbox controller is not conected)
def override_button_function():
    hide_frame()
    title.pack_forget()
    override.pack()

    #ser.write(str(-200.00).encode())
    #ser.write(str(-700.00).encode())
    
    def actuator1_movement_function(value):
        print(value)
        ser.write(str(value).encode())
        ser.read_all()

    def actuator2_movement_function(value):
        print(value)
        ser.write(str(value).encode())
        #send_size = 0 
        #float_size = link.tx_obj(value/1.0) #Deviding by 1.0 to ensure that the value is a float
        #send_size = float_size
        #link.send(send_size)
        ser.read_all()

    def DC_switch_function():
        float_ = switch_var.get()
        if float_ == 1000: 
            ser.write(str(float_).encode())
            pass
        elif float_ == 2000: 
            ser.write(str(float_).encode())
            pass


    #Slider for the first actuator
    slider1 = ctk.CTkSlider(master=override,
                            from_=-300,
                            to=-100,
                            command=actuator1_movement_function
                            )
    slider1.place(relx=0.5, rely=0.35, anchor=tk.CENTER)

    #Slider for the second actoator
    slider2 = ctk.CTkSlider(master=override,
                            from_=-600,
                            to=-800, 
                            command=actuator2_movement_function
                                )
    slider2.place(relx=0.5, rely=0.45, anchor=tk.CENTER)
    
    #Switch for the DC-motor
    switch_var = ctk.DoubleVar(value=2000)
    switch = ctk.CTkSwitch(master = override,
                            text="",
                            command=DC_switch_function,
                            variable=switch_var,
                            onvalue= 1000,
                            offvalue=2000
                                )
    
    switch.place(relx=0.54, rely = 0.55, anchor = tk.CENTER)

    #Adding labels for the sliders
    actuator1 = ctk.CTkLabel(override, text = "Actuator 1", fg_color = "transparent", font=("Arial", 28))
    actuator1.place(relx=0.2, rely=0.35, anchor = "center")

    actuator2 = ctk.CTkLabel(override, text = "Actuator 2", fg_color = "transparent", font=("Arial", 28))
    actuator2.place(relx=0.2, rely=0.45, anchor = "center")

    dc_motor = ctk.CTkLabel(override, text = "DC-motor", fg_color = "transparent", font=("Arial", 28))
    dc_motor.place(relx = 0.2, rely = 0.55, anchor = "center")

    return_button = ctk.CTkButton(master = override,
                                text = "Return to main menu",
                                command = return_function_override,
                                fg_color = "#0000FF",
                                border_color = "black",           
                                border_width = 1,                 
                                corner_radius = 10,
                                width = 150,
                                height = 50, 
                                hover = True, 
                                hover_color = "#00008B"
                                )
    return_button.place(relx = 0.02, rely = 0.05, anchor = "nw")

def run_Maze1Score():
    scoreboard.pack_forget()
    Maze1Score.pack()
         
    label1 = ctk.CTkLabel(Maze1Score,
            text = "Maze 1 scoreboard",
            fg_color = "transparent",
            font=("Arial", 36, "bold"),
            text_color = "white"
      )
    label1.place(x = 260, y = 70)    

    return_button = ctk.CTkButton(master=Maze1Score,
                                 text="Return to scoreboard selection",
                                 command=return_function_Maze1Score,  # Change this to the appropriate return function
                                 fg_color="#0000FF",
                                 border_color="black",
                                 border_width=1,
                                 corner_radius=10,
                                 width=150,
                                 height=50,
                                 hover=True,
                                 hover_color="#00008B"
                                 )
    return_button.place(relx = 0.02, rely = 0.05, anchor = "nw")

    # Sample list of players and their best times (replace this with your data)
    # Read data from the "Maze1score.txt" file
    players = []
    with open("Maze1score.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            try:
                time_str, name = line.strip().rsplit(" ", 1)
                time = float(time_str)
                players.append({"name": name, "best_time": time})
            except ValueError:
                print(f"Invalid data format in Maze1score.txt: {line.strip()}")

    # Sort players based on their best times (ascending order)
    players = sorted(players, key=lambda player: player["best_time"])

    # Display only the top 5 players' times
    top_5_players = players[:5]
    for rank, player in enumerate(top_5_players, start=1):
        ctk.CTkLabel(Maze1Score, text=str(rank), font=("Arial", 16)).place(x=275, y=120 + rank * 30)
        ctk.CTkLabel(Maze1Score, text=player["name"], font=("Arial", 16)).place(x=375, y=120 + rank * 30)
        ctk.CTkLabel(Maze1Score, text=f"{player['best_time']} seconds", font=("Arial", 16)).place(x=475, y=120 + rank * 30)

def run_Maze2Score():
    scoreboard.pack_forget()
    Maze2Score.pack()

    label1 = ctk.CTkLabel(Maze2Score,
            text = "Maze 2 scoreboard",
            fg_color = "transparent",
            font=("Arial", 36, "bold"),
            text_color = "white"
      )
    label1.place(x = 260, y = 70)     

    return_button = ctk.CTkButton(master=Maze2Score,
                                 text="Return to scoreboard selection",
                                 command=return_function_Maze2Score,  # Change this to the appropriate return function
                                 fg_color="#0000FF",
                                 border_color="black",
                                 border_width=1,
                                 corner_radius=10,
                                 width=150,
                                 height=50,
                                 hover=True,
                                 hover_color="#00008B"
                                 )
    return_button.place(relx = 0.02, rely = 0.05, anchor = "nw")

    # Sample list of players and their best times (replace this with your data)
    # Read data from the "Maze1score.txt" file
    players = []
    with open("Maze2score.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            try:
                time_str, name = line.strip().rsplit(" ", 1)
                time = float(time_str)
                players.append({"name": name, "best_time": time})
            except ValueError:
                print(f"Invalid data format in Maze2score.txt: {line.strip()}")

    # Sort players based on their best times (ascending order)
    players = sorted(players, key=lambda player: player["best_time"])

    # Display only the top 5 players' times
    top_5_players = players[:5]
    for rank, player in enumerate(top_5_players, start=1):
        ctk.CTkLabel(Maze2Score, text=str(rank), font=("Arial", 16)).place(x=275, y=120 + rank * 30)
        ctk.CTkLabel(Maze2Score, text=player["name"], font=("Arial", 16)).place(x=375, y=120 + rank * 30)
        ctk.CTkLabel(Maze2Score, text=f"{player['best_time']} seconds", font=("Arial", 16)).place(x=475, y=120 + rank * 30)

def run_Maze3Score():
    scoreboard.pack_forget()
    Maze3Score.pack()

    label1 = ctk.CTkLabel(Maze3Score,
            text = "Maze 3 scoreboard",
            fg_color = "transparent",
            font=("Arial", 36, "bold"),
            text_color = "white"
      )
    label1.place(x = 260, y = 70)      

    return_button = ctk.CTkButton(master=Maze3Score,
                                 text="Return to scoreboard selection",
                                 command=return_function_Maze3Score,  # Change this to the appropriate return function
                                 fg_color="#0000FF",
                                 border_color="black",
                                 border_width=1,
                                 corner_radius=10,
                                 width=150,
                                 height=50,
                                 hover=True,
                                 hover_color="#00008B"
                                 )
    return_button.place(relx = 0.02, rely = 0.05, anchor = "nw")

    # Sample list of players and their best times (replace this with your data)
    # Read data from the "Maze1score.txt" file
    players = []
    with open("Maze3score.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            try:
                time_str, name = line.strip().rsplit(" ", 1)
                time = float(time_str)
                players.append({"name": name, "best_time": time})
            except ValueError:
                print(f"Invalid data format in Maze3score.txt: {line.strip()}")

    # Sort players based on their best times (ascending order)
    players = sorted(players, key=lambda player: player["best_time"])

    # Display only the top 5 players' times
    top_5_players = players[:5]
    for rank, player in enumerate(top_5_players, start=1):
        ctk.CTkLabel(Maze3Score, text=str(rank), font=("Arial", 16)).place(x=275, y=120 + rank * 30)
        ctk.CTkLabel(Maze3Score, text=player["name"], font=("Arial", 16)).place(x=375, y=120 + rank * 30)
        ctk.CTkLabel(Maze3Score, text=f"{player['best_time']} seconds", font=("Arial", 16)).place(x=475, y=120 + rank * 30)

def show_scoreboard_function():

    hide_frame()
    title.pack_forget()
    scoreboard.pack()


    return_button = ctk.CTkButton(master=scoreboard,
                                 text="Return to main menu",
                                 command=return_function_scoreboard,  # Change this to the appropriate return function
                                 fg_color="#0000FF",
                                 border_color="black",
                                 border_width=1,
                                 corner_radius=10,
                                 width=150,
                                 height=50,
                                 hover=True,
                                 hover_color="#00008B"
                                 )
    return_button.place(relx = 0.02, rely = 0.05, anchor = "nw")

    def Maze1Score():
        run_Maze1Score()

    run_Maze1ScoreButton = ctk.CTkButton(master=scoreboard,
                                    text="Maze 1 Score",
                                    fg_color="#0000FF",
                                    border_color="black",
                                    border_width=1,
                                    corner_radius=10,
                                    width=225,
                                    height=150,
                                    text_color="white",
                                    hover_color="#00008B",
                                    font=("Arial", 28, "bold"),
                                    hover=True,
                                    command=Maze1Score
                                    )
    run_Maze1ScoreButton.place(relx=0.2, rely=0.5, anchor=tk.CENTER)

    def Maze2Score():
        run_Maze2Score()

    run_Maze2ScoreButton = ctk.CTkButton(master=scoreboard,
                                    text="Maze 2 Score",
                                    fg_color="#0000FF",
                                    border_color="black",
                                    border_width=1,
                                    corner_radius=10,
                                    width=225,
                                    height=150,
                                    text_color="white",
                                    hover_color="#00008B",
                                    font=("Arial", 28, "bold"),
                                    hover=True,
                                    command=Maze2Score
                                    )
    run_Maze2ScoreButton.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def Maze3Score():
        run_Maze3Score()

    run_Maze3ScoreButton = ctk.CTkButton(master=scoreboard,
                                    text="Maze 3 Score",
                                    fg_color="#0000FF",
                                    border_color="black",
                                    border_width=1,
                                    corner_radius=10,
                                    width=225,
                                    height=150,
                                    text_color="white",
                                    hover_color="#00008B",
                                    font=("Arial", 28, "bold"),
                                    hover=True,
                                    command=Maze3Score
                                    )
    run_Maze3ScoreButton.place(relx=0.8, rely=0.5, anchor=tk.CENTER)

#Making the tree main buttons in the main menu
button1 = ctk.CTkButton( master = frame,
                        image = add_gameController_image, #Adding the image to the button
                        compound = "right",               #Placing the image on the top
                        text = "Manual",          #Text of the button
                        fg_color = "#0000FF",             #Color of the button
                        border_color = "black",           #Color of the border
                        border_width = 1,                 #Width of the border
                        corner_radius = 10,               #Radius of the border
                        width = 235,                      #Width of the button
                        height = 160,                      #Height of the button
                        text_color = "white",              #Text color of the button
                        font=("Arial", 28),                
                        hover_color = "#00008B",          #Hover color of the button
                        hover = True,                     #Enable hovering
                        command = button1_function        #Calling the function of the button
                        )

button2 = ctk.CTkButton( master = frame,
                        image = add_maze_image,
                        compound = "right",
                        text = "Auto",  
                        fg_color = "#0000FF", 
                        border_color = "black", 
                        border_width = 1,
                        corner_radius = 10,
                        width = 235,
                        height = 160,
                        text_color = "white",
                        font=("Arial", 28),  
                        command = button2_function, 
                        hover_color = "#00008B", 
                        hover = True)

button3 = ctk.CTkButton( master = frame,
                        text = "AI",    
                        fg_color = "#0000FF", 
                        border_color = "black", 
                        border_width = 1,
                        corner_radius = 10,
                        width = 235,
                        height = 160,
                        text_color = "white",
                        font=("Arial", 28), 
                        command = button3_function, 
                        hover_color = "#00008B", 
                        hover = True)

override_button = ctk.CTkButton( master = frame,
                        text = "Override",    
                        fg_color = "#0000FF", 
                        border_color = "black", 
                        width = 150,
                        height = 50,
                        text_color = "white", 
                        command = override_button_function, 
                        hover_color = "#00008B", 
                        hover = True
                        )

scoreboard_button = ctk.CTkButton(master=frame,
                                  text="Scoreboard",
                                  fg_color="#0000FF",
                                  border_color="black",
                                  width=150,
                                  height=50,
                                  text_color="white",
                                  command=show_scoreboard_function,
                                  hover_color="#00008B",
                                  hover=True
                                  )

quit_button = ctk.CTkButton(master = window,
                            text="Quit",
                            text_color = "white",
                            fg_color = "#FF0000",
                            border_color = "black", 
                            hover = True, 
                            width = 150,
                            height = 50,
                            hover_color = "#D10000",
                            command=quit_application
                            )

#placing the buttons on the frame = "frame"
button1.place(relx = 0.20, rely = 0.3, anchor = "center")
button2.place(relx = 0.5, rely = 0.3, anchor = "center")
button3.place(relx = 0.8, rely = 0.3, anchor = "center")
override_button.place(relx = 0.8, rely = 0.82) 
scoreboard_button.place(relx = 0.40, rely = 0.82)   
quit_button.place(relx = 0.02, rely = 0.88)


#Running the window
window.mainloop()