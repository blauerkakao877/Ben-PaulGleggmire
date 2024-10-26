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
    Skit.servo[0].angle = 95
    
#---------------------------------------
    
def steuern(lenkwinkel):
    if lenkwinkel > 120:
        lenkwinkel = 120

    if lenkwinkel < 70:
        lenkwinkel = 70

    Skit.servo[0].angle = lenkwinkel
    time.sleep(w)
    
#---------------------------------------
    
def lenkenlinks():
       Skit.servo[0].angle = 130
       time.sleep(0.7)
       Skit.servo[0].angle = 95
       time.sleep(0.5)
       
#---------------------------------------
       
def lenkenrechts():
       Skit.servo[0].angle = 60
       time.sleep(0.7)
       Skit.servo[0].angle = 95
       time.sleep(0.5)
       
#---------------------------------------
       
def nach_links():
       Skit.servo[0].angle = 120
       
#---------------------------------------
       
def nach_rechts():
       Skit.servo[0].angle = 70
       
#---------------------------------------
       
def Uturn_links():
       Skit.servo[0].angle = 120
       
#---------------------------------------
       
def Uturn_rechts():
       Skit.servo[0].angle = 70
       
#---------------------------------------