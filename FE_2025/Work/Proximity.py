# Bibliotheken einbinden
import RPi.GPIO as GPIO
import time
import LED as L

# GPIO Modus (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# GPIO Pins zuweisen
#Rechts vorne
GPIO_HL = 5
GPIO_VL = 6
#GPIO_V = 12

GPIO.setup(GPIO_HL, GPIO.IN)
GPIO.setup(GPIO_VL, GPIO.IN)
#GPIO.setup(GPIO_V, GPIO.IN)

def prox_alarm():

    alarm_HL = False
    alarm_VL = False
    #alarm_V = False
    wertHL = GPIO.input(GPIO_HL)
    wertVL = GPIO.input(GPIO_VL)
    #wertM = GPIO.input(GPIO_V)
    
    if wertHL == 0:
        alarm_HL = True
        L.led_W21()
    else:
        alarm_HL = False
        L.led_W20()
        
    if wertVL == 0:
        alarm_VL = True
        
    #if wertM == 0:
        #alarm_V = True
        
    return alarm_HL, alarm_VL

if __name__ == '__main__':
    try:
        while True:
            alarm_HL, alarm_VL = prox_alarm()
            print("Hindernis HL-VL: ", alarm_HL, alarm_VL,)
            time.sleep(0.1)

    # Beim Abbruch durch STRG+C resetten
    except KeyboardInterrupt:
        print("Messung vom User gestoppt")
        GPIO.cleanup()






