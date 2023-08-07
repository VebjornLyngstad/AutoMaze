import cv2
import numpy as np
import time
import tkinter as tk
from tkinter import simpledialog, messagebox
from threading import Thread


import tkinter as tk
import customtkinter as ctk 

class NewWindow():
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title('Scoreboard')
        self.root.geometry("400x200")

        self.label1 = ctk.CTkLabel(self.root, text = "Write your initials here to show the scoreboard")
        self.label1.place(relx = 0.5, rely = 0.4, anchor = ctk.CENTER)


        self.textbox = ctk.CTkTextbox(self.root, width=100, height = 20)
        self.textbox.place(relx = 0.5, rely = 0.5, anchor = ctk.CENTER)
        self.textbox.configure(state = "normal")

        def bt_press(self):
            print(self.textbox.get("0.0", "end"))
            self.destroy()
        def bt2_press(self):
            print("Nå gjør jeg ingenting")
            self.destroy()

        self.bt1 = ctk.CTkButton(self.root, text="Display on scoreboard", command=bt_press)
        self.bt2 = ctk.CTkButton(self.root, text="Dont display on scoreboard", command=bt2_press)
        self.bt1.place(relx = 0.3, rely = 0.8, anchor = ctk.CENTER)
        self.bt2.place(relx = 0.7, rely = 0.8, anchor = ctk.CENTER)
    



class ObjectTracker:
    def __init__(self):
        self.cap = cv2.VideoCapture(1)
        self.lower_silver = np.array([0, 40, 150])
        self.upper_silver = np.array([179, 255, 255])
        self.start_time_green = None
        self.start_time_red = None
        self.printed_time_red = False
        self.elapsed_time_red = None
        self.is_running = False
        self.thread = None


    def check_intersection(self, rect1, rect2):
        x1, y1, w1, h1 = rect1
        x2, y2, w2, h2 = rect2

        if x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2:
            return True
        return False

    def process_frame(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower_silver, self.upper_silver)

        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        frame_resized = frame[0:400, 200:570]
        mask_resized = mask[0:400, 200:570]

        contours, _ = cv2.findContours(mask_resized, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        largest_contour_area = 0
        largest_contour = None
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > largest_contour_area:
                largest_contour_area = area
                largest_contour = contour

        if largest_contour is not None:
            x, y, w, h = cv2.boundingRect(largest_contour)
            cv2.rectangle(frame_resized, (x, y), (x + w, y + h), (255, 0, 0), 2)

            starting_point_rectangle = (10, 75, 50, 50)
            goal_rectangle = (300, 0, 69, 70)

            intersect_starting_point = self.check_intersection((x, y, w, h), starting_point_rectangle)
            intersect_goal = self.check_intersection((x, y, w, h), goal_rectangle)

            if not intersect_starting_point and not intersect_goal and self.start_time_green is None:
                self.start_time_green = time.time()
                self.start_time_red = None
                self.printed_time_red = False
            elif intersect_starting_point and self.start_time_green is not None and not self.printed_time_red:
                elapsed_time_green = time.time() - self.start_time_green
                print(f"Time taken to enter GOAL: {elapsed_time_green:.2f} seconds")

                #a = NewWindow(tid)  #This might work?




                self.printed_time_red = True
                self.start_time_green = None
            elif intersect_goal and self.start_time_green is not None and not self.printed_time_red:
                self.start_time_red = time.time()
                self.printed_time_red = True
                self.start_time_green = None
                self.elapsed_time_red = time.time() - self.start_time_red

        if self.start_time_green is not None:
            elapsed_time_green = time.time() - self.start_time_green
            cv2.putText(frame_resized, f"Time: {elapsed_time_green:.2f} s", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        if self.start_time_red is not None and not self.printed_time_red:
            elapsed_time_red = time.time() - self.start_time_red
            cv2.putText(frame_resized, f"Time: {elapsed_time_red:.2f} s", (frame_resized.shape[1] - 350, frame_resized.shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.rectangle(frame_resized, (10, 75), (60, 130), (0, 0, 255), 2)
        cv2.rectangle(frame_resized, (300, 0), (369, 70), (0, 255, 0), 2)

        return frame_resized

    def close(self):
        self.is_running = False

    def run(self):
        self.is_running = True
        while self.is_running:
            _, frame = self.cap.read()
            if frame is not None:
                processed_frame = self.process_frame(frame)
                # Display the processed_frame on the GUI (if needed)

            key = cv2.waitKey(1)
            if key == 27:
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def start_tracking(self):
        self.thread = Thread(target=self.run)
        self.thread.start()

    def stop_tracking(self):
        self.close()
        self.thread.join()
        if self.start_time_red is not None:
            self.elapsed_time_red = time.time() - self.start_time_red

    def save_data(self):
        user_input = simpledialog.askstring("Input", "Enter some text:")
        if user_input is not None:
            with open("saved_data.txt", "w") as file:
                file.write(f"Text entered: {user_input}\n")
                file.write(f"Elapsed time for red rectangle: {self.elapsed_time_red:.2f} seconds")

        self.close()


if __name__ == "__main__":
    tracker = ObjectTracker()
    tracker.start_tracking()

    while tracker.thread.is_alive():
        time.sleep(0.1)  # Wait for a short duration

    tracker.stop_tracking()

    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Create a dummy window to handle the messagebox
    dummy = tk.Toplevel(root)
    dummy.withdraw()

    messagebox.showinfo("Elapsed Time", "Elapsed time for red rectangle: {} seconds".format(tracker.elapsed_time_red))
    tracker.save_data()

    # Destroy the dummy window and exit the main loop
    dummy.destroy()
    root.quit()