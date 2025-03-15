import cv2
import time

import numpy as np
from picamera2 import Picamera2
import Kameramoduls_neu as I

picam2 = None


def read_colorfilter_data():
    with open("/home/pi/FE_2024_WF/Data/Colorfilter.dat", "r") as myfile:
#lower and upper hue for blue
        line = myfile.readline()
        txt = line.split(",")
        lower = int(txt[0])
        upper = int(txt[1])
        cv2.setTrackbarPos("Lower Hue", "Blue Detection", lower)
        cv2.setTrackbarPos("Upper Hue", "Blue Detection", upper)
#lower and upper saturation for blue
        line = myfile.readline()
        txt = line.split(",")
        lower = int(txt[0])
        upper = int(txt[1])
        cv2.setTrackbarPos("Lower Sat", "Blue Detection", lower)
        cv2.setTrackbarPos("Upper Sat", "Blue Detection", upper)
#lower and upper Value for blue
        line = myfile.readline()
        txt = line.split(",")
        lower = int(txt[0])
        upper = int(txt[1])
        cv2.setTrackbarPos("Lower Val", "Blue Detection", lower)
        cv2.setTrackbarPos("Upper Val", "Blue Detection", upper)
        
#========================================================================
        
#lower and upper hue for orange
        line = myfile.readline()
        txt = line.split(",")
        lower = int(txt[0])
        upper = int(txt[1])
        cv2.setTrackbarPos("Lower Hue", "Orange Detection", lower)
        cv2.setTrackbarPos("Upper Hue", "Orange Detection", upper)
#lower and upper saturation for orange
        line = myfile.readline()
        txt = line.split(",")
        lower = int(txt[0])
        upper = int(txt[1])
        cv2.setTrackbarPos("Lower Sat", "Orange Detection", lower)
        cv2.setTrackbarPos("Upper Sat", "Orange Detection", upper)
#lower and upper Value for orange
        line = myfile.readline()
        txt = line.split(",")
        lower = int(txt[0])
        upper = int(txt[1])
        cv2.setTrackbarPos("Lower Val", "Orange Detection", lower)
        cv2.setTrackbarPos("Upper Val", "Orange Detection", upper)
    
#========================================================================

#lower and upper hue for red
        line = myfile.readline()
        txt = line.split(",")
        lower = int(txt[0])
        upper = int(txt[1])
        cv2.setTrackbarPos("Lower Hue", "Red Detection", lower)
        cv2.setTrackbarPos("Upper Hue", "Red Detection", upper)
#lower and upper saturation for red
        line = myfile.readline()
        txt = line.split(",")
        lower = int(txt[0])
        upper = int(txt[1])
        cv2.setTrackbarPos("Lower Sat", "Red Detection", lower)
        cv2.setTrackbarPos("Upper Sat", "Red Detection", upper)
#lower and upper Value for red
        line = myfile.readline()
        txt = line.split(",")
        lower = int(txt[0])
        upper = int(txt[1])
        cv2.setTrackbarPos("Lower Val", "Red Detection", lower)
        cv2.setTrackbarPos("Upper Val", "Red Detection", upper)

#========================================================================

#lower and upper hue for green
        line = myfile.readline()
        txt = line.split(",")
        lower = int(txt[0])
        upper = int(txt[1])
        cv2.setTrackbarPos("Lower Hue", "Green Detection", lower)
        cv2.setTrackbarPos("Upper Hue", "Green Detection", upper)
#lower and upper saturation for green
        line = myfile.readline()
        txt = line.split(",")
        lower = int(txt[0])
        upper = int(txt[1])
        cv2.setTrackbarPos("Lower Sat", "Green Detection", lower)
        cv2.setTrackbarPos("Upper Sat", "Green Detection", upper)
#lower and upper Value for green
        line = myfile.readline()
        txt = line.split(",")
        lower = int(txt[0])
        upper = int(txt[1])
        cv2.setTrackbarPos("Lower Val", "Green Detection", lower)
        cv2.setTrackbarPos("Upper Val", "Green Detection", upper)

#========================================================================
        
#lower and upper hue for magenta
        line = myfile.readline()
        txt = line.split(",")
        lower = int(txt[0])
        upper = int(txt[1])
        cv2.setTrackbarPos("Lower Hue", "Magenta Detection", lower)
        cv2.setTrackbarPos("Upper Hue", "Magenta Detection", upper)
