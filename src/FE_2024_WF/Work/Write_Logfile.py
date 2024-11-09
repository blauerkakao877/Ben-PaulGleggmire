import time

myfile = None
logging = False

def write_Log(line):
    global myfile
    global logging
    
    if logging:
        line = line + "\n"
        myfile.write(line)
        print(line)

def open_Log(start_Log):
    global logging
    global myfile
    if start_Log:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        logfile_name = f"/home/pi/FE_2024_WF/Data/Logfile_{timestamp}.dat"
        myfile = open(logfile_name, "w")
        logging = True
    
def close_Log():
    global myfile
    if myfile is not None:
        myfile.close()
        myfile = None

if __name__ == '__main__':
    try:
        open_Log(True)
        write_Log("Hello")
        close_Log()
        
    except KeyboardInterrupt:
        print("STOP")
        GPIO.cleanup()
