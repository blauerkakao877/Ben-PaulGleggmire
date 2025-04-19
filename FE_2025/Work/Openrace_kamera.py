import time
import board
import RPi.GPIO as GPIO
from adafruit_motorkit import MotorKit
from adafruit_servokit import ServoKit
import Fahren as F
import LED as L
import gyro as G
import cv2
import numpy as np
import Kameramoduls as K
import Ultrasonic as U


# Initialize MotorKit and ServoKit
Mkit = MotorKit(i2c=board.I2C())
Skit = ServoKit(channels=16)

# Constants and Variables
#default
speed = 0.45
startspeed = 0.45
linien_zaehlen_b =  0.52  #wartezeit bis linie ausgewertet wird
linien_zaehlen_o =  0.52  #wartezeit bis linie ausgewertet wird
linien_zaehlen =  0.52    #wartezeit bis linie ausgewertet wird
linien_warten = 1.0      #vermeidet das linien mehrmals gezählt werden
end_time = 2.0            #wartezeit bis auto nach letzter kurve anhält
#---------------------
# kopiervorlagen für versch geschwindigkeiten
#langsam
slow1 = True #False
speed1 = 0.45
startspeed1 = 0.45
linien_zaehlen_b1 =  0.52  #wartezeit bis linie ausgewertet wird
linien_zaehlen_o1 =  0.52  #wartezeit bis linie ausgewertet wird
linien_zaehlen1 =  0.52    #wartezeit bis linie ausgewertet wird
linien_warten1 = 1.0       #vermeidet das linien mehrmals gezählt werden
end_time1 = 2.0            #wartezeit bis auto nach letzter kurve anhält
#mittel
mid2 = False #True
speed2 = 0.55
startspeed2 = 0.55
linien_zaehlen_b2 =  0.33  #wartezeit bis linie ausgewertet wird
linien_zaehlen_o2 =  0.33  #wartezeit bis linie ausgewertet wird
linien_zaehlen2 =  0.33    #wartezeit bis linie ausgewertet wird
linien_warten2 = 0.70      #vermeidet das linien mehrmals gezählt werden
end_time2 = 1.5            #wartezeit bis auto nach letzter kurve anhält
#schnell !!!ACHTUNG UNSICHER!!!
fast3 = False
speed3 = 0.60
startspeed3 = 0.65
linien_zaehlen_b3 =  0.28  #0.4 #0.44 #wartezeit bis linie ausgewertet wird
linien_zaehlen_o3 =  0.28  #0.4 #0.54 #wartezeit bis linie ausgewertet wird
linien_zaehlen3 =  0.28    #0.4 #0.21 #wartezeit bis linie ausgewertet wird
linien_warten3 = 0.70      #vermeidet das linien mehrmals gezählt werden
end_time3 = 1.2            #wartezeit bis auto nach letzter kurve anhält
########################

steerangle = 95
k = 0.6  # Adjust as needed
Seitehalten = 0
BUTTON_PIN = 16
servmitte = 95
geradeaus = 0
current_direction = "n"
linie = False
linien_zeit = 0
linien_counter = 0
stop_time = time.time() + 180.0 
x = 0
y = 0
s = 0
farbe = "N"
links = False
rechts = False
hellL = 0
hellR = 0
abstand = 0
blaue_linie = False
orange_linie = False
hindernis = False
h_warten = 1.0
h_zeit = 0.0
gesamt = 0.0
Rennen_laeuft = True
reduced = False

#==TEST==
test = False

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN)

