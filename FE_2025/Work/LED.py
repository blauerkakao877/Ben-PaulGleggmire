import time
import board
import RPi.GPIO as GPIO
from adafruit_servokit import ServoKit

Skit = ServoKit(channels=16)


# =====================================================
    
def led_R0():
    Skit.servo[3].angle = None
        
        
def led_R1():
    Skit.servo[3].angle = 50
        
#=====================================================    
        
def led_G0():
    Skit.servo[4].angle = None
        
        
def led_G1():
    Skit.servo[4].angle = 50
        
#===================================================== 
        
def led_B0():
    Skit.servo[5].angle = None
        
        
def led_B1():
    Skit.servo[5].angle = 50
        
#=====================================================

def led_W0():
    Skit.servo[7].angle = None
        
        
def led_W1():
    Skit.servo[7].angle = 90

#=====================================================

def led_Y0():
    Skit.servo[8].angle = None
        
        
def led_Y1():
    Skit.servo[8].angle = 80
        
#=====================================================

def led_O0():
    Skit.servo[6].angle = None
        
        
def led_O1():
    Skit.servo[6].angle = 50
        
#=====================================================

def led_G20():
    Skit.servo[13].angle = None
        
        
def led_G21():
    Skit.servo[13].angle = 50
        
#=====================================================

def led_R20():
    Skit.servo[12].angle = None
        
        
def led_R21():
    Skit.servo[12].angle = 50
        
#=====================================================

def leds_an():
    led_W1()
    led_R1()
    led_B1()
    led_G1()
    led_Y1()
    led_O1()
    led_G21()
    led_R21()
        
#++++++++++++++++++++++++++++++++++++++++++++++++++++
        
def leds_aus():
    led_W0()
    led_R0()
    led_B0()
    led_G0()
    led_Y0()
    led_O0()
    led_G20()
    led_R20()
        
#++++++++++++++++++++++++++++++++++++++++++++++++++++
        
def led_start():
    led_W0()
    led_R0()
    led_B0()
    led_G0()
    led_Y0()
    led_O0()
    led_G20()
    led_R20()
        
        
    led_R1()
    time.sleep(0.1)
    led_R0()
    led_G1()
    time.sleep(0.1)
    led_G0()
    led_B1()
    time.sleep(0.1)
    led_B0()
    led_O1()
    time.sleep(0.1)
    led_O0()
    led_R21()
    time.sleep(0.1)
    led_R20()
    led_G21()
    time.sleep(0.1)
    led_R20()
    led_W1()
    time.sleep(0.1)
    led_W0()
    led_Y1()
    time.sleep(0.1)
    led_Y0()
    led_W1()
    time.sleep(0.1)
    led_W0()
    led_G21()
    time.sleep(0.1)
    led_G20()
    led_R21()
    time.sleep(0.1)
    led_R20()
    led_O1()
    time.sleep(0.1)
    led_O0()
    led_B1()
    time.sleep(0.1)
    led_B0()
    led_G1()
    time.sleep(0.1)
    led_G0()
    led_R1()
    time.sleep(0.1)
    led_R0()
    led_R1()
    time.sleep(0.1)
    led_R0()
    led_G1()
    time.sleep(0.1)
    led_G0()
    led_B1()
    time.sleep(0.1)
    led_B0()
    led_O1()
    time.sleep(0.1)
    led_O0()
    led_R21()
    time.sleep(0.1)
    led_R20()
    led_G21()
    time.sleep(0.1)
    led_R20()
    led_W1()
    time.sleep(0.1)
    led_W0()
    led_Y1()
    time.sleep(0.1)
    led_Y0()
    led_W1()
    time.sleep(0.1)
    led_W0()
    led_G21()
    time.sleep(0.1)
    led_G20()
    led_R21()
    time.sleep(0.1)
    led_R20()
    led_O1()
    time.sleep(0.1)
    led_O0()
    led_B1()
    time.sleep(0.1)
    led_B0()
    led_G1()
    time.sleep(0.1)
    led_G0()
    led_R1()
    time.sleep(0.1)
    led_R0()
        