#lower and upper saturation for magenta
        line = myfile.readline()
        txt = line.split(",")
        lower = int(txt[0])
        upper = int(txt[1])
        cv2.setTrackbarPos("Lower Sat", "Magenta Detection", lower)
        cv2.setTrackbarPos("Upper Sat", "Magenta Detection", upper)
#lower and upper Value for magenta
        line = myfile.readline()
        txt = line.split(",")
        lower = int(txt[0])
        upper = int(txt[1])
        cv2.setTrackbarPos("Lower Val", "Magenta Detection", lower)
        cv2.setTrackbarPos("Upper Val", "Magenta Detection", upper)



#Close file
        myfile.close()
    
def write_colorfilter_data():
    with open("/home/pi/FE_2024_WF/Data/Colorfilter.dat", "w") as myfile:
#lower and upper hue for blue
        lower = cv2.getTrackbarPos("Lower Hue", "Blue Detection")
        upper = cv2.getTrackbarPos("Upper Hue", "Blue Detection")
        line = str(lower)+","+str(upper)+"\n"
        myfile.write(line)
#lower and upper saturation for blue
        lower = cv2.getTrackbarPos("Lower Sat", "Blue Detection")
        upper = cv2.getTrackbarPos("Upper Sat", "Blue Detection")
        line = str(lower)+","+str(upper)+"\n"
        myfile.write(line)
#lower and upper Value for blue
        lower = cv2.getTrackbarPos("Lower Val", "Blue Detection")
        upper = cv2.getTrackbarPos("Upper Val", "Blue Detection")
        line = str(lower)+","+str(upper)+"\n"
        myfile.write(line)
        
#========================================================================

#lower and upper hue for orange
        lower = cv2.getTrackbarPos("Lower Hue", "Orange Detection")
        upper = cv2.getTrackbarPos("Upper Hue", "Orange Detection")
        line = str(lower)+","+str(upper)+"\n"
        myfile.write(line)
#lower and upper saturation for orange
        lower = cv2.getTrackbarPos("Lower Sat", "Orange Detection")
        upper = cv2.getTrackbarPos("Upper Sat", "Orange Detection")
        line = str(lower)+","+str(upper)+"\n"
        myfile.write(line)
#lower and upper Value for orange
        lower = cv2.getTrackbarPos("Lower Val", "Orange Detection")
        upper = cv2.getTrackbarPos("Upper Val", "Orange Detection")
        line = str(lower)+","+str(upper)+"\n"
        myfile.write(line)

#========================================================================

#lower and upper hue for red
        lower = cv2.getTrackbarPos("Lower Hue", "Red Detection")
        upper = cv2.getTrackbarPos("Upper Hue", "Red Detection")
        line = str(lower)+","+str(upper)+"\n"
        myfile.write(line)
#lower and upper saturation for red
        lower = cv2.getTrackbarPos("Lower Sat", "Red Detection")
        upper = cv2.getTrackbarPos("Upper Sat", "Red Detection")
        line = str(lower)+","+str(upper)+"\n"
        myfile.write(line)
#lower and upper Value for red
        lower = cv2.getTrackbarPos("Lower Val", "Red Detection")
        upper = cv2.getTrackbarPos("Upper Val", "Red Detection")
        line = str(lower)+","+str(upper)+"\n"
        myfile.write(line)

#========================================================================
        
#lower and upper hue for green
        lower = cv2.getTrackbarPos("Lower Hue", "Green Detection")
        upper = cv2.getTrackbarPos("Upper Hue", "Green Detection")
        line = str(lower)+","+str(upper)+"\n"
        myfile.write(line)
#lower and upper saturation for green
        lower = cv2.getTrackbarPos("Lower Sat", "Green Detection")
        upper = cv2.getTrackbarPos("Upper Sat", "Green Detection")
        line = str(lower)+","+str(upper)+"\n"
        myfile.write(line)
#lower and upper Value for green
        lower = cv2.getTrackbarPos("Lower Val", "Green Detection")
        upper = cv2.getTrackbarPos("Upper Val", "Green Detection")
        line = str(lower)+","+str(upper)+"\n"
        myfile.write(line)

#========================================================================
        
