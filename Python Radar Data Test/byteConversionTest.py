import ast
import struct

def getBarkerCodeIndexes():
        # Creates a string representing the text in binaryData.txt
        with open('binaryData.txt', 'r') as file:
                data = file.read().strip()
        # Converts from str to data, trims 'b\', removes extra \ between each byte
        # All stored in an array first byte is [0]
                byteData = ast.literal_eval(data)
                #decimal_str = ' '.join(f"{byte:02d}" for byte in byteData)
                barkerCode = b'\x02\x01\x04\x03\x06\x05\x08\x07' #Defining barker in terms of bytes
                barkerCodeIndexes = [] #Initialize array to store barkerCodeIndexes
                i = 0 #Initialize i
                while i < len(byteData):#Ensuring all data is searched
                        i = byteData.find(barkerCode, i)#Finds start of next barkerCode

                        if i == -1:
                                i = 0 #Resets i for future use
                                break #No more cases of barkerCode found
                        else:
                                barkerCodeIndexes.append(i)#Appends index of next barkerCode
                                i = i + 1
        return  byteData, barkerCode, barkerCodeIndexes

byteData, barkerCode, barkerCodeIndexes = getBarkerCodeIndexes()
dopplerIndex = 0 #This is just here so I can have the breakpoint with all the variables I can play with

#def checkSum(byteData, barkerCodeIndex):
       # frameHeader = byteData[]