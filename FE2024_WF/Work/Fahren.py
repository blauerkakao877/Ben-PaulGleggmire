import time
import board
from adafruit_motor import motor
from adafruit_motorkit import MotorKit
from adafruit_servokit import ServoKit

kit = MotorKit(i2c=board.I2C())
Skit = ServoKit(channels=16)
w = 0.08

print("PWM Frequenz:", kit.frequency)  # Verify internal PWM frequency
kit.motor1.decay_mode = motor.SLOW_DECAY
kit.motor2.decay_mode = motor.SLOW_DECAY

def vor(speed):
    speed1 = speed #----Speed hier ändern----
    if speed1 > 1.0:
        speed1 = 1.0 #begrenzung fuer speed
        
    speed1 = round(speed1, 2) #round to 2 digits motorkit doesnt support more
    
    kit.motor1.throttle = speed1
    kit.motor2.throttle = speed1
    
#---------------------------------------

def stop():
    speed1 = 0.0
    kit.motor1.throttle = speed1
    kit.motor2.throttle = speed1
    
#---------------------------------------

def ruck(speed):
    speed1 = -1.0*speed #----Speed hier ändern----
    kit.motor1.throttle = speed1
    kit.motor2.throttle = speed1
    
#---------------------------------------

def anfahren(speed):
    speed1 = 0.5*speed #----slowing speed down----
    speed2 = 0.7*speed #----slowing speed down----
    
    kit.motor1.throttle = speed1
    kit.motor2.throttle = speed1
    time.sleep(0.1)
    kit.motor1.throttle = speed2
    kit.motor2.throttle = speed2
    time.sleep(0.1)

#---------------------------------------

def gerade():
    Skit.servo[0].angle = 93
    
#---------------------------------------
    
def steuern(lenkwinkel):
    if lenkwinkel > 115:
        lenkwinkel = 115

    if lenkwinkel < 65:
        lenkwinkel = 65

    Skit.servo[0].angle = lenkwinkel
    time.sleep(w)
    
#---------------------------------------
    
def lenkenlinks():
       Skit.servo[0].angle = 125
       time.sleep(0.8)
       Skit.servo[0].angle = 93
       time.sleep(0.6)
       
#---------------------------------------
       
def lenkenrechts():
       Skit.servo[0].angle = 55
       time.sleep(0.8)
       Skit.servo[0].angle = 93
       time.sleep(0.6)
       
#---------------------------------------
       
def nach_links():
       Skit.servo[0].angle = 115
       
#---------------------------------------
       
def nach_rechts():
       Skit.servo[0].angle = 65
       
#---------------------------------------
       
def linkshalten1():
       Skit.servo[0].angle = 110
       time.sleep(w)
       
#---------------------------------------
       
def rechtshalten1():
       Skit.servo[0].angle = 70
       time.sleep(w)
   
#---------------------------------------
       
def linkshalten2():
       Skit.servo[0].angle = 70
       time.sleep(w)
       
#---------------------------------------
       
def rechtshalten2():
       Skit.servo[0].angle = 110
       time.sleep(w)
       
#---------------------------------------

def wandweg_L():
    Skit.servo[0].angle = 125
    time.sleep(0.2)
    Skit.servo[0].angle = 75
    
#---------------------------------------
    
def wandweg_R():
    Skit.servo[0].angle = 125
    time.sleep(0.2)
    Skit.servo[0].angle = 75
    
