#imports
from adafruit_motorkit import MotorKit
from adafruit_servokit import ServoKit
import time
import board
import cv2
import RPi.GPIO as GPIO
import Fahren as F
import LED as L
import gyro as G
import numpy as np
import Kameramoduls_neu as K
import Ultrasonic as U

#Initialize MotorKit and ServoKit
Mkit = MotorKit(i2c=board.I2C())
Skit = ServoKit(channels=16)

#Constants and Variables
######################
#default
speed = 0.45
startspeed = 0.55
linien_zaehlen = 0.20     #wartezeit/Sperrzeit bis erste linie ausgewertet wird
linien_zaehlen_LG = 0.10  #Links+Grun
linien_zaehlen_RG = 0.01  #Rechts+Grun
linien_zaehlen_LR = 0.10  #Links+Rot
linien_zaehlen_RR = 0.01  #Rechts+Rot
linien_warten = 0.1       #vermeidet das linien mehrmals gezählt werden
h_warten = 0.75           #warten nach Hindernissen
#---------------------
#kopiervorlagen für versch geschwindigkeiten
#langsam
slow1 = False #True
speed1 = 0.45
startspeed1 = 0.55
linien_zaehlen1 =  0.20   #wartezeit bis linie ausgewertet wird
linien_zaehlen_LG1 = 0.10  #Links+Grun
linien_zaehlen_RG1 = 0.01  #Rechts+Grun
linien_zaehlen_LR1 = 0.10  #Links+Rot
linien_zaehlen_RR1 = 0.01  #Rechts+Rot
linien_warten1 = 0.1       #vermeidet das linien mehrmals gezählt werden
h_warten1 = 1.0           #warten nach Hindernissen

#mittel
mid2 = True #False
speed2 = 0.55
startspeed2 = 0.55
linien_zaehlen2 =  0.33   #wartezeit bis linie ausgewertet wird
linien_zaehlen_LG2 = 0.10  #Links+Grun
linien_zaehlen_RG2 = 0.01  #Rechts+Grun
linien_zaehlen_LR2 = 0.10  #Links+Rot
linien_zaehlen_RR2 = 0.01  #Rechts+Rot
linien_warten2 = 0.05       #vermeidet das linien mehrmals gezählt werden
h_warten2 = 0.7           #warten nach Hindernissen

#schnell !!!ACHTUNG UNSICHER!!!
fast3 = False
speed3 = 0.60
startspeed3 = 0.65
linien_zaehlen3 =  0.28   #0.4 #0.21 #wartezeit bis linie ausgewertet wird
linien_zaehlen_LG3 = 0.10  #Links+Grun
linien_zaehlen_RG3 = 0.01  #Rechts+Grun
linien_zaehlen_LR3 = 0.10  #Links+Rot
linien_zaehlen_RR3 = 0.01  #Rechts+Rot
linien_warten3 = 1.0       #vermeidet das linien mehrmals gezählt werden
h_warten3 = 0.75           #warten nach Hindernissen
######################

# Hardware-Pins
BUTTON_PIN = 16  
# Fahrzeugbewegung & Steuerung  
steerangle = 95  
steeringpoint = 60  
servmitte = 95  
Seitehalten = 0  
geradeaus = 0  
# Sensordaten  
hellL = 0  
hellR = 0  
abstand = 0  
# Linienverfolgung  
linien_counter = 0  
linien_zeit = 0  
# Zeitsteuerung  
h_zeit = 0.0  
stop_time = time.time() + 18000.0  
park_stop_time = time.time() + 18000.0  
# Regelungsfaktoren  
k = 0.6    # Standard-Faktor für Gerade  
kh = 0.35  # Standard-Faktor für Hindernisse  
# Sonstige Variablen  
gesamt = 0.0  
hoehe = 210  
breite = 320  
s = 0  
x = 0  
y = 0  


current_direction = "n"
farbe = "N"
letzte_farbe = "N"

