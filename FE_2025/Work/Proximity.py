# Bibliotheken einbinden
import RPi.GPIO as GPIO
import time

# GPIO Modus (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# GPIO Pins zuweisen
#Rechts vorne
GPIO_RV = 4
GPIO_LV = 17
GPIO_V = 12

GPIO.setup(GPIO_RV, GPIO.IN)
GPIO.setup(GPIO_LV, GPIO.IN)
GPIO.setup(GPIO_V, GPIO.IN)


def prox_alarm():

    alarm_RV = False
    alarm_LV = False
    alarm_V = False
    wertR = GPIO.input(GPIO_RV)
    wertL = GPIO.input(GPIO_LV)
    wertM = GPIO.input(GPIO_V)
    
    if wertR == 0:
        alarm_RV = True
        
    if wertL == 0:
        alarm_LV = True
        
    if wertM == 0:
        alarm_V = True
        
    return alarm_RV, alarm_LV, alarm_V

if __name__ == '__main__':
    try:
        while True:
            alarm_RV, alarm_LV, alarm_V = prox_alarm()
            print("Hindernis rechts-links-vorne: ", alarm_RV, alarm_LV, alarm_V)
            time.sleep(0.1)

    # Beim Abbruch durch STRG+C resetten
    except KeyboardInterrupt:
        print("Messung vom User gestoppt")
        GPIO.cleanup()

