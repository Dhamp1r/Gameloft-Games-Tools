"""Hero of Sparta FontArchive Packer
   Tested on game version 1.0.4 (fonts, text files)

   Author: Dhampir
   Version: 1.0
   License: MIT
"""

import struct
import os


def pack_files_to_binary(input_dir, output_dir):
    folders = [folder for folder in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, folder))]

    for folder in folders:
        output_filename = os.path.join(output_dir, f'{folder}')

        files = sorted(os.listdir(os.path.join(input_dir, folder)), key=lambda x: int(x.split('.')[0]))
        offsets = []

        with open(output_filename, 'wb') as output_file:
            num_files = len(files) + 2
            output_file.write(struct.pack('H', num_files))

            offset = 0
            for i, file_name in enumerate(files):
                with open(os.path.join(input_dir, folder, file_name), 'rb') as file:
                    file_data = file.read()
                    if i == 1:
                        output_file.write(struct.pack('I', offset))
                        output_file.write(struct.pack('I', offset))
                        offsets.extend([offset, offset])
                    elif i == 12:
                        output_file.write(struct.pack('I', offset))
                        output_file.write(struct.pack('I', offset))
                        output_file.write(struct.pack('I', offset))
                        offsets.extend([offset, offset])
                    else:
                        output_file.write(struct.pack('I', offset))
                        offsets.append(offset)
                    offset += len(file_data)
            output_file.write(struct.pack('I', offset))
            output_file.write(struct.pack('I', offset))
            output_file.write(struct.pack('I', offset))
            output_file.write(struct.pack('I', offset))
            output_file.write(struct.pack('I', offset))
            output_file.write(struct.pack('I', offset))
            output_file.write(struct.pack('I', offset))
            offsets.extend([offset, offset, offset])

            for file_name in files:
                with open(os.path.join(input_dir, folder, file_name), 'rb') as file:
                    file_data = file.read()
                    output_file.write(file_data)

        with open(output_filename, 'r+b') as file:
            file.seek(0)
            num_offsets = len(offsets) + 5
            file.write(struct.pack('H', num_offsets))

        print(f"Packed to: {output_filename}.")


pack_files_to_binary('input', 'output')
