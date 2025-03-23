from gpiozero import LED, TonalBuzzer
#from time import sleep
#import serial
#import dataParser
from gpiozero.tones import Tone
from dataParser import parse
#dataPort = serial.Serial('/dev/ttyAMA0', baudrate=921600)
#cliPort = serial.Serial('/dev/ttyAMA0', baudrate=115200)

red = LED(17)#Assigning the red LED to GPIO 17
yellow = LED(27)#Assigning the yellow LED to GPIO 27
green = LED(22)#Assigning the green LED to GPIO 22
speakerLow = TonalBuzzer(18)#Assinging the low voltage tone to a PWM GPIO 18
speakerHigh = TonalBuzzer(13)#Assinging the high voltage tone to a PWM GPIO 13
distance = float(0)#Defining and initializing distance as a float
speed = float(0)#Defining and initializing speed as a float
time = float(0)#Defining and initializing time as a float

try:#Make room for interrupts
    while True:#Loop forever
        #distance = float(input("What is the sample distance in meters? "))#Get sample distance data
        #speed = float(input("What is the sample speed in m/s? "))#Get sample speed data
        #time = float(distance/speed)#Calculate time until reaching the other object
        range, doppler = parse()
        range = [x * 10 ** 41 for x in range]
        doppler = [x * 10 ** -38 if i % 2 != 0 else x for i, x in enumerate(doppler)]
        doppler = [x * 10 ** 42 if i % 2 == 0 else x for i, x in enumerate(doppler)]
        time = [abs(x) for x in [a / b for a, b in zip(range, doppler)]]
        for t in time:
            match t:                #Match case switch
                case _ if t>=7:#If time is greater than 7 seconds switch off everything and enable green light
                    red.off()
                    yellow.off()
                    green.on()
                    speakerLow.stop()
                    speakerHigh.stop()

                case _ if 6.6 <= t < 7:#If time is between 7 and 6.6 seconds, enable yellow light and low tone switch off else
                    red.off()
                    yellow.on()
                    green.off()
                    speakerLow.play(220.0)
                    speakerHigh.stop()

                case _ if t<6.6 and t != 0:#If time is less than 6.6 seconds, enable red light and high tone switch off else
                    red.on()
                    yellow.off()
                    green.off()
                    speakerLow.stop()
                    speakerHigh.play(220.0)
except KeyboardInterrupt:#If force closed with ctrl+c turn everything off
    red.off()
    yellow.off()
    green.off()
    speakerLow.stop()
    speakerHigh.stop()
