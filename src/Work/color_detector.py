import time
import board
import adafruit_tcs34725

# I2C und Sensor initialisieren
i2c = board.I2C()
sensor = adafruit_tcs34725.TCS34725(i2c)
start = True

# Globale Variablen
kor_R, kor_G, kor_B = 1.0, 1.0, 1.0
T_R, T_G, T_B = 1.0, 1.0, 1.0
co_b = False
co_o = False

B_param = 0.45 ##anpassen##
O_param = 0.55 ##anpassen##

def col_init():
    """Sensor kalibrieren und Korrekturfaktoren berechnen"""
    global kor_R, kor_G, kor_B, T_R, T_G, T_B
    
    for i in range(3):
        color_rgb = sensor.color_rgb_bytes
        print(f"Messung {i+1}: RGB {color_rgb}")

        R, G, B = float(color_rgb[0]), float(color_rgb[1]), float(color_rgb[2])
        W = R + G + B

        if W > 0:
            R, G, B = R / W, G / W, B / W
            kor_R, kor_G, kor_B = 0.33 / R, 0.33 / G, 0.33 / B
            T_R, T_G, T_B = kor_R * R, kor_G * G, kor_B * B

        print("Unkor_ =", R, G, B)
        print("T_ =", T_R, T_G, T_B)
        print("kor_ =", kor_R, kor_G, kor_B)


def col_messen():
    global T_R, T_G, T_B
    color_rgb = sensor.color_rgb_bytes
    #print(f"RGB: {color_rgb}")

    R, G, B = float(color_rgb[0]), float(color_rgb[1]), float(color_rgb[2])
    W = R + G + B

    if W > 0:
        R, G, B = R / W, G / W, B / W
        T_R, T_G, T_B = kor_R * R, kor_G * G, kor_B * B
    else:
        T_R, T_G, T_B = 0.0, 0.0, 0.0
        
    print("TRGB= ", T_R, T_G, T_B)
        
def col_detect(): 
    co_b = False
    co_o = False
    
    col_messen()
    
    if T_B > B_param:
        co_b = True
        print("Blau erkannt!")
            
    if T_R > O_param:
        co_o = True
        print("Orange erkannt!")
            
    return co_b, co_o
            
if __name__ == '__main__':
    try:
        blau = False
        orange = False
        col_init()
        while start:
            blau, orange = col_detect()
        
        
        
    except KeyboardInterrupt:
        print("++ Color detector vom User gestoppt ++")