#lower and upper hue for magenta
        lower = cv2.getTrackbarPos("Lower Hue", "Magenta Detection")
        upper = cv2.getTrackbarPos("Upper Hue", "Magenta Detection")
        line = str(lower)+","+str(upper)+"\n"
        myfile.write(line)
#lower and upper saturation for magenta
        lower = cv2.getTrackbarPos("Lower Sat", "Magenta Detection")
        upper = cv2.getTrackbarPos("Upper Sat", "Magenta Detection")
        line = str(lower)+","+str(upper)+"\n"
        myfile.write(line)
#lower and upper Value for magenta
        lower = cv2.getTrackbarPos("Lower Val", "Magenta Detection")
        upper = cv2.getTrackbarPos("Upper Val", "Magenta Detection")
        line = str(lower)+","+str(upper)+"\n"
        myfile.write(line)


#-----------------------------------------------
#Close file
        myfile.close()

# Function to detect a specific color
def detect_color(hsv_image, lower_color, upper_color):
    # Convert image to HSV color space
    
    # Threshold the HSV image to get only the specified color
    mask = cv2.inRange(hsv_image, lower_color, upper_color)
    
    return mask

def detect_red(hsv_image, lower_color, upper_color):
    # Convert image to HSV color space
    
    lower_color1 = np.array([0, lower_color[1], lower_color[2]])
    upper_color1 = np.array([lower_color[0], upper_color[1], upper_color[2]])
    lower_color2 = np.array([upper_color[0], lower_color[1], lower_color[2]])
    upper_color2 = np.array([179, upper_color[1], upper_color[2]])
    
    #Threshold the HSV image to get only the specified color
    mask1 = cv2.inRange(hsv_image, lower_color1, upper_color1)
    mask2 = cv2.inRange(hsv_image, lower_color2, upper_color2)
    mask = cv2.bitwise_or(mask1, mask2)
    
    #R_lower1 = np.array([0, 20, 70])
   # R_upper1 = np.array([10, 255, 255])
   # R_mask1 = cv2.inRange(hsv_image, R_lower1, R_upper1)

    #get the positions for the color red2
   # R_lower2 = np.array([R_h_max, R_s_min, R_v_min])
   # R_upper2 = np.array([179, R_s_max, R_v_max])
   # R_mask2 = cv2.inRange(imgHsv, R_lower2, R_upper2)

    #calculate summary mask from mask1 and mask2
    #R_mask = cv2.bitwise_or(R_mask1, R_mask2)
    
    return mask

# Callback function for trackbars
def update_color_values(x):
    global lower_color, upper_color
    lower_color[0] = cv2.getTrackbarPos("Lower Hue", "Color Detection")
    upper_color[0] = cv2.getTrackbarPos("Upper Hue", "Color Detection")
    lower_color[1] = cv2.getTrackbarPos("Lower Sat", "Color Detection")
    upper_color[1] = cv2.getTrackbarPos("Upper Sat", "Color Detection")
    lower_color[2] = cv2.getTrackbarPos("Lower Val", "Color Detection")
    upper_color[2] = cv2.getTrackbarPos("Upper Val", "Color Detection")
    
def update_Wall_values(x):
    global lower_color, upper_color
    lower_color[0] = 0
    upper_color[0] = 180
    lower_color[1] = 0
    upper_color[1] = 255
    lower_color[2] = cv2.getTrackbarPos("Lower Val", "Color Detection")
    upper_color[2] = cv2.getTrackbarPos("Upper Val", "Color Detection")

#================Main Program==============================

# Create a window to display color detection and trackbars to adjust thresholds for green detection
cv2.namedWindow("Green Detection")
cv2.createTrackbar("Lower Hue", "Green Detection", 35, 180, update_color_values)
cv2.createTrackbar("Upper Hue", "Green Detection", 85, 180, update_color_values)
cv2.createTrackbar("Lower Sat", "Green Detection", 50, 255, update_color_values)
cv2.createTrackbar("Upper Sat", "Green Detection", 255, 255, update_color_values)
cv2.createTrackbar("Lower Val", "Green Detection", 50, 255, update_color_values)
cv2.createTrackbar("Upper Val", "Green Detection", 255, 255, update_color_values)

# Initialize values for green color detection
lower_color = np.array([35, 50, 50])
upper_color = np.array([85, 255, 255])

