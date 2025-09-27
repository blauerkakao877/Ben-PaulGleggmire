# Bibliotheken einbinden
import RPi.GPIO as GPIO
import time
import LED as L

# GPIO Modus (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#GPIO Pins zuweisen
#Rechts vorne
GPIO_HL = 5
GPIO_VL = 6
GPIO_HR = 22
GPIO_VR = 26
GPIO_HM = 4


GPIO.setup(GPIO_HL, GPIO.IN)
GPIO.setup(GPIO_VL, GPIO.IN)
GPIO.setup(GPIO_HR, GPIO.IN)
GPIO.setup(GPIO_VR, GPIO.IN)
GPIO.setup(GPIO_HM, GPIO.IN)

def prox_alarm():

    alarm_HL = False
    alarm_VL = False
    alarm_HR = False
    alarm_VR = False
    alarm_HM = False
    
    wertHL = GPIO.input(GPIO_HL)
    wertVL = GPIO.input(GPIO_VL)
    wertHR = GPIO.input(GPIO_HR)
    wertVR = GPIO.input(GPIO_VR)
    wertHM = GPIO.input(GPIO_HM)
    
    if wertHL == 1:
        alarm_HL = True
        L.led_W21()
    else:
        alarm_HL = False
        L.led_W20()
#---------------------------  
    if wertVL == 1:
        alarm_VL = True
        L.led_W21()
    else:
        alarm_VL = False
        L.led_W20()
#---------------------------  
    if wertHR == 1:
        alarm_HR = True
        L.led_W21()
    else:
        alarm_HR = False
        L.led_W20()
#---------------------------  
    if wertVR == 1:
        alarm_VR = True
        L.led_W21()
    else:
        alarm_VR = False
        L.led_W20()
#---------------------------  
    if wertHM == 1:
        alarm_HM = True
        L.led_W21()
    else:
        alarm_HM = False
        L.led_W20()
        
        
    return alarm_HL, alarm_VL, alarm_HR, alarm_VR, alarm_HM

if __name__ == '__main__':
    try:
        while True:
            alarm_HL, alarm_VL, alarm_HR, alarm_VR, alarm_HM = prox_alarm()
            print("Hindernis HL-VL-HR-VR-HM: ", alarm_HL, alarm_VL, alarm_HR, alarm_VR, alarm_HM)
            time.sleep(0.1)

    # Beim Abbruch durch STRG+C resetten
    except KeyboardInterrupt:
        print("Messung vom User gestoppt")
        GPIO.cleanup()