#++++++++++++++++++++++++++++++++++++++++++++++++++++

def led_blink():
    leds_aus()
    time.sleep(0.2)
    leds_an()
    time.sleep(0.2)
    leds_aus()
    time.sleep(0.2)
    leds_an()
    time.sleep(0.2)
    leds_aus()
    time.sleep(0.2)
    leds_an()
    time.sleep(0.2)
    leds_aus()
    time.sleep(0.2)
    leds_an()
    time.sleep(0.2)
    leds_aus()
    time.sleep(0.2)
    leds_an()
    time.sleep(0.2)
    leds_aus()
    
#++++++++++++++++++++++++++++++++++++++++++++++++++++

def led_flow():
    led_R1()
    time.sleep(0.1)
    led_G1()
    led_R0()
    time.sleep(0.1)
    led_B1()
    led_G0()
    time.sleep(0.1)
    led_O1()
    led_B0()
    time.sleep(0.1)
    led_W1()
    led_O0()
    time.sleep(0.1)
    led_Y1()
    led_W0()
    time.sleep(0.1)
    led_Y0()
    time.sleep(0.3)
    led_R1()
    time.sleep(0.1)
    led_G1()
    led_R0()
    time.sleep(0.1)
    led_B1()
    led_G0()
    time.sleep(0.1)
    led_O1()
    led_B0()
    time.sleep(0.1)
    led_W1()
    led_O0()
    time.sleep(0.1)
    led_Y1()
    led_W0()
    time.sleep(0.1)
    led_Y0()
    time.sleep(0.3)
    led_R1()
    time.sleep(0.1)
    led_G1()
    led_R0()
    time.sleep(0.1)
    led_B1()
    led_G0()
    time.sleep(0.1)
    led_O1()
    led_B0()
    time.sleep(0.1)
    led_W1()
    led_O0()
    time.sleep(0.1)
    led_Y1()
    led_W0()
    time.sleep(0.1)
    led_Y0()
    time.sleep(0.3)
    led_R1()
    time.sleep(0.1)
    led_G1()
    led_R0()
    time.sleep(0.1)
    led_B1()
    led_G0()
    time.sleep(0.1)
    led_O1()
    led_B0()
    time.sleep(0.1)
    led_W1()
    led_O0()
    time.sleep(0.1)
    led_Y1()
    led_W0()
    time.sleep(0.1)
    led_Y0()
    time.sleep(0.3)
        
#++++++++++++++++++++++++++++++++++++++++++++++++++++ 

def led_startup():
    led_start()
    time.sleep(0.2)
    led_blink()

#++++++++++++++++++++++++++++++++++++++++++++++++++++ 

def led_ende():
    leds_an()
    time.sleep(0.5)
    leds_aus()
    time.sleep(0.5)
    leds_an()
    time.sleep(0.5)
    leds_aus()

#++++++++++++++++++++++++++++++++++++++++++++++++++++ 

def led_countdown5():
    leds_aus()
    time.sleep(0.1)
    led_Y1()
    time.sleep(1.0)
    led_W1()
    time.sleep(1.0)
    led_G21()
    time.sleep(1.0)
    led_R21()
    time.sleep(1.0)
    led_O1()
    time.sleep(1.0)
    leds_aus()
    led_Y1()


#++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    
def led_countdown3():
    leds_aus()
    time.sleep(0.1)
    led_Y1()
    time.sleep(1.0)
    led_W1()
    time.sleep(1.0)
    led_G21()
    time.sleep(1.0)
    leds_aus()
    led_Y1()


