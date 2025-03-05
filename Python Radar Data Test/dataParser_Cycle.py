 
import struct
import sys

# Define message header structure (based on MmwDemo_output_message_header)
HEADER_FORMAT = "<4H I I I I I I"
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

# Define TLV structure
TLV_FORMAT = "<I I I"
TLV_SIZE = struct.calcsize(TLV_FORMAT)

# Define detected object structure (example, assuming 4 integers per object)
OBJ_FORMAT = "<4h"  # (x, y, z, velocity) in Q format
OBJ_SIZE = struct.calcsize(OBJ_FORMAT)

def parse_radar_output(binary_data, offset):
    """ Parses radar output binary message dynamically """

    
    if len(binary_data) < HEADER_SIZE:
        print("Error: Incomplete header")
        return

    # Parse Header
    header = struct.unpack_from(HEADER_FORMAT, binary_data, offset)

    magic_word = header[:4]
    num_detected_obj = header[4]
    num_tlvs = header[5]
    total_packet_len = header[6]
    frame_number = header[8]
    
    #can uncomment to manually inspect
    
    # print(f"Magic Word: {magic_word}")
    # print(f"Number of Detected Objects: {num_detected_obj}")
    # print(f"Number of TLVs: {num_tlvs}")
    # print(f"Total Packet Length: {total_packet_len}")
    # print(f"Frame Number: {frame_number}\n")
    
    
    #experiment with this...
    if num_tlvs < 100:
        print(offset)
        parsed_tlvs = 1
    else:
        parsed_data = 0

    return parsed_data
    # Parse TLVs dynamically
    # for _ in range(num_tlvs):
    #     if offset + TLV_SIZE > len(binary_data):
    #         print("Error: Incomplete TLV header")
    #         break

    #     # Read TLV
    #     tlv_type, tlv_length, tlv_address = struct.unpack_from(TLV_FORMAT, binary_data, offset)
    #     offset += TLV_SIZE

    #     print(f"TLV Type: {tlv_type}, Length: {tlv_length}, Address: {hex(tlv_address)}")

    #     # Parse TLV based on type
    #     tlv_data = []
    #     num_objects = tlv_length // OBJ_SIZE
        
    #     for i in range(num_objects):
    #         if offset + OBJ_SIZE > len(binary_data):
    #             print(f"Error: Incomplete data for TLV Type {tlv_type}")
    #             break

    #         obj_data = struct.unpack_from(OBJ_FORMAT, binary_data, offset)
    #         tlv_data.append(obj_data)
    #         offset += OBJ_SIZE

    #     parsed_tlvs[tlv_type] = tlv_data

    # print("\nParsed TLV Data:")
    # for tlv_type, data in parsed_tlvs.items():
    #     print(f"TLV {tlv_type}: {data}")

    # return parsed_tlvs


f = open("binaryData.bin", "rb")
binary_data = f.read()
#cycling through the data
for offset in range(0, sys.getsizeof(binary_data) - 120, 1):
    parsed_data = parse_radar_output(binary_data, offset)
    if parsed_data:
        print('This Offset might make sense:', offset )