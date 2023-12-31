"""Brother in Arms 2 Archive Unpacker
   Tested on game version 1.0.4 (fonts, text files)

   Author: Dhampir
   Version: 1.0
   License: MIT
"""

import os
import struct

def recognize_format(file_data):
    if b'\xDF\x03' in file_data[:2]:
        return 'font'
    elif b'\xFF\xFE' in file_data[:2]:
        return 'map'
    elif b'!"#$' in file_data[65:69]:
        return 'map'
    elif b'\xD0\x06' in file_data[:2]:
        return 'text'
    else:
        return 'dat'

def read_binary_file(input_folder, output_folder):
    input_files = os.listdir(input_folder)

    for input_file_name in input_files:
        input_file_path = os.path.join(input_folder, input_file_name)

        with open(input_file_path, 'rb') as file:
            count = struct.unpack('H', file.read(2))[0]
            offset_length = count * 4
            file.seek(2)

            offsets = []
            seen_values = set()

            for _ in range(count):
                data = file.read(4)

                combined_data = ''.join([format(byte, '02X') for byte in reversed(data)])

                if combined_data not in seen_values:
                    offsets.append(combined_data)
                    seen_values.add(combined_data)

            for i in range(len(offsets) - 1):
                start_offset = (offset_length + 2) + int(offsets[i], 16)
                end_offset = (offset_length + 2) + int(offsets[i + 1], 16)
                file.seek(start_offset)

                file_data = file.read(end_offset - start_offset)

                file_extension = recognize_format(file_data)

                output_file_folder = os.path.join(output_folder, input_file_name)
                if not os.path.exists(output_file_folder):
                    os.makedirs(output_file_folder)

                output_filename = f'{start_offset}.{file_extension}'
                output_filepath = os.path.join(output_file_folder, output_filename)
                with open(output_filepath, 'wb') as output_file:
                    output_file.write(file_data)

                print(f"{output_filename} unpacked in {output_file_folder}")


input_folder = 'input'
output_folder = 'output'

read_binary_file(input_folder, output_folder)
print("Processing complete.")
