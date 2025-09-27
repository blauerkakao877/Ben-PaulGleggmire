from picamera2 import Picamera2
import numpy as np
import cv2
import time
import LED as L


picam2 = None
blob_detector = None
mask = None
image = None

def init():
    global picam2
    global blob_detector
    picam2 = Picamera2()
    picam2.preview_configuration.raw.size = (1620, 1232)
    picam2.preview_configuration.main.size = (320, 240)
    picam2.preview_configuration.main.format = "RGB888"
    picam2.preview_configuration.align()
    picam2.configure("preview")
    picam2.set_controls({"Saturation": 1.5})
    picam2.set_controls({"Brightness": 0.3})
    picam2.set_controls({"Contrast": 1.5})
    picam2.set_controls({"FrameRate": 40})
    #blob detector für Linien
    blob_params = cv2.SimpleBlobDetector_Params()
    blob_params.filterByArea = True
    blob_params.minArea = 300
    blob_params.maxArea = 10000
    blob_params.filterByCircularity = False
    blob_params.filterByConvexity = False
    blob_params.filterByInertia = False

    #erstelle blob detector
    blob_detector = cv2.SimpleBlobDetector_create(blob_params)
    
    picam2.start()
    time.sleep(2.0)
    
def get_image():
    global picam2
    global image
    frame = picam2.capture_array()
    image = frame[40:240, 0:320]
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    return hsv

def ende():
    picam2.stop()
    
    
def finde_blau(hsv_img):
    global blob_detector
    global mask
#Filterwerte aus Trackbars
    L_hue = 90
    U_hue = 120
    L_sat = 50
    U_sat = 255
    L_val = 50
    U_val = 255
    
    lower_color = np.array([L_hue, L_sat, L_val])
    upper_color = np.array([U_hue, U_sat, U_val])
#Suche nach Linien nur direkt vor dem Auto
    crop_img = hsv_img[170:200, 80:240]
    mask = cv2.inRange(crop_img, lower_color, upper_color)
    mask = cv2.copyMakeBorder(mask,1,1,1,1, cv2.BORDER_CONSTANT, value=[0,0,0])
    mask = cv2.bitwise_not(mask)
    blau_keypoints = blob_detector.detect(mask)
    
    if len(blau_keypoints) > 0:
        L.led_B1()
        return True
    else:
        L.led_B0()
        return False
    

def finde_orange(hsv_img):
    global mask
    global blob_detector
#Filterwerte aus Trackbars
    L_hue = 5
    U_hue = 25
    L_sat = 50
    U_sat = 255
    L_val = 50
    U_val = 255
    
    lower_color = np.array([L_hue, L_sat, L_val])
    upper_color = np.array([U_hue, U_sat, U_val])
#Suche nach Linien nur direkt vor dem Auto
    crop_img = hsv_img[170:200, 80:240]
    mask = cv2.inRange(crop_img, lower_color, upper_color)
    mask = cv2.copyMakeBorder(mask,1,1,1,1, cv2.BORDER_CONSTANT, value=[0,0,0])
    mask = cv2.bitwise_not(mask)
    orange_keypoints = blob_detector.detect(mask)
    
    if len(orange_keypoints) > 0:
        L.led_O1()
        return True
    else:
        L.led_O0()
        return False
    

    
if __name__ == '__main__':
        try:
            init()
            linien_zeit = time.time()
            while True:
                
                bild = get_image()
                cv2.imshow("Original", image)
                linie = finde_blau(bild)
                cv2.imshow("Maske blau", mask)
              #  if time.time() - linien_zeit > 1000:
               #     linie = finde_orange(bild)
               #     if linie == True:
                #        linien_zeit = time.time
               #     cv2.imshow("Maske orange", mask)
                
                

                # Exit loop if 'x' is pressed
                if cv2.waitKey(1) == ord('x'):
                    break
            cv2.destroyAllWindows()
            ende()
            
        except KeyboardInterrupt:
            GPIO.cleanup()

