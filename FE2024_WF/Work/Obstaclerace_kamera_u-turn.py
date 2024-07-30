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
speed = 0.5
steerangle = 93
k = 0.6   #Adjust as needed standard faktor fuer gerade
kh = 0.9  #Adjust as needed faktor fuer hindernisse
Seitehalten = 0
BUTTON_PIN = 16
servmitte = 93
geradeaus = 0
current_direction = "n"
linie = False
linien_zeit = 0
linien_warten = 2.1 #vermeidet das linien mehrmals gezählt werden
linien_counter = 0
x = 0
y = 0
s = 0
farbe = "N"
links = False
rechts = False
hellL = 0
hellR = 0
abstand = 0
linien_zaehlen = 0.21 #wartezeit/Sperrzeit bis linie ausgewertet wird
linien_zaehlen_LG = 0.18  #Links+Grun
linien_zaehlen_RG = 0.27  #Rechts+Grun
linien_zaehlen_LR = 0.18  #Links+Rot
linien_zaehlen_RR = 0.27  #Rechts+Rot
blaue_linie = False
orange_linie = False
hindernis = False
h_warten = 1.5
h_zeit = 0.0
gesamt = 0.0
Rennen_laeuft = True
hoehe = 200
breite = 320
hindernis_sperre = False
linie_imbild = False
NowUturn = False
Uturn = False
Uturndetected = False
endcounter = 12
#==TEST==
test = False

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN)

#----------------Funktionen erstellen----------------

# Function to start the program
def start_program():
    G.gyro_start()
    K.init("obstacle")
    hindernis_sperre = False
    L.led_Y1()
    print("--Press button to start--")
    while not GPIO.input(BUTTON_PIN):
        time.sleep(0.1)
    L.led_Y0()
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

def DoUturn():
    global endcounter
    global NowUturn
    
    F.stop()
    time.sleep(1.0)
    F.ruck(0.5)
    time.sleep(0.5)
    F.stop()
    endcounter = 12
    geradeaus = geradeaus - 180
    if current_direction == "l":
        current_direction = "r"
    elif current_direction == "r":
        current_direction = "l"
    F.nach_links()
    F.vor(speed)
    geradeaus_lenken()
    NowUturn = False
    
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
    global hindernis_sperre
    global linie_imbild
    global endcounter
    
    if linien_counter < endcounter:
        if current_direction == "l":
#nach links verschieben, damit linie orange nicht 2 mal gezählt wird und crash auf innenecke kommt
            hsv_crop = hsv_img[hoehe - 30:hoehe, 60:200]
        elif current_direction == "r":
#nach rechts verschieben, damit linie blau nicht 2 mal gezählt wird und crash auf innenecke kommt
            hsv_crop = hsv_img[hoehe - 30:hoehe, 120:260]
        else:
            hsv_crop = hsv_img[hoehe - 30:hoehe, 90:230]
    else:
        hsv_crop = hsv_img[50:round(hoehe/2), 90:230]
    
    
    if current_direction == "l":
        if (time.time() - linien_zeit) > linien_warten:
            linie = K.finde_blau(hsv_crop)
            if linie == True:
                linien_zeit = time.time()
                blaue_linie = True
                linie_imbild = True
                L.led_B1()
                if linien_counter == 12:
                    Rennen_laeuft = False #Rennen Ende erkannt, setze Stopsignal
        else:
            if blaue_linie and time.time() - linien_zeit > linien_zaehlen:
                linien_counter = linien_counter + 1
                #geradeaus = linien_counter*(-90)
                geradeaus =  geradeaus - 90
                blaue_linie = False
                linie_imbild = False
                L.led_B0()
                    
                    
    elif current_direction == "r":
        if (time.time() - linien_zeit) > linien_warten:
            linie = K.finde_orange(hsv_crop)
            if linie == True:
                linien_zeit = time.time()
                orange_linie = True
                linie_imbild = True
                L.led_O1()
                if linien_counter == 12:
                    Rennen_laeuft = False #Rennen Ende erkannt, setze Stopsignal
                    
            
        else:
            if orange_linie and time.time() - linien_zeit > linien_zaehlen:
                linien_counter = linien_counter + 1
                #geradeaus = linien_counter*(90)
                geradeaus = geradeaus + 90
                orange_linie = False
                linie_imbild = False
                L.led_O0()
        
    else:
        linie = K.finde_blau(hsv_crop)
        if linie == True:
            current_direction = "l"
            linien_zeit = time.time()
            #linien_counter = linien_counter + 1
            #geradeaus = linien_counter*(-90)
            blaue_linie = True
            print("Blau")
            
        else:
            linie = K.finde_orange(hsv_crop)
            if linie == True:
                current_direction = "r"
                linien_zeit = time.time()
                #linien_counter = linien_counter + 1
                #geradeaus = linien_counter*(90)
                orange_linie = True
                print("Orange")
#=============================Hauptprogram===============================================
try:
    if test:
        speed = 0.0
    F.gerade()
    L.leds_aus()
    L.led_startup()
    L.leds_aus()
    start_program()