#++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    
def led_obstaclerace():
    leds_aus()
    led_R1()
    led_Y1()
    time.sleep(0.1)
    led_Y0()
    led_R0()
    led_G1()
    led_W1()
    time.sleep(0.1)
    led_G0()
    led_W0()
    led_B1()
    led_G21()
    time.sleep(0.1)
    led_B0()
    led_G20()
    led_O1()
    led_R21()
    time.sleep(0.1)
    led_O0()
    led_R20()
    led_B1()
    led_G21()
    time.sleep(0.1)
    led_B0()
    led_G20()
    led_G1()
    led_W1()
    time.sleep(0.1)
    led_G0()
    led_W0()
    led_R1()
    led_Y1()
    time.sleep(0.1)
    led_R1()
    led_Y1()
    time.sleep(0.1)
    led_Y0()
    led_R0()
    led_G1()
    led_W1()
    time.sleep(0.1)
    led_G0()
    led_W0()
    led_B1()
    led_G21()
    time.sleep(0.1)
    led_B0()
    led_G20()
    led_O1()
    led_R21()
    time.sleep(0.1)
    led_O0()
    led_R20()
    led_B1()
    led_G21()
    time.sleep(0.1)
    led_B0()
    led_G20()
    led_G1()
    led_W1()
    time.sleep(0.1)
    led_G0()
    led_W0()
    led_R1()
    led_Y1()
    time.sleep(0.1)
    led_R1()
    led_Y1()
    time.sleep(0.1)
    led_Y0()
    led_R0()
    led_G1()
    led_W1()
    time.sleep(0.1)
    led_G0()
    led_W0()
    led_B1()
    led_G21()
    time.sleep(0.1)
    led_B0()
    led_G20()
    led_O1()
    led_R21()
    time.sleep(0.1)
    led_O0()
    led_R20()
    led_B1()
    led_G21()
    time.sleep(0.1)
    led_B0()
    led_G20()
    led_G1()
    led_W1()
    time.sleep(0.1)
    led_G0()
    led_W0()
    led_R1()
    led_Y1()
    time.sleep(0.1)
    led_R1()
    led_Y1()
    time.sleep(0.1)
    led_Y0()
    led_R0()
    led_G1()
    led_W1()
    time.sleep(0.1)
    led_G0()
    led_W0()
    led_B1()
    led_G21()
    time.sleep(0.1)
    led_B0()
    led_G20()
    led_O1()
    led_R21()
    time.sleep(0.1)
    led_O0()
    led_R20()
    led_B1()
    led_G21()
    time.sleep(0.1)
    led_B0()
    led_G20()
    led_G1()
    led_W1()
    time.sleep(0.1)
    led_G0()
    led_W0()
    led_R1()
    led_Y1()
    time.sleep(0.1)
    leds_aus()
    led_blink()


#++++++++++++++++++++++++++++++++++++++++++++++++++++

def  led_test():
    Skit.servo[13].angle = None
    time.sleep(1.0)
    Skit.servo[13].angle = 50
    time.sleep(1.0)
    Skit.servo[13].angle = None
    time.sleep(1.0)
    Skit.servo[13].angle = 50
    time.sleep(1.0)
    Skit.servo[13].angle = None
    print("Test beendet")
    
#Reihenfolge der Led's: RGBOWY
def  led_test_R2():
    print("Test R2")
    time.sleep(0.5)
    led_R21()
    time.sleep(1.0)
    led_R20()
    time.sleep(1.0)
    led_R21()
    time.sleep(1.0)
    led_R20()
    print("Test R2 done")

        
def  led_test_G2():
    print("Test G2")
    time.sleep(0.5)
    led_G21()
    time.sleep(1.0)
    led_G20()
    time.sleep(1.0)
    led_G21()
    time.sleep(1.0)
    led_G20()
    print("Test G2 done")


if __name__ == '__main__':
    try:
        leds_aus()
        #led_startup()
        leds_aus()
        #led_countdown5()
        leds_aus()
        #led_start()
        leds_aus()
        #led_obstaclerace()
        led_test_R2()
        
                    
             
    except KeyboardInterrupt:
        print("Messung vom User gestoppt")
        GPIO.cleanup()