linie = False
links = False
rechts = False
blaue_linie = False
orange_linie = False
hindernis = False
Rennen_laeuft = True
hindernis_sperre = False
linie_imbild = False
reduced = False
park_runde = False
linie_korrigiert = False

#====TEST====
test = False
#====Parken====
parken = True

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN)


#======================================================================
#-------------------- functions / procedures --------------------
#======================================================================

def start_program():
    global stop_time
    global park_stop_time
    
    G.gyro_start()
    K.init("obstacle")
    hindernis_sperre = False
    L.led_Y1()
    
    if slow1:
        speed = speed1
        startspeed = startspeed1
        linien_zaehlen = linien_zaehlen1
        linien_zaehlen_LG = linien_zaehlen_LG1 
        linien_zaehlen_RG = linien_zaehlen_RG1
        linien_zaehlen_LR = linien_zaehlen_LR1
        linien_zaehlen_RR = linien_zaehlen_RR1
        linien_warten = linien_warten1
        h_warten = h_warten1
        L.led_R1()
    if mid2:
        speed = speed2
        startspeed = startspeed2
        linien_zaehlen = linien_zaehlen2
        linien_zaehlen_LG = linien_zaehlen_LG2 
        linien_zaehlen_RG = linien_zaehlen_RG2
        linien_zaehlen_LR = linien_zaehlen_LR2
        linien_zaehlen_RR = linien_zaehlen_RR2
        linien_warten = linien_warten2
        h_warten = h_warten2
        L.led_G1()
    if fast3:
        speed = speed3
        startspeed = startspeed3
        linien_zaehlen = linien_zaehlen3
        linien_zaehlen_LG = linien_zaehlen_LG3
        linien_zaehlen_RG = linien_zaehlen_RG3
        linien_zaehlen_LR = linien_zaehlen_LR3
        linien_zaehlen_RR = linien_zaehlen_RR3
        linien_warten = linien_warten3
        h_warten = h_warten3
        L.led_B1()
    
    print("--Press button to start--")
    while not GPIO.input(BUTTON_PIN):
        time.sleep(0.1)
    L.led_Y0()
    while GPIO.input(BUTTON_PIN):
        time.sleep(0.1)
    print("Program started!")
    time.sleep(0.5)
    stop_time = time.time() + 18000.0
    park_stop_time = time.time() + 18000.0
#-------------------------------------------
def stop_program():
    F.stop()
    F.gerade()
    L.led_ende()
    L.led_R1()
    L.led_G1()
#-------------------------------------------
def geradeaus_lenken():
    global geradeaus
    global gesamt
    winkel, gesamt = G.Winkelmessen()
    lenkwinkel = 95 + k * (gesamt - geradeaus)
    F.steuern(lenkwinkel)
#-------------------------------------------
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
    global speed
    global reduced
    global stop_time
    global linie_korrigiert
    
    if linien_counter == 12:
        if not reduced:
            speed = speed*1.0
            F.vor(speed)
            reduced = True
            stop_time = time.time() + 3.0
            
            if letzte_farbe == "G":
                if current_direction == "l":
                    stop_time = time.time() + 2.2
                elif current_direction == "r":
                    stop_time = time.time() + 3.5
                    
            elif letzte_farbe == "R":
                if current_direction == "l":
                    stop_time = time.time() + 3.5
                elif current_direction == "r":
                    stop_time = time.time() + 2.5


    if  (linien_counter == 8) or (linien_counter == 12):
        hsv_crop = hsv_img[50:round(hoehe/2), 90:230]
        
    else:
        if current_direction == "l":
#nach links verschieben, damit linie orange nicht 2 mal gezählt wird und crash auf innenecke kommt
            hsv_crop = hsv_img[hoehe - 30:hoehe, 60:200]
        elif current_direction == "r":
