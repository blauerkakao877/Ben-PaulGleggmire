import time
import board
import adafruit_tcs34725


i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_tcs34725.TCS34725(i2c)
kor_R = 1.0
kor_G = 1.0
kor_B = 1.0
R = 1.0
G = 1.0
B = 1.0
W = 1.0
T_R = 1.0
T_G = 1.0
T_B = 1.0


# Sensor drei Mal messen lassen, bevor die Hauptschleife beginnt
for i in range(3):
    color = sensor.color
    color_rgb = sensor.color_rgb_bytes
    print(f"Messung {i+1}: RGB {color_rgb}")
    #print('Color: ({0}, {1}, {2})'.format(*sensor.color_rgb_bytes))
    R = float(color_rgb[0]) 
    G = float(color_rgb[1])
    B = float(color_rgb[2])
    
    W = R + G + B
    R = R / W
    G = G / W
    B = B / W
    
    kor_R = 0.33 / R
    kor_G = 0.33 / G
    kor_B = 0.33 / B
        
    T_R = kor_R * R
    T_G = kor_G * G
    T_B = kor_B * B

    
    print("T_ = ",T_R, T_G, T_G)
    print("kor_ = ", kor_R, kor_G, kor_B)
    time.sleep(1)
    
    

while True:
    # Messwerte auslesen
    color = sensor.color
    color_rgb = sensor.color_rgb_bytes
    print(f"RGB color as 8 bits per channel int: #{color:02X} or as 3-tuple: {color_rgb}")
    
    # Verzögerung für eine Sekunde
    time.sleep(1.0)
