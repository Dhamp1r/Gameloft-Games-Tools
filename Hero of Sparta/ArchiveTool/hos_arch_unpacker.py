import sys
import os

def recognize_format(file_data):
    if b'PVR!' in file_data:
        return 'pvr'
    elif b'!"#$' in file_data:
        return 'map'
    elif b'\xDF\x05' in file_data[:2]:
        return 'bdae'
    elif b'\xAE\x01' in file_data[:2]:
        return 'off'
    else:
        return 'dat'

def read_binary_file(filename):
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'exp_text')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(filename, 'rb') as file:
        bytes_read = file.read(2)
        reversed_bytes = bytes_read[::-1]
        dex_value = int.from_bytes(reversed_bytes, byteorder='big')
        offset_length = dex_value * 4
        file.seek(2)

        offsets = []
        seen_values = set()

        for _ in range(dex_value):
            data = file.read(4)

            combined_data = ''.join([format(byte, '02X') for byte in reversed(data)])

            if combined_data not in seen_values:
                offsets.append(combined_data)
                seen_values.add(combined_data)

        for i in range(len(offsets) - 1):
            start_offset = (offset_length + 2) + int(offsets[i], 16)
            end_offset = (offset_length + 2) + int(offsets[i+1], 16)
            file.seek(start_offset)

            file_data = file.read(end_offset - start_offset)

            file_extension = recognize_format(file_data)

            output_filename = f'{start_offset}.{file_extension}'
            output_filepath = os.path.join(output_dir, output_filename)
            with open(output_filepath, 'wb') as output_file:
                output_file.write(file_data)

            print(f"{output_filename} unpacked")


read_binary_file('TEXT')