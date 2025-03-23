import ast
import struct

def parse(): 
    # Creates a string representing the text in binaryData.txt
    with open('binaryData.txt', 'r') as file:
        data = file.read().strip()

    # Converts from str to data, trims 'b\', removes extra \ between each byte
    #All stored in an array first byte is [0]
    byteData = ast.literal_eval(data)

    # Convert bytes to space-separated two-digit decimal strings
    decimal_str = ' '.join(f"{byte:02d}" for byte in byteData)

    # Separate each frame by new line
    # Define the target sequence and replacement
    barkerCode = "02 01 04 03 06 05 08 07"
    replacement = "\n" + barkerCode
    doppler = []
    range = []
    # Replace all occurrences of the target sequence
    modified_str = decimal_str.replace(barkerCode, replacement)

    # Write the result to "filteredData.txt"
    with open('filteredData.txt', 'w') as output_file:
        output_file.write(modified_str)

    # Open "filterData.txt" in read mode
    with open("filteredData.txt", 'r') as file:
        lines = file.readlines()  # Read all lines once

        # Read through the file to find barker code and ensure that 76 bytes can be read ahead
        for i, line in enumerate(lines):
            if line.strip() == "":  # Skip empty lines
                continue
            elif i + 76 < len(lines):  # Ensure index does not go out of range
                frame = lines[i + 76].split()  # Get the line 76 places ahead
                # Print barker or sync code bytes
                #print("sync", frame[:8])

                # Print range values (4)
                #print("range", frame[60:64])

                # Convert range to bytes and unpack as float
                deicmalRangeList = [frame[60], frame[61], frame[62], frame[63]]
                bytesRange = bytes(int(x) for x in deicmalRangeList)
                floatValueRange = struct.unpack('f', bytesRange)[0]
                #print(f"Float Range: {floatValueRange}")
                range.append(floatValueRange)

                # **Implement try catch for when azimuth, doppler, and SNR are not full
                #print("azimuth", frame[64:68])

                # Ensure there are at least 4 values for azimuth
                if len(frame) < 68:
                    print("Azimuth reading is null")
                else:
                    deicmalAzimuthList = [frame[64], frame[65], frame[66], frame[67]]

                    try:
                        # Convert to bytes and unpack as float
                        bytesAzimuth = bytes(int(x) for x in deicmalAzimuthList)
                        floatValueAzimuth = struct.unpack('f', bytesAzimuth)[0]
                        print(f"Float Azimuth: {floatValueAzimuth}")
                    except ValueError:
                        print("Invalid Azimuth data")

                # Print doppler values (4)
                #print("doppler", frame[68:72])

                # Ensure there are at least 4 values for azimuth
                if len(frame) < 72:
                    print("Doppler reading is null")
                else:
                    deicmalDopplerList = [frame[68], frame[69], frame[70], frame[71]]

                    try:
                        # Convert to bytes and unpack as float
                        bytesDoppler = bytes(int(x) for x in deicmalDopplerList)
                        floatValueDoppler = struct.unpack('f', bytesDoppler)[0]
                        #print(f"Float Doppler: {floatValueDoppler}")
                        doppler.append(floatValueDoppler)
                    except ValueError:
                        print("Invalid Doppler data")

                # Print SNR values (4)
                #print("SNR", frame[72:76])

                # Ensure there are at least 4 values for azimuth
                if len(frame) < 76:
                    print("SNR reading is null")
                else:
                    deicmalSNRList = [frame[72], frame[73], frame[74], frame[75]]

                    try:
                        # Convert to bytes and unpack as float
                        bytesSNR = bytes(int(x) for x in deicmalSNRList)
                        floatValueSNR = struct.unpack('f', bytesSNR)[0]
                        print(f"Float SNR: {floatValueSNR}")
                    except ValueError:
                        print("Invalid SNR data")
    return range, doppler
range, doppler = parse()
range = [x * 10**41 for x in range]
doppler = [x * 10**-38 if i %2 != 0 else x for i, x in enumerate(doppler)]
doppler = [x * 10**42 if i %2 == 0 else x for i, x in enumerate(doppler)]
collisionTime =  [abs(x) for x in [a/b for a,b in zip(range, doppler)]]

i = 0