"""Hero os Sparta Text Unpacker by Dhampir v1.0
   Tested on game version 1.1.4"""

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
    return string


def process_data(off_file_path, dat_file_path, output_folder):
    with open(off_file_path, 'rb') as off_file, open(dat_file_path, 'rb') as dat_file:
        count_str = struct.unpack('H', off_file.read(2))[0]
        block_off = count_str * 2

        offsets = [0]

        for i in range(count_str):
            offset = struct.unpack('H', off_file.read(2))[0]
            offsets.append(offset)

        data = dat_file.read()

        dat_filename = os.path.splitext(os.path.basename(dat_file_path))[0]
        output_file_path = os.path.join(output_folder, f'{dat_filename}.txt')

        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for i in range(count_str):
                start_off = offsets[i]
                end_off = offsets[i + 1] - 1 if i < count_str - 1 else block_off
                text = data[start_off:end_off].decode('utf-8')
                # encode = text.translate(translation_table)  # use only for Ukrainian and Russian language
                encode2 = EncodeText(text)  # for Ukrainian and Russian language change 'text' to 'encode'
                output_file.write(encode2 + '\n')


def find_files_with_extension(folder, extension):
    files = [file for file in os.listdir(folder) if file.endswith(extension)]
    return sorted(files, key=lambda x: int(os.path.splitext(x)[0]))


folder_path = 'input'
output_folder = 'output'
off_files = find_files_with_extension(folder_path, '.off')
dat_files = find_files_with_extension(folder_path, '.dat')

for off_file_name, dat_file_name in zip(off_files, dat_files):
    off_file_path = os.path.join(folder_path, off_file_name)
    dat_file_path = os.path.join(folder_path, dat_file_name)
    process_data(off_file_path, dat_file_path, output_folder)

print("Processing complete.")
