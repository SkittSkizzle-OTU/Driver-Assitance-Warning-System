import time
import serial

#dataPort = serial.Serial("/dev/ttyAMA0", baudrate=921600, timeout=3.0)
#cliPort = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=3.0)
dataPort = serial.Serial('COM4', baudrate=921600, timeout=3.0)
cliPort = serial.Serial('COM5', baudrate=115200, timeout=3.0)

f = open("binaryData.txt", "w")

try:
    while True:
        rcv = dataPort.read(1024)
        print(rcv)

        if rcv:
            f.write(str(rcv))  # Save data to file
        time.sleep(0.1)  # Small delay to avoid CPU overuse

except KeyboardInterrupt:
    dataPort.close()
    cliPort.close()
    f.close()
    print("Serial ports closed.")
