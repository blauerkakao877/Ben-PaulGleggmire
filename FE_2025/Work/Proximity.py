# Bibliotheken einbinden
import RPi.GPIO as GPIO
import time

# GPIO Modus (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# GPIO Pins zuweisen
#Rechts vorne
GPIO_RV = 4


GPIO.setup(GPIO_RV, GPIO.IN)


def proximity_alarm():

    alarm_RV = False
    #prüfe
    wert = GPIO.input(GPIO_RV)
    if wert == 0:
        alarm_RV = True
        
    return alarm_RV

if __name__ == '__main__':
    try:
        while True:
            alarm_RV = proximity_alarm()
            print("Hindernis rechts vorne: ", alarm_RV)
            time.sleep(0.1)

    # Beim Abbruch durch STRG+C resetten
    except KeyboardInterrupt:
        print("Messung vom User gestoppt")
        GPIO.cleanup()

