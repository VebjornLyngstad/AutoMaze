import cv2

class MazeDetector:
    # Initialize the MazeDetector class with video capture settings
    def __init__(self, video_capture_index=0, frame_width=1080, frame_height=720):
        self.cap = cv2.VideoCapture(video_capture_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

        # Load the maze templates
        self.templates = [
            {"image": cv2.imread("/home/maze/Desktop/Maze_Project/Code/images/maze1_grayscale", cv2.IMREAD_GRAYSCALE), "name": "Maze 1"},
            {"image": cv2.imread("/home/maze/Desktop/Maze_Project/Code/images/maze2_grayscale", cv2.IMREAD_GRAYSCALE), "name": "Maze 2"},
            {"image": cv2.imread("/home/maze/Desktop/Maze_Project/Code/images/maze3_grayscale", cv2.IMREAD_GRAYSCALE), "name": "Maze 3"},
            {"image": cv2.imread("/home/maze/Desktop/Maze_Project/Code/images/maze4_grayscale", cv2.IMREAD_GRAYSCALE), "name": "Maze 4"},
            # Add more templates for other mazes if needed
        ]

    # Read a frame from the video capture
    def detect_maze(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        
        # Extract a region of interest (ROI) from the frame for maze detection
        Ramme = frame[20: 400, 220: 570]
        gray_frame = cv2.cvtColor(Ramme, cv2.COLOR_BGR2GRAY)

        best_match_score = 0  # Tracks the best match score
        best_match_name = ""  # Tracks the best match name

        for template in self.templates:
            if template["image"] is None:
                continue

            # Resize the template image to match the size of the region of interest (Ramme)
            resized_template = cv2.resize(template["image"], (Ramme.shape[1], Ramme.shape[0]))

            # Perform template matching
            res = cv2.matchTemplate(gray_frame, resized_template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            # Set different thresholds for each maze template
            thresholds = {"Maze 1": 0.85, "Maze 2": 0.85, "Maze 3": 0.75, "Maze 4": 0.85}
            if max_val > thresholds[template["name"]] and max_val > best_match_score:
                best_match_score = max_val
                best_match_name = template["name"]

        if best_match_score > 0:
            return best_match_name
        else:
            return None

    # Release the video capture and close OpenCV windows
    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()

#End of MazeDetector class

# Example usage:
#if __name__ == "__main__":
 #   maze_detector = MazeDetector()

  #  while True:
   #     detected_maze = maze_detector.detect_maze()
    #    if detected_maze:
     #       print(f"Detected: {detected_maze}")
            # Do something with the detected maze information here
      #      break  # Stop the loop after detecting a maze

    #maze_detector.release()