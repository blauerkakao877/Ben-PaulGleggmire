import board
import busio
import time
import RPi.GPIO as GPIO
from adafruit_extended_bus import ExtendedI2C as I2C
import adafruit_tca9548a
import adafruit_vl53l4cd

# GPIO Modus (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
# software i2c bus 9 on sda=17, scl=27
i2c = I2C(9)
#i2c = board.I2C()

GPIO_HL = 23
GPIO_VL = 24
GPIO_HR = 20
GPIO_VR = 21

GPIO.setup(GPIO_HL, GPIO.OUT)
GPIO.setup(GPIO_VL, GPIO.OUT)
GPIO.setup(GPIO_HR, GPIO.OUT)
GPIO.setup(GPIO_VR, GPIO.OUT)

park_dist = 1.0
field_dist = 5.0
alarm_dist = 5.0

#multiplexer object
tca = adafruit_tca9548a.TCA9548A(i2c)
try:
    #sensor an i2c slot 0
    sensorVL = adafruit_vl53l4cd.VL53L4CD(tca[0])
    sensorVL.inter_measurement = 0 # no wait between measurements
    sensorVL.timing_budget = 20 # 20 msec ranging time
except:
    print("Error init VL")

#sensor an i2c slot 1
try:
    sensorHL = adafruit_vl53l4cd.VL53L4CD(tca[6])
    sensorHL.inter_measurement = 0
    sensorHL.timing_budget = 20
except:
     print("Error init HL")


#sensor an i2c slot 7
try:
    sensorVR = adafruit_vl53l4cd.VL53L4CD(tca[7])
    sensorVR.inter_measurement = 0 # no wait between measurements
    sensorVR.timing_budget = 20 # 20 msec ranging time
except:
    print("Error init VR")
    
#sensor an i2c slot 6
try:
    sensorHR = adafruit_vl53l4cd.VL53L4CD(tca[5])
    sensorHR.inter_measurement = 0
    sensorHR.timing_budget = 20
except:
    print("Error init HR")
    
#sensor an i2c slot 4
try:
    sensorHM = adafruit_vl53l4cd.VL53L4CD(tca[4])
    sensorHM.inter_measurement = 0
    sensorHM.timing_budget = 20
except:
    print("Error init HM")

print("VL53L4CD Simple Test.")
print("--------------------")
model_id, module_type = sensorVL.model_info
print("Model ID: 0x{:0X}".format(model_id))
print("Module Type: 0x{:0X}".format(module_type))
print("Timing Budget: {}".format(sensorVL.timing_budget))
print("Inter-Measurement: {}".format(sensorVL.inter_measurement))
print("--------------------")

time.sleep(2.0)


sensorVL.start_ranging()
sensorHL.start_ranging()
sensorVR.start_ranging()
sensorHR.start_ranging()
sensorHM.start_ranging()

startTime = time.time()

GPIO.output(GPIO_VL, False)
GPIO.output(GPIO_HL, False)
GPIO.output(GPIO_VR, False)
GPIO.output(GPIO_HR, False)

while True:
    try:
        if not sensorVL.data_ready:
            pass
        else:
            sensorVL.clear_interrupt()
            #print("Distance VL: {} cm".format(sensorVL.distance))
            distVL = sensorVL.distance
            if distVL < alarm_dist:
                GPIO.output(GPIO_VL, True)
            else:
                GPIO.output(GPIO_VL, False)
    except:
        print("io_error VL")
    
    try:
        if not sensorHL.data_ready:
            pass
        else:
            sensorHL.clear_interrupt()
            #print("Distance HL: {} cm".format(sensorHL.distance))
            distHL = sensorHL.distance
            if distHL < alarm_dist:
                GPIO.output(GPIO_HL, True)
            else:
                GPIO.output(GPIO_HL, False)
    except:
        print("io_error HL")
        
      
    try:
        if not sensorVR.data_ready:
            pass
        else:
            sensorVR.clear_interrupt()
            #print("Distance VR: {} cm".format(sensorVR.distance))
            distVR = sensorVR.distance
            if distVR < alarm_dist:
                GPIO.output(GPIO_VR, True)
            else:
                GPIO.output(GPIO_VR, False)
            
    except:
        print("io_error VR")
    
    try:
        if not sensorHR.data_ready:
            pass
        else:
            sensorHR.clear_interrupt()
            #print("Distance HR: {} cm".format(sensorHR.distance))
            distHR = sensorHR.distance
            if distHR < alarm_dist:
                GPIO.output(GPIO_HR, True)
            else:
                GPIO.output(GPIO_HR, False)
    except:
        print("io_error HR")
        
        
    try:
        if not sensorHM.data_ready:
            pass
        else:
            sensorHM.clear_interrupt()
            #print("Distance HM: {} cm".format(sensorHM.distance))
            distHM = sensorHM.distance
            if distHM < alarm_dist:
                GPIO.output(GPIO_HR, True)
                GPIO.output(GPIO_HL, True)
           """else:
                GPIO.output(GPIO_HR, False)
                GPIO.output(GPIO_HL, False)"""
    except:
        print("io_error HM")
        
    #time.sleep(1.0)