#check for obstacle color behind car for u-turn
    hsv_frame, bgr_frame = K.get_image_back()
    x, y, s, farbe = K.finde_hindernisse(hsv_frame)
    if farbe == "R":
        Uturn = True
        Uturndetected = True
        endcounter = 4
        L.led_R1()
    elif farbe == "G":
        Uturndetected = True
        Uturn = False
        L.led_G1()
    
    F.vor(speed)
    
#====================Beginn der Hauptschleife=========================
    
    while not GPIO.input(BUTTON_PIN) and Rennen_laeuft:
        #abstand_R = Ultrasonic.distanz_R()
        #abstand_L = Ultrasonic.distanz_L()
        winkel, gesamt = G.Winkelmessen()
        hsv_frame, bgr_frame = K.get_image()
        hoehe = hsv_frame.shape[0] 
        
        
#--Wände finden + auswerten--
        links, rechts, hellL, hellR = K.waende(bgr_frame)
#--Magenta Wände finden + auswerten--
        linksMag, rechtsMag, hellLMag, hellRMag = K.waende_Magenta(hsv_frame)
        if current_direction == "r":
            if rechtsMag:
                rechtsMag = False #korektur, weil magenta kann nicht an der rechten wand stehen
        elif current_direction == "l":
            if linksMag:
                linksMag = False #korektur, weil magenta kann nicht an der linken wand stehen
        else:
            rechtsMag = False
            linksMag = False
            
        if rechtsMag:
            print(rechtsMag)
        if rechtsMag:
            print(linksMag)
#--Hindernisse finden + auswerten--
        x, y, s, farbe = K.finde_hindernisse(hsv_frame)
#--Linien suchen--
#====End Sequenz==================================================================
        linien_suchen(hsv_frame)
        if not Rennen_laeuft and not test:
            L.led_Y1()
            F.stop()
            F.gerade()
            F.ruck(0.5)
            time.sleep(1.1)
            F.stop()
            break
        
        elif NowUturn:
            L.led_W1()
            DoUturn()
            L.led_W0()
            
#==TEST==
        if test:
            if farbe == "R":
                cv2.line(bgr_frame, (x, 0), (x, hoehe), (0, 0, 255), 2)
            if farbe == "G":
                cv2.line(bgr_frame, (x, 0), (x, hoehe), (0, 255, 0), 2)
            cv2.imshow("Original", bgr_frame)
            cv2.waitKey(1)
            print("x: ", x)
            print("Y: ", y)
            print("S: ", s)
            print("Links: ", links)
            print("Rechts: ", rechts)
            print(linien_counter)
            print("Hinderniss_sperre",hindernis_sperre)
#==TEST=ENDE==
             
#----------------------Ende Linien/Wände/Hindernisse finden------------------------
        if (links or linksMag) and not (rechts):
            if gesamt <= geradeaus + 60.0:
                F.nach_rechts()
#Korrektur für Frontcrash
            else:
                F.nach_links()
            
        elif (rechts or rechtsMag) and not links:
            if gesamt >= geradeaus - 60.0:
                F.nach_links()
#Korrektur für Frontcrash           
            else:
                F.nach_rechts()
            
        elif rechts and links:
            
            if hellL > 14000 or hellR > 14000:
                if gesamt >= geradeaus:
                    F.nach_links()
                else:
                    F.nach_rechts()
                
                if U.distanz_V() < 5.0:
                    F.stop()
                    time.sleep(0.2)
                    if gesamt >= geradeaus:
                        F.ruck(speed)
                        F.nach_rechts()
                        time.sleep(0.8)
                        F.stop()
                        F.vor(speed)
                        F.gerade()
                    else:
                        F.ruck(speed)
                        F.nach_links()
                        time.sleep(0.8)
                        F.stop()
                        F.vor(speed)
                        F.gerade()
            
         
        else:
            if farbe == "R" and not linie_imbild:
            #if farbe == "R":
                if x > 0:
                    abstand = 0 - x
                    lenkwinkel = 93 + kh * (abstand)
                    if gesamt < geradeaus + 80:
                        F.steuern(lenkwinkel)
                    hindernis = True
                    h_zeit = time.time()
                    if current_direction == "r":
                        linien_zaehlen = linien_zaehlen_RR
                    elif current_direction == "l":
                        linien_zaehlen = linien_zaehlen_LR
                    
                else:
                    F.gerade()
                    h_zeit = time.time()
                    hindernis = True
                    
            elif farbe == "G" and not linie_imbild:
            #elif farbe == "G":
                if  x < 320 and x > 0:
                    abstand = 320 - x
                    lenkwinkel = 93 + kh * (abstand)
                    if gesamt > geradeaus - 80:
                        F.steuern(lenkwinkel)
                    hindernis = True
                    h_zeit = time.time()
                    if current_direction == "l":
                        linien_zaehlen = linien_zaehlen_LG
                    elif current_direction == "r":
                        linien_zaehlen = linien_zaehlen_RG
                    
                else:
                    F.gerade()
                    h_zeit = time.time()
                    hindernis = True
            
            else:
                if hindernis:
                    F.gerade()
                    hindernis_sperre = True
                    L.led_Y1()
                    if time.time() - h_zeit > h_warten:
                        hindernis = False
                else:
                    geradeaus_lenken()
                
                    
#-----------------------ENDE--------------------------
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
    