#nach rechts verschieben, damit linie blau nicht 2 mal gezählt wird und crash auf innenecke kommt
            hsv_crop = hsv_img[hoehe - 30:hoehe, 120:260]
        else:
            hsv_crop = hsv_img[hoehe - 60:hoehe, 90:230]
   
    if current_direction == "l":
        if (time.time() - linien_zeit) > linien_warten:
            linie = K.finde_blau(hsv_crop)
            if linie == True:
                linien_zeit = time.time()
                blaue_linie = True
                linie_imbild = True
                linie_korrigiert = False
                L.led_B1()

        else:
            if blaue_linie and time.time() - linien_zeit > linien_zaehlen:
                linien_counter = linien_counter + 1
                L.led_B1()
                #geradeaus = linien_counter*(-90)
                geradeaus =  geradeaus - 90
                blaue_linie = False
                linie_imbild = False
                linie_korrigiert = False
                L.led_B0()
                    
    elif current_direction == "r":
        if (time.time() - linien_zeit) > linien_warten:
            linie = K.finde_orange(hsv_crop)
            if linie == True:
                linien_zeit = time.time()
                orange_linie = True
                linie_imbild = True
                linie_korrigiert = False
                L.led_O1()
        else:
            if orange_linie and time.time() - linien_zeit > linien_zaehlen:
                linien_counter = linien_counter + 1
                L.led_O1()
                #geradeaus = linien_counter*(90)
                geradeaus = geradeaus + 90
                orange_linie = False
                linie_imbild = False
                linie_korrigiert = False
                L.led_O0()
    else:
        b_linie = K.finde_blau(hsv_crop)
        o_linie = K.finde_orange(hsv_crop)
        crop_start = 50
        
        while o_linie and b_linie:
            #2 Linien im Bild
            crop_start = crop_start - 10
            hsv_crop = hsv_img[hoehe - crop_start:hoehe, 90:230]
            
        if b_linie == True:
            L.led_B1()
            current_direction = "l"
            if letzte_farbe == "G":
                linien_zaehlen = linien_zaehlen_LG
            elif letzte_farbe == "R":
                linien_zaehlen = linien_zaehlen_RR
            linien_zeit = time.time()
            blaue_linie = True
            print("Blau")
        else:
            if o_linie == True:
                L.led_O1()
                current_direction = "r"
                if letzte_farbe == "G":
                    linien_zaehlen =linien_zaehlen_RG
                elif letzte_farbe == "R":
                    linien_zaehlen = linien_zaehlen_RR
                linien_zeit = time.time()
                orange_linie = True
                print("Orange")
#-------------------------------------------
def messen():
    global winkel
    global gesamt
    global hsv_frame
    global bgr_frame
    global hoehe
    global linien_counter
    global links
    global rechts
    global hellL
    global hellR
    global linksMag
    global rechtsMag
    global hellLMag
    global hellRMag
    global current_direction
    global x
    global y
    global s
    global farbe
    
    #abstand_R = Ultrasonic.distanz_R()
    #abstand_L = Ultrasonic.distanz_L()
    winkel, gesamt = G.Winkelmessen()
    hsv_frame, bgr_frame = K.get_image()
    hoehe = hsv_frame.shape[0]
    
