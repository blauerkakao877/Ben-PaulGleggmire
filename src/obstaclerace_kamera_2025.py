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
import Write_Logfile as W
import sys


# Initialize MotorKit and ServoKit
Mkit = MotorKit(i2c=board.I2C())
Skit = ServoKit(channels=16)

# Constants and Variables
speed = 0.57
startspeed = 0.57
steerangle = 95
k = 0.6   #Adjust as needed standard faktor fuer gerade
kh = 0.35  #Adjust as needed faktor fuer hindernisse
Seitehalten = 0
BUTTON_PIN = 16
servmitte = 95
geradeaus = 0
current_direction = "n"
linie = False
linien_zeit = 0
linien_warten = 2.4 #vermeidet das linien mehrmals gezählt werden
linien_counter = 0
x = 0
y = 0
s = 0
farbe = "N"
letzte_farbe = "N"
links = False
rechts = False
hellL = 0
hellR = 0
abstand = 0
linien_zaehlen = 0.10 #wartezeit/Sperrzeit bis erste linie ausgewertet wird
linien_zaehlen_LG = 0.10  #Links+Grun
linien_zaehlen_RG = 0.01  #Rechts+Grun
linien_zaehlen_LR = 0.10  #Links+Rot
linien_zaehlen_RR = 0.01  #Rechts+Rot
blaue_linie = False
orange_linie = False
hindernis = False
h_warten = 0.75
h_zeit = 0.0
gesamt = 0.0
Rennen_laeuft = True
hoehe = 210
breite = 320
hindernis_sperre = False
linie_imbild = False
stop_time = time.time() + 18000.0
reduced = False
park_runde = False
park_stop_time = time.time() + 18000.0
linie_korrigiert = False
steeringpoint = 60
#==TEST==
test = False
#==Parken==
parken = True

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN)

#======================================================================
#-------------------- functions /  procedures --------------------
#======================================================================

# Function to start the program
def start_program():
    
    global stop_time
    global park_stop_time
    
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
    W.write_Log("program_started")
    time.sleep(0.5)
    stop_time = time.time() + 18000.0
    park_stop_time = time.time() + 18000.0

    
def stop_program():
    F.stop()
    F.gerade()
    L.led_ende()
    L.led_R1()
    L.led_G1()
    W.close_Log()
    sys.exit()

def geradeaus_lenken():
    global geradeaus
    global gesamt
    winkel, gesamt = G.Winkelmessen()
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


    if  (linien_counter == 12) or (linien_counter == 8):
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
                #if linien_counter == 12:
                    #Rennen_laeuft = False #Rennen Ende erkannt, setze Stopsignal

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
                
#-----------------------------------------------------
                
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
    
#------------------------------------------------------------
    
def linie_uebersehen():
    global linien_counter
    global linien_zeit
    global geradeaus
    global linie_imbild
    global blaue_linie
    global linie_korrigiert

    if not linie_korrigiert:
        if current_direction == "l":
            linien_counter = linien_counter + 1        
            geradeaus =  geradeaus - 90
            blaue_linie = False
            linie_imbild = False
            
        elif current_direction == "r":
            linien_counter = linien_counter + 1        
            geradeaus =  geradeaus + 90
            blaue_linie = False
            linie_imbild = False
            
        linien_zeit = time.time() - 2.0
        linie_korrigiert = True

#------------------------------------------------------------
    
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

#======================================================================
#============================= mainprogram ============================
#======================================================================     
#--------------------------------setup---------------------------------
try:
    if test:
        speed = 0.0
    W.open_Log(True)
    F.gerade()
    L.leds_aus()
    L.led_startup()
    L.leds_aus()
    start_program()
#check for obstacle color behind car for u-turn
    hsv_frame, bgr_frame = K.get_image_back()
    x, y, s, farbe = K.finde_hindernisse(hsv_frame)
    
    if time.time() > linien_zeit + 10.0:
        linie_uebersehen()
        
    F.anfahren(startspeed)
    F.vor(startspeed)

