import cv2
import numpy as np

class MazeDetector:
    def __init__(self, frame_width=1080, frame_height=720, show_feed=False):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

        self.templates = [
            {"image": cv2.imread("/home/maze/Desktop/Maze_Project/Code/images/maze1_grayscale_black", cv2.IMREAD_GRAYSCALE), "name": "Maze 1"},
            {"image": cv2.imread("/home/maze/Desktop/Maze_Project/Code/images/maze2_grayscale_filter_new", cv2.IMREAD_GRAYSCALE), "name": "Maze 2"},
            {"image": cv2.imread("/home/maze/Desktop/Maze_Project/Code/images/maze3_grayscale_black", cv2.IMREAD_GRAYSCALE), "name": "Maze 3"},
            {"image": cv2.imread("/home/maze/Desktop/Maze_Project/Code/images/empty_maze", cv2.IMREAD_GRAYSCALE), "name": "None"}
        ]

        self.no_maze_found_time = 0
        self.no_maze_found_printed = False
        self.maze_name = ""
        self.show_feed = show_feed

    def apply_clahe_correction(self, img):
        clahefilter = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(16, 16))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        claheCorrecttedFrame = clahefilter.apply(gray)
        return cv2.merge((claheCorrecttedFrame, claheCorrecttedFrame, claheCorrecttedFrame))

    def remove_glare(self, img):
        GLARE_MIN = np.array([0, 0, 50], np.uint8)
        GLARE_MAX = np.array([0, 0, 225], np.uint8)

        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        frame_threshed = cv2.inRange(hsv_img, GLARE_MIN, GLARE_MAX)

        grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        mask1 = cv2.threshold(grayimg, 220, 255, cv2.THRESH_BINARY)[1]
        result1 = cv2.inpaint(img, mask1, 0.1, cv2.INPAINT_TELEA)
        return result1

    def detect_maze(self, frame):
        Ramme = frame[0: 400, 200: 570]
        clahe_corrected_frame = self.apply_clahe_correction(Ramme)
        glare_removed_frame = self.remove_glare(clahe_corrected_frame)
        gray_frame = cv2.cvtColor(glare_removed_frame, cv2.COLOR_BGR2GRAY)

        best_match_score = 0
        best_match_name = ""

        for template in self.templates:
            if template["image"] is None:
                continue

            resized_template = cv2.resize(template["image"], (Ramme.shape[1], Ramme.shape[0]))
            res = cv2.matchTemplate(gray_frame, resized_template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            thresholds = {"Maze 1": 0.4, "Maze 2": 0.2, "Maze 3": 0.4, "None": 0.4}
            if max_val > thresholds[template["name"]] and max_val > best_match_score:
                best_match_score = max_val
                best_match_name = template["name"]

        if best_match_score > 0:
            self.maze_name = best_match_name
            self.no_maze_found_time = 0
            self.no_maze_found_printed = False
            #print(f"Detected: {self.maze_name} precision: {best_match_score:.2f}/1.00")
        else:
            self.maze_name = ""
            self.no_maze_found_time += 1
    
    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()

'''
if __name__ == "__main__":
    detector = MazeDetector(show_feed=False)
    detector.run_detection()
    detected_maze = detector.get_detected_maze()
    print("Detected Maze:", detected_maze)
'''


