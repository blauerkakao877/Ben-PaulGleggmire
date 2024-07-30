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


# Initialize MotorKit and ServoKit
Mkit = MotorKit(i2c=board.I2C())
Skit = ServoKit(channels=16)

# Constants and Variables
speed = 0.7
steerangle = 93
k = 0.6  # Adjust as needed
Seitehalten = 0
BUTTON_PIN = 16
servmitte = 93
geradeaus = 0
current_direction = "n"
linie = False
linien_zeit = 0
linien_warten = 0.8 #vermeidet das linien mehrmals gezählt werden
linien_counter = 0
x = 0
y = 0
s = 0
farbe = "N"
links = False
rechts = False
hell_L = 0
hell_R = 0
abstand = 0
linien_zaehlen = 0.21 #wartezeit bis linie ausgewertet wird 
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
    G.gyro_start()
    K.init("open")
    L.led_W1()
    print("--Press button to start--")
    while not GPIO.input(BUTTON_PIN):
        time.sleep(0.1)
    L.led_W0()
    while GPIO.input(BUTTON_PIN):
        time.sleep(0.1)
    print("Program started!")
    time.sleep(0.5)
    

    
def geradeaus_lenken():
    global geradeaus
    global gesamt
    winkel, gesamt = G.Winkelmessen()
    #lenkwinkel = 93 + k * (geradeaus - gesamt)
    lenkwinkel = 93 + k * (gesamt - geradeaus)
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
    
    if linien_counter < 12:
        hsv_crop = hsv_img[170:200, 80:240]
    else:
        hsv_crop = hsv_img[50:100, 80:240]
        if not reduced:
            speed = speed*0.7
            F.vor(speed)
            reduced = True

    
    
    if current_direction == "l":
        #L.led_O0()
        #L.led_B0()
        if (time.time() - linien_zeit) > linien_warten:
            linie = K.finde_blau(hsv_crop)
            if linie == True:
                linien_zeit = time.time()
                blaue_linie = True
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
            linien_zaehlen = linien_zaehlen/1.2
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
                linien_zaehlen = linien_zaehlen/1.2
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
    F.vor(speed)
    
#====================Beginn der Hauptschleife=========================
    
    while not GPIO.input(BUTTON_PIN) and Rennen_laeuft:
        #abstand_R = Ultrasonic.distanz_R()
        #abstand_L = Ultrasonic.distanz_L()
        winkel, gesamt = G.Winkelmessen()
        hsv_frame, bgr_frame = K.get_image()
        
        
#--Wände finden + auswerten--
        links, rechts, hell_L, hell_R = K.waende(bgr_frame)
        
#--Hindernisse finden + auswerten--
       # x, y, s, farbe = K.finde_hindernisse(hsv_frame)
#--Linien suchen--
        linien_suchen(hsv_frame)
        if not Rennen_laeuft:
            L.led_Y1()
            F.stop()
            F.gerade()
            #F.ruck(0.5)
            #time.sleep(1.6)
            #F.stop()
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
        if links and not rechts:
            F.nach_rechts()
            
        elif rechts and not links:
            F.nach_links()
            
       # elif rechts and links:
        #    F.stop()
         #   time.sleep(0.1)
         #   F.ruck
         
        else:
            if farbe == "R":
                if x > 5:
                    abstand = 5 - x
                    lenkwinkel = 93 + k * (abstand)
                    F.steuern(lenkwinkel)
                else:
                    F.gerade()
                    h_zeit = time.time()
                    hindernis = True
                    
            elif farbe == "G":
                if  x < 315 and x > 0:
                    abstand = 315 - x
                    lenkwinkel = 93 + k * (abstand)
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
    

except KeyboardInterrupt:
    F.gerade()
    F.stop()
    L.leds_aus()
    print("Program stopped by the user.")
    