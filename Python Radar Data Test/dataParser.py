import struct

# Define message header structure (based on MmwDemo_output_message_header)
HEADER_FORMAT = "<Q 10H 2I"
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

# Define TLV structure
TLV_FORMAT = "<I I I"
TLV_SIZE = struct.calcsize(TLV_FORMAT)

# Define detected object structure (example, assuming 4 integers per object)
OBJ_FORMAT = "<4h"  # (x, y, z, velocity) in Q format
OBJ_SIZE = struct.calcsize(OBJ_FORMAT)

def parse_radar_output(binary_data):
    """ Parses radar output binary message dynamically """

    offset = 0
    if len(binary_data) < HEADER_SIZE:
        print("Error: Incomplete header")
        return

    # Parse Header
    header = struct.unpack_from(HEADER_FORMAT, binary_data, offset)
    offset += HEADER_SIZE

    magic_word = header[:4]
    num_detected_obj = header[4]
    num_tlvs = header[5]
    total_packet_len = header[6]
    frame_number = header[8]
    
    print(f"Magic Word: {magic_word}")
    print(f"Number of Detected Objects: {num_detected_obj}")
    print(f"Number of TLVs: {num_tlvs}")
    print(f"Total Packet Length: {total_packet_len}")
    print(f"Frame Number: {frame_number}\n")

    parsed_tlvs = {}

    # Parse TLVs dynamically
    for _ in range(num_tlvs):
        if offset + TLV_SIZE > len(binary_data):
            print("Error: Incomplete TLV header")
            break

        # Read TLV
        tlv_type, tlv_length, tlv_address = struct.unpack_from(TLV_FORMAT, binary_data, offset)
        offset += TLV_SIZE

        print(f"TLV Type: {tlv_type}, Length: {tlv_length}, Address: {hex(tlv_address)}")

        # Parse TLV based on type
        tlv_data = []
        num_objects = tlv_length // OBJ_SIZE
        
        for i in range(num_objects):
            if offset + OBJ_SIZE > len(binary_data):
                print(f"Error: Incomplete data for TLV Type {tlv_type}")
                break

            obj_data = struct.unpack_from(OBJ_FORMAT, binary_data, offset)
            tlv_data.append(obj_data)
            offset += OBJ_SIZE

        parsed_tlvs[tlv_type] = tlv_data

    print("\nParsed TLV Data:")
    for tlv_type, data in parsed_tlvs.items():
        print(f"TLV {tlv_type}: {data}")

    return parsed_tlvs

# Example: Reading a binary file and parsing
#with open("radar_output.bin", "rb") as f:
f = open("binaryData.bin", "rb")
binary_data = f.read()
parsed_data = parse_radar_output(binary_data)