# setting speed higher after first corner 
    if linien_counter > 0:
        F.vor(speed)
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
#-------------------------------------------
def einparken():
    global current_direction
    global gesamt
    global geradeaus
    eingeparkt = False
    linksMag = False
    rechtsMag = False
    hellLMag = 0
    hellRMag = 0
    ziel_winkel = 0.0
    
    
    F.stop()
    time.sleep(1.0)
    if current_direction == "l":
        F.nach_links()
        F.ruck(0.3)
        time.sleep(1.5)
        F.stop()
        time.sleep(0.1)
        F.vor(0.3)
        F.nach_rechts()
        while gesamt < geradeaus + 75 or U.distanz_V() < 7.0:
            time.sleep(0.1)
            winkel, gesamt = G.Winkelmessen()
        F.gerade()
  
        while U.distanz_V() > 5.0:
            time.sleep(0.1)
        time.sleep(0.3)
        F.stop()
        time.sleep(0.1)
        F.ruck(0.3)
        
        while U.distanz_V() < 11.0:
            time.sleep(0.1)
        F.nach_rechts()
        
        while gesamt > geradeaus:
            time.sleep(0.1)
            winkel, gesamt = G.Winkelmessen()
        F.stop()
        F.vor(0.3)
        F.gerade()
        
        hsv_frame, bgr_frame = K.get_image_back()
        linksMag, rechtsMag, hellLMag, hellRMag = K.waende_Magenta(hsv_frame)
        while hellLMag < 4500:
            geradeaus_lenken()
            hsv_frame, bgr_frame = K.get_image_back()
            linksMag, rechtsMag, hellLMag, hellRMag = K.waende_Magenta(hsv_frame)
        F.stop()
        time.sleep(0.5)
        F.gerade()
        F.ruck(0.3)
        time.sleep(0.45)
        F.stop()
        F.parken_rechts()
        F.ruck(0.3)
        
    elif current_direction == "r":
        F.vor(0.3)
        F.nach_links()
        while gesamt > geradeaus -85:
            time.sleep(0.1)
            winkel, gesamt = G.Winkelmessen()
        F.gerade()
        
        while U.distanz_V() > 5.0:
            time.sleep(0.1)
        time.sleep(0.5)
        F.stop()
        F.ruck(0.3)
        
        while U.distanz_V() < 8.0:
            time.sleep(0.1)
        F.nach_links()
        
        while gesamt < geradeaus:
            time.sleep(0.1)
            winkel, gesamt = G.Winkelmessen()
        F.stop()
        F.vor(0.3)
        F.gerade()
        
        hsv_frame, bgr_frame = K.get_image_back()
        linksMag, rechtsMag, hellLMag, hellRMag = K.waende_Magenta(hsv_frame)
        while hellRMag < 5000:
            geradeaus_lenken()
            hsv_frame, bgr_frame = K.get_image_back()
            linksMag, rechtsMag, hellLMag, hellRMag = K.waende_Magenta(hsv_frame)
        F.stop()
        time.sleep(0.5)
        F.gerade()
        F.ruck(0.3)
        time.sleep(0.8)
        F.stop()
        F.parken_links()
        F.ruck(0.3)
        
    while hellLMag < 20000 and hellRMag < 20000:
        hsv_frame, bgr_frame = K.get_image_back()
        linksMag, rechtsMag, hellLMag, hellRMag = K.waende_Magenta(hsv_frame)
    F.stop()
    
    if current_direction == "l":
        F.parken_links()
        F.vor(0.1)
    elif current_direction == "r":
        F.parken_rechts()
        F.vor(0.1)
    time.sleep(0.2)
    F.stop()
    F.gerade()
    F.ruck(0.3)
        
    while not eingeparkt:
        hsv_frame, bgr_frame = K.get_image_back()
        linksMag, rechtsMag, hellLMag, hellRMag = K.waende_Magenta(hsv_frame)
        parken_hellL, parken_hellR = K.parken_waende(bgr_frame)
        
        #if parken_hellL > parken_hellR:
        if hellLMag > hellRMag:
            F.nach_links()
        else:
            F.nach_rechts()
        
        if parken_hellL > 35000 or parken_hellR > 35000:
            F.stop()
            F.gerade()
            F.ruck(0.3)
            time.sleep(0.4)
            eingeparkt = True
#-------------------------------------------

#======================================================================
#=============================-   mainprogram-============================
#======================================================================     
#--------------------------------setup---------------------------------

try:
    if test:
        speed = 0.0
        startspeed = 0.0
        print("!!Running-in-Test-Mode!!")
    F.gerade()
    L.leds_aus()
    L.led_obstaclerace()
    L.leds_aus()
    start_program()
    hsv_frame, bgr_frame = K.get_image_back()
    x, y, s, farbe = K.finde_hindernisse(hsv_frame)
    
    if time.time() > linien_zeit + 10.0:
        linie_uebersehen()
        
    F.anfahren(startspeed)
    F.vor(startspeed)

#====================-main-loop-=========================
