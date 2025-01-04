import cv2
import time
from picamera2 import Picamera2, Preview
from libcamera import controls

picam_vorn = Picamera2(0)
picam_back = Picamera2(1)

picam_vorn.preview_configuration.raw.size = (1620,1232)
picam_vorn.preview_configuration.main.size = (320,240)
picam_vorn.preview_configuration.main.format = "RGB888"
picam_vorn.preview_configuration.align()
picam_vorn.configure("preview")
picam_vorn.set_controls({"Saturation": 1.5})
picam_vorn.set_controls({"Brightness": 0.3})
picam_vorn.set_controls({"Contrast": 1.5})
picam_vorn.set_controls({"FrameRate": 40})


picam_back.preview_configuration.raw.size = (1620,1232)
picam_back.preview_configuration.main.size = (320,240)
picam_back.preview_configuration.main.format = "RGB888"
picam_back.preview_configuration.align()
picam_back.configure("preview")
picam_back.set_controls({"Saturation": 1.5})
picam_back.set_controls({"Brightness": 0.3})
picam_back.set_controls({"Contrast": 1.5})
picam_back.set_controls({"FrameRate": 40})

picam_vorn.start()
picam_back.start()
counter0 = 0
while True:
    img0_roh = picam_vorn.capture_array()
    img0 = img0_roh[30:240, 0:320]
    im1= picam_back.capture_array()
    
    cv2.imshow("Camera vorn", img0)
    cv2.imshow("Camera hinten", im1)
    
    if cv2.waitKey(1)==ord('x'):
        break
    elif cv2.waitKey(1)==ord('s'):
        Filename = "/home/pi/FE_2025/Work/Bilder_machen/Bilder/Bild_" + str(counter) + ".jpg"
        print(Filename)
        cv2.imwrite(Filename, im0)
        counter0 = counter0 + 1
cv2.destroyAllWindows()