# Function to start the program
def start_program():
    global speed
    global startspeed
    global linien_zaehlen_b
    global linien_zaehlen_o
    global linien_zaehlen
    global linien_warten
    global end_time
    
    G.gyro_start()
    K.init("open")
    L.leds_aus()
    if slow1:
        speed = speed1
        startspeed = startspeed1
        linien_zaehlen_b = linien_zaehlen_b1 
        linien_zaehlen_o = linien_zaehlen_o1
        linien_zaehlen = linien_zaehlen1
        linien_warten = linien_warten1
        end_time = end_time1
        L.led_R1()
    if mid2:
        speed = speed2
        startspeed = startspeed2
        linien_zaehlen_b = linien_zaehlen_b2
        linien_zaehlen_o = linien_zaehlen_o2
        linien_zaehlen = linien_zaehlen2
        linien_warten = linien_warten2
        end_time = end_time2
        L.led_G1()
    if fast3:
        speed = speed3
        startspeed = startspeed3
        linien_zaehlen_b = linien_zaehlen_b3
        linien_zaehlen_o = linien_zaehlen_o3
        linien_zaehlen = linien_zaehlen3
        linien_warten = linien_warten3
        end_time = end_time3
        L.led_B1()
        
    L.led_W1()
    print("--Press button to start--")
    while not GPIO.input(BUTTON_PIN):
        time.sleep(0.1)
    L.leds_aus()
    while GPIO.input(BUTTON_PIN):
        time.sleep(0.1)
    print("Program started!")
    time.sleep(0.5)
    
def geradeaus_lenken():
    global geradeaus
    global gesamt
    winkel, gesamt = G.Winkelmessen()
    #lenkwinkel = 93 + k * (geradeaus - gesamt)
    lenkwinkel = 95 + k * (gesamt - geradeaus)
    F.steuern(lenkwinkel)

def linien_suchen(hsv_img):
    global current_direction
    global geradeaus
    global linien_counter
    global linien_zeit
    global linien_warten
    global linien_zaehlen
    global blaue_linie
    global orange_linie
    global Rennen_laeuft
    global speed
    global reduced
    global stop_time
    
    if linien_counter < 12:
        hsv_crop = hsv_img[170:200, 50:210]
    else:
        hsv_crop = hsv_img[50:100, 50:210]
        if not reduced:
            speed = speed*1.0
            F.vor(speed)
            reduced = True
            stop_time = time.time() + end_time
    
    if current_direction == "l":
        if (time.time() - linien_zeit) > linien_warten:
            linie = K.finde_blau(hsv_crop)
            if linie == True:
                linien_zeit = time.time()
                blaue_linie = True
                linien_zaehlen = linien_zaehlen_b
                if linien_counter == 12:
                    Rennen_laeuft = False #Rennen Ende erkannt, setze Stopsignal
        else:
            if blaue_linie and time.time() - linien_zeit > linien_zaehlen:
                linien_counter = linien_counter + 1
                L.led_B1()
                geradeaus = linien_counter*(-90)
                blaue_linie = False
                    
                    
    elif current_direction == "r":
        #L.led_O0()
        #L.led_B0()
        if (time.time() - linien_zeit) > linien_warten:
            linie = K.finde_orange(hsv_crop)
            if linie == True:
                linien_zeit = time.time()
                orange_linie = True
                linien_zaehlen = linien_zaehlen_o
                if linien_counter == 12:
                    Rennen_laeuft = False #Rennen Ende erkannt, setze Stopsignal
            
        else:
            if orange_linie and time.time() - linien_zeit > linien_zaehlen:
                linien_counter = linien_counter + 1
                L.led_O1()
                geradeaus = linien_counter*(90)
                orange_linie = False
        
    else:
        linie = K.finde_blau(hsv_crop)
        if linie == True:
            current_direction = "l"
            linien_zeit = time.time()
            #linien_counter = linien_counter + 1
            #geradeaus = linien_counter*(-90)
            blaue_linie = True
            #linien_zaehlen = linien_zaehlen_b/1.2
            speed = speed*1.2
            F.vor(speed)
            #print("Blau")
            
        else:
            linie = K.finde_orange(hsv_crop)
            if linie == True:
                current_direction = "r"
                linien_zeit = time.time()
                #linien_counter = linien_counter + 1
                #geradeaus = linien_counter*(90)
                orange_linie = True
                #linien_zaehlen = linien_zaehlen_o/1.2
                speed = speed*1.2
                F.vor(speed)
                #print("Orange")