#==================== main loop =========================
    
    while not GPIO.input(BUTTON_PIN) and Rennen_laeuft:
        if time.time() > stop_time and not park_runde:
            if parken:
                if not park_runde:
                    F.stop()
                    L.led_countdown5()
                    time.sleep(0.5)
                    #check for obstacle too near
                    x = 160
                    messen()
                    if current_direction == "r":
                       if x < 160:
                            F.gerade()
                            F.ruck(0.3)
                            time.sleep(1.0)
                            F.stop()
                            
                    if current_direction == "l":
                        if x > 160:
                            F.gerade()
                            F.ruck(0.3)
                            time.sleep(1.0)
                            F.stop()
                        
                    F.anfahren(speed)
                    F.vor(speed)
                    park_runde = True
            else:
                Rennen_laeuft = False
        if park_runde and time.time() > park_stop_time:
            F.stop()
            time.sleep(0.2)
            L.led_G21()
            L.led_R21()
            L.led_W1()
            einparken()
            break
            
        messen()
        linien_suchen(hsv_frame)
            
        if not Rennen_laeuft and not test:
            L.led_Y1()
            F.stop()
            F.gerade()
            #F.ruck(0.7)
            #time.sleep(1.2)
            #F.stop()
            break
            
#==TEST==
        if test:
            W.write_Log("started_in_testmode")
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
            
#...berechne ab hier Lenkung...
            
        if park_runde:
            if current_direction == "r":
                if farbe == "R":
                    farbe = "G"
            elif current_direction == "l":
                if farbe == "G":
                    farbe = "R"
            
            if hellLMag > 10000 or hellRMag > 10000:
                if current_direction == "l":
                    park_stop_time = time.time() + 0.0
                elif current_direction == "r":
                    park_stop_time = time.time() + 0.0
            
        if hellLMag > 9600 and hellRMag > 9600:
            if current_direction == "l":
                F.nach_links()
            elif current_direction == "r":
                F.nach_rechts()
        elif (links or linksMag) and not (rechts):
            if gesamt <= geradeaus + 60.0:
                F.nach_rechts()
#Korrektur für sidecrash
            else:
                F.nach_links()
            
        elif (rechts or rechtsMag) and not links:
            if gesamt >= geradeaus - 60.0:
                F.nach_links()
#Korrektur für sidecrash           
            else:
                F.nach_rechts()
            
        elif rechts and links:
#frontcrash
            if hellL > 13000 or hellR > 13000:
                if gesamt >= geradeaus:
                    F.nach_links()
                else:
                    F.nach_rechts()
                
                if U.distanz_V() < 5.0:
                    F.stop()
                    time.sleep(0.2)
#check ob linie verpasst
                        
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
            if farbe == "R" and not linie_imbild:
                letzte_farbe = farbe
                L.led_W0()
                
                if s < 50:
                    steeringpoint = 110
                elif s < 70:
                    steeringpoint = 60
                elif s < 100:
                    steeringpoint = 30
                    
                if s >= 100:
                    F.ausweichen_rechts()
                    hindernis = True
                    h_zeit = time.time()

                elif x > steeringpoint:
                    abstand = steeringpoint - x
                    lenkwinkel = 95 + kh * (abstand)
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
                letzte_farbe = farbe
                L.led_W0()
                
                if s < 50:
                    steeringpoint = 110
                elif s < 70:
                    steeringpoint = 60
                elif s < 100:
                    steeringpoint = 30
                    
                if s >= 100:
                    F.ausweichen_links()
                    h_zeit = time.time()
                elif  x < 320 - steeringpoint and x > 0:
                    abstand = 320 - steeringpoint - x
                    lenkwinkel = 95 + kh * (abstand)
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
                L.led_W1()
                if hindernis:
                    F.gerade()
                    hindernis_sperre = True
                    if time.time() - h_zeit > h_warten:
                        hindernis = False
                else:      #nichts wichtiges in Sicht
                    #if hellR > 6500:
                     #   F.nach_links()
                    #elif hellL > 6500:
                     #   F.nach_rechts()
                    #else:
                    geradeaus_lenken()
                    
#-----------------------END--------------------------
    stop_program()
    

except KeyboardInterrupt:
    F.gerade()
    F.stop()
    L.leds_aus()
    print("Program stopped by the user.")
    
