"""Brother in Arms 2 Archive Packer
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

        with open(output_filename, 'wb') as output_file:
            num_files = len(files)
            output_file.write(struct.pack('H', num_files + 1))

            offset = 0
            for i, file_name in enumerate(files):
                with open(os.path.join(input_dir, folder, file_name), 'rb') as file:
                    file_data = file.read()
                    output_file.write(struct.pack('I', offset))
                    offset += len(file_data)

            output_file.write(struct.pack('I', offset))

            for file_name in files:
                with open(os.path.join(input_dir, folder, file_name), 'rb') as file:
                    file_data = file.read()
                    output_file.write(file_data)

        print(f"{folder} packed to {output_filename}")


pack_files_to_binary('input', 'output')