# Create a window to display color detection and trackbars to adjust thresholds for red detection
cv2.namedWindow("Red Detection")
cv2.createTrackbar("Lower Hue", "Red Detection", 0, 180, update_color_values)
cv2.createTrackbar("Upper Hue", "Red Detection", 10, 180, update_color_values)
cv2.createTrackbar("Lower Sat", "Red Detection", 20, 255, update_color_values)
cv2.createTrackbar("Upper Sat", "Red Detection", 255, 255, update_color_values)
cv2.createTrackbar("Lower Val", "Red Detection", 70, 255, update_color_values)
cv2.createTrackbar("Upper Val", "Red Detection", 255, 255, update_color_values)

# Initialize values for red color detection
lower1_color = np.array([0, 20, 70])
upper1_color = np.array([10, 255, 255])

lower2_color = np.array([0, 20, 70])
upper2_color = np.array([10, 255, 255])



# Create a window to display color detection and trackbars to adjust thresholds for orange detection
cv2.namedWindow("Orange Detection")
cv2.createTrackbar("Lower Hue", "Orange Detection", 5, 180, update_color_values)
cv2.createTrackbar("Upper Hue", "Orange Detection", 25, 180, update_color_values)
cv2.createTrackbar("Lower Sat", "Orange Detection", 50, 255, update_color_values)
cv2.createTrackbar("Upper Sat", "Orange Detection", 255, 255, update_color_values)
cv2.createTrackbar("Lower Val", "Orange Detection", 50, 255, update_color_values)
cv2.createTrackbar("Upper Val", "Orange Detection", 255, 255, update_color_values)

# Initialize values for orange color detection
lower_color = np.array([5, 50, 50])
upper_color = np.array([25, 255, 255])


# Create a window to display color detection and trackbars to adjust thresholds for blue detection
cv2.namedWindow("Blue Detection")
cv2.createTrackbar("Lower Hue", "Blue Detection", 0, 179, update_color_values)
cv2.createTrackbar("Upper Hue", "Blue Detection", 0, 179, update_color_values)
cv2.createTrackbar("Lower Sat", "Blue Detection", 0, 255, update_color_values)
cv2.createTrackbar("Upper Sat", "Blue Detection", 0, 255, update_color_values)
cv2.createTrackbar("Lower Val", "Blue Detection", 0, 255, update_color_values)
cv2.createTrackbar("Upper Val", "Blue Detection", 0, 255, update_color_values)

# Initialize values for blue color detection
lower_color = np.array([0, 0, 0])
upper_color = np.array([179, 255, 255])


# Create a window to display color detection and trackbars to adjust thresholds for Magenta detection-----------
cv2.namedWindow("Magenta Detection")
cv2.createTrackbar("Lower Hue", "Magenta Detection", 90, 180, update_color_values)
cv2.createTrackbar("Upper Hue", "Magenta Detection", 120, 180, update_color_values)
cv2.createTrackbar("Lower Sat", "Magenta Detection", 50, 255, update_color_values)
cv2.createTrackbar("Upper Sat", "Magenta Detection", 255, 255, update_color_values)
cv2.createTrackbar("Lower Val", "Magenta Detection", 50, 255, update_color_values)
cv2.createTrackbar("Upper Val", "Magenta Detection", 255, 255, update_color_values)

# Initialize values for Magenta color detection
lower_color = np.array([90, 50, 50])
upper_color = np.array([120, 255, 255])


# Create a window to display color detection and trackbars to adjust thresholds for black detection
cv2.namedWindow("Wall Detection")
cv2.createTrackbar("Lower Val", "Wall Detection", 0, 255, update_Wall_values)
cv2.createTrackbar("Upper Val", "Wall Detection", 70, 255, update_Wall_values)

# Initialize values for black color detection
lower_color = np.array([0, 0, 0])
upper_color = np.array([180, 255, 70])


I.init("obstacle")


read_colorfilter_data()