#=============================Hauptprogram===============================================

try:
    if test:
        speed = 0.0
#anfang    
    F.gerade()
    L.leds_aus()
    L.led_startup()
    L.leds_aus()
    start_program()
    F.anfahren(startspeed)
    F.vor(startspeed)
    if linien_counter > 1:
        F.vor(speed)
    
#====================Beginn der Hauptschleife=========================
    
    while not GPIO.input(BUTTON_PIN) and Rennen_laeuft:
        if time.time() > stop_time:
            Rennen_laeuft = False
        winkel, gesamt = G.Winkelmessen()
        hsv_frame, bgr_frame = K.get_image()
        
        
#--Wände finden + auswerten--
        links, rechts, hellL, hellR = K.waende(bgr_frame)
        
#--Hindernisse finden + auswerten--
       # x, y, s, farbe = K.finde_hindernisse(hsv_frame)
#--Linien suchen--
        linien_suchen(hsv_frame)
        if not Rennen_laeuft:
            L.led_Y1()
            F.stop()
            F.gerade()
            L.led_countdown5()
            break
#==TEST==
        if test:
            if farbe == "R":
                cv2.line(bgr_frame, (x, 0), (x, 200), (0, 0, 255), 2)
            if farbe == "G":
                cv2.line(bgr_frame, (x, 0), (x, 200), (0, 255, 0), 2)
            cv2.imshow("Original", bgr_frame)
            cv2.waitKey(1)
            print("x: ", x)
            print("Links: ", links)
            print("Rechts: ", rechts)
            print(linien_counter)
#==TEST=ENDE==
             
#----------------------Ende Linien/Wände/Hindernisse finden------------------------
#sidecrash
        if hellL > 8000:
            links = True
        else:
            hellL = False
            
        if hellR > 8000:
            rechts = True
        else:
            hellR = False
            
        if links and not rechts:
            F.nach_rechts()
            
        elif rechts and not links:
            F.nach_links()
            
        elif rechts and links:
#frontcrash
            if hellL > 12000 or hellR > 12000:
                if gesamt >= geradeaus:
                    F.nach_links()
                else:
                    F.nach_rechts()
                    
                if U.distanz_V() < 5.0:
                    F.stop()
                    if gesamt >= geradeaus:
                        F.stop()
                        time.sleep(0.1)
                        F.nach_rechts()
                        F.ruck(speed)
                        time.sleep(0.8)
                        F.stop()
                        F.gerade()
                        F.anfahren(speed)
                        F.vor(speed)
                    else:
                        F.stop()
                        time.sleep(0.1)
                        F.nach_links()
                        F.ruck(speed)
                        time.sleep(0.8)
                        F.stop()
                        F.gerade()
                        F.anfahren(speed)
                        F.vor(speed)
         
        else:
            if farbe == "R":
                if x > 5:
                    abstand = 5 - x
                    lenkwinkel = 95 + k * (abstand)
                    F.steuern(lenkwinkel)
                else:
                    F.gerade()
                    h_zeit = time.time()
                    hindernis = True
                    
            elif farbe == "G":
                if  x < 315 and x > 0:
                    abstand = 315 - x
                    lenkwinkel = 95 + k * (abstand)
                    F.steuern(lenkwinkel)
                else:
                    F.gerade()
                    h_zeit = time.time()
                    hindernis = True
            
            else:
                if hindernis:
                    F.gerade()
                    if time.time() - h_zeit > h_warten:
                        hindernis = False
                else:      
                    geradeaus_lenken()
            
                    
#-----------------------ENDE-----------------------
    F.stop()
    F.gerade()
    L.led_ende()
    L.led_R1()
    L.led_G1()
    L.led_Y1()
    

except KeyboardInterrupt:
    F.gerade()
    F.stop()
    L.leds_aus()
    L.led_Y1()
    print("Program stopped by the user.")
    