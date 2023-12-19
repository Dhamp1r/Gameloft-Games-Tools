"""Brother in Arms 2 Text Unpacker
   Tested on game version 1.0.4

   Author: Dhampir
   Version: 1.0
   License: MIT
"""

import os
import struct

translation_table = str.maketrans(
    'ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ¡¢¹º²³§¨¼½¾¿',
    'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюяЁёЄєІіЇїҐґ–…'
)


def EncodeText(string):
    string = string.replace('\x0A', '\\n')
    string = string.replace('\x00', '[x00]')
    string = string.replace('\x01', '[x01]')
    string = string.replace('\x02', '[x02]')
    string = string.replace('\x03', '[x03]')
    string = string.replace('\x04', '[x04]')
    string = string.replace('\x05', '[x05]')
    string = string.replace('\x06', '[x06]')
    string = string.replace('\x07', '[x07]')
    string = string.replace('\x08', '[x08]')
    string = string.replace('\x09', '[x09]')
    string = string.replace('\x10', '[x10]')
    string = string.replace('\x11', '[x11]')
    string = string.replace('\xFF', '[xFF]')
    string = string.replace('\x0E', '[x0E]')
    string = string.replace('\x0F', '[x0F]')
    string = string.replace('\x2B', '[x2B]')
    return string


def process_data(dat_file_path, output_folder):
    output_file_name = os.path.splitext(os.path.basename(dat_file_path))[0] + '.txt'
    output_file_path = os.path.join(output_folder, output_file_name)

    with open(dat_file_path, 'rb') as dat_file, open(output_file_path, 'w', encoding='utf-16') as output_file:
        count_str = struct.unpack('I', dat_file.read(4))[0]

        offsets = []

        for i in range(count_str):
            offset = struct.unpack('I', dat_file.read(4))[0]
            offsets.append(offset)

        data = dat_file.read()

        for i in range(count_str):
            start_off = offsets[i]
            end_off = offsets[i + 1] - 2 if i < count_str - 1 else len(data) - 2
            text = data[start_off:end_off].decode('utf-16')
            # encode = text.translate(translation_table)  # use only for Ukrainian and Russian language
            encode2 = EncodeText(text)  # for Ukrainian and Russian language change 'text' to 'encode'
            output_file.write(encode2 + '\n')

    print(f'{dat_file_path} exported to {output_file_path}')


def process_files_in_folder(input_folder, output_folder):
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.text'):
            dat_file_path = os.path.join(input_folder, file_name)
            process_data(dat_file_path, output_folder)


input_folder_path = 'input'
output_folder_path = 'output'

if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

process_files_in_folder(input_folder_path, output_folder_path)
print("Processing complete.")