# Main loop for capturing and processing frames
while True:
    
    # Capture frame from camera
    frame, bgr_frame = I.get_image()
    #frame, bgr_frame = I.get_image_back()
    

    # Get current trackbar positions for green color detection
    lower_color[0] = cv2.getTrackbarPos("Lower Hue", "Green Detection")
    upper_color[0] = cv2.getTrackbarPos("Upper Hue", "Green Detection")
    lower_color[1] = cv2.getTrackbarPos("Lower Sat", "Green Detection")
    upper_color[1] = cv2.getTrackbarPos("Upper Sat", "Green Detection")
    lower_color[2] = cv2.getTrackbarPos("Lower Val", "Green Detection")
    upper_color[2] = cv2.getTrackbarPos("Upper Val", "Green Detection")

    # Detect green color using updated threshold values
    green_detected = detect_color(frame, lower_color, upper_color)

    # Get current trackbar positions for red color detection
    lower_color[0] = cv2.getTrackbarPos("Lower Hue", "Red Detection")
    upper_color[0] = cv2.getTrackbarPos("Upper Hue", "Red Detection")
    lower_color[1] = cv2.getTrackbarPos("Lower Sat", "Red Detection")
    upper_color[1] = cv2.getTrackbarPos("Upper Sat", "Red Detection")
    lower_color[2] = cv2.getTrackbarPos("Lower Val", "Red Detection")
    upper_color[2] = cv2.getTrackbarPos("Upper Val", "Red Detection")

    # Detect red color using updated threshold values
    red_detected = detect_red(frame, lower_color, upper_color)

    # Get current trackbar positions for orange color detection
    lower_color[0] = cv2.getTrackbarPos("Lower Hue", "Orange Detection")
    upper_color[0] = cv2.getTrackbarPos("Upper Hue", "Orange Detection")
    lower_color[1] = cv2.getTrackbarPos("Lower Sat", "Orange Detection")
    upper_color[1] = cv2.getTrackbarPos("Upper Sat", "Orange Detection")
    lower_color[2] = cv2.getTrackbarPos("Lower Val", "Orange Detection")
    upper_color[2] = cv2.getTrackbarPos("Upper Val", "Orange Detection")

    # Detect orange color using updated threshold values
    orange_detected = detect_color(frame, lower_color, upper_color)

    # Get current trackbar positions for blue color detection
    lower_color[0] = cv2.getTrackbarPos("Lower Hue", "Blue Detection")
    upper_color[0] = cv2.getTrackbarPos("Upper Hue", "Blue Detection")
    lower_color[1] = cv2.getTrackbarPos("Lower Sat", "Blue Detection")
    upper_color[1] = cv2.getTrackbarPos("Upper Sat", "Blue Detection")
    lower_color[2] = cv2.getTrackbarPos("Lower Val", "Blue Detection")
    upper_color[2] = cv2.getTrackbarPos("Upper Val", "Blue Detection")

    # Detect blue color using updated threshold values
    blue_detected = detect_color(frame, lower_color, upper_color)
    
    
    # Get current trackbar positions for Magenta color detection
    lower_color[0] = cv2.getTrackbarPos("Lower Hue", "Magenta Detection")
    upper_color[0] = cv2.getTrackbarPos("Upper Hue", "Magenta Detection")
    lower_color[1] = cv2.getTrackbarPos("Lower Sat", "Magenta Detection")
    upper_color[1] = cv2.getTrackbarPos("Upper Sat", "Magenta Detection")
    lower_color[2] = cv2.getTrackbarPos("Lower Val", "Magenta Detection")
    upper_color[2] = cv2.getTrackbarPos("Upper Val", "Magenta Detection")

    # Detect blue color using updated threshold values
    Magenta_detected = detect_color(frame, lower_color, upper_color)
    
    
    # Get current trackbar positions for Black color detection
    lower_color[2] = cv2.getTrackbarPos("Lower Val", "Wall Detection")
    upper_color[2] = cv2.getTrackbarPos("Upper Val", "Wall Detection")

    # Detect blue color using updated threshold values
    Wall_detected = detect_color(frame, lower_color, upper_color)

    # Display the original frame and the color detections
    cv2.imshow("Original Frame", bgr_frame)
    cv2.imshow("Green Detection", green_detected)
    cv2.imshow("Red Detection", red_detected)
    cv2.imshow("Orange Detection", orange_detected)
    cv2.imshow("Blue Detection", blue_detected)
    cv2.imshow("Magenta Detection", Magenta_detected)
    cv2.imshow("Wall Detection", Wall_detected)

    # Exit loop if 'x' is pressed save  data when s is pressed
    Key = cv2.waitKey(1)
    
    if Key == ord('x'):
        break
    elif Key == ord('s'):
        write_colorfilter_data()
        print("+++++++++++++colours saved+++++++++++++")
        break
        
    
cv2.destroyAllWindows()