import board
import busio
import time
from adafruit_extended_bus import ExtendedI2C as I2C
import adafruit_tca9548a
import adafruit_vl53l4cd
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)

GPIO_HL = 6
GPIO_VL = 5

GPIO.setup(GPIO_HL, GPIO.OUT)
GPIO.setup(GPIO_VL, GPIO.OUT)

# software i2c bus 9 on sda=17, scl=27
i2c = I2C(9)
#i2c = board.I2C()

#multiplexer object
tca = adafruit_tca9548a.TCA9548A(i2c)

#sensor an i2c slot 0
sensorVL = adafruit_vl53l4cd.VL53L4CD(tca[0])
sensorVL.inter_measurement = 0 # no wait between measurements
sensorVL.timing_budget = 20 # 20 msec ranging time

#sensor an i2c slot 6
sensorHL = adafruit_vl53l4cd.VL53L4CD(tca[6])
sensorHL.inter_measurement = 0
sensorHL.timing_budget = 20



print("VL53L4CD Simple Test.")
print("--------------------")
model_id, module_type = sensorVL.model_info
print("Model ID: 0x{:0X}".format(model_id))
print("Module Type: 0x{:0X}".format(module_type))
print("Timing Budget: {}".format(sensorVL.timing_budget))
print("Inter-Measurement: {}".format(sensorVL.inter_measurement))
print("--------------------")

time.sleep(2.0)

count_VL = 0
count_HL = 0

sensorVL.start_ranging()
sensorHL.start_ranging()

startTime = time.time()


while True:
    try:
        if not sensorVL.data_ready:
            pass
        else:
            sensorVL.clear_interrupt()
            #print("Distance VL: {} cm".format(sensorVL.distance))
            #count_VL = count_VL + 1
    except:
        print("error VL")
    
    try:
        if not sensorHL.data_ready:
            pass
        else:
            sensorHL.clear_interrupt()
            #print("Distance HL: {} cm".format(sensorHL.distance))
            
            dist_HL = sensorHL.distance
            #count_HL = count_HL + 1
            if dist_HL < 5.0:
                GPIO.output(GPIO_HL, True)
            else:
                GPIO.output(GPIO_HL, False)
    except:
        print("error HL")
        
        
        
    """if time.time() > startTime + 10.0:
        print("Count VL: {} ".format(count_VL))
        print("Count HL: {} ".format(count_HL))
        time.sleep(2.0)
        count_VL = 0
        count_HL = 0
        startTime = time.time()"""
