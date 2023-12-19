"""Hero of Sparta Text Packer
   Tested on game version 1.1.4

   Author: Dhampir
   Version: 1.0
   License: MIT
"""

import csv
import struct
import os
from modules.gsheets_downloader import download_gsheets

translation_table = str.maketrans(
    'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюяЁёЄєІіЇїҐґ–…',
    'ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ¡¢¹º²³§¨¼½¾¿'
)


def encode_text(string):
    string = string.replace('\\n', '\n')
    string = string.replace('[x00]', '\x00')
    string = string.replace('[x01]', '\x01')
    string = string.replace('[x02]', '\x02')
    string = string.replace('[x03]', '\x03')
    string = string.replace('[x04]', '\x04')
    string = string.replace('[x05]', '\x05')
    string = string.replace('[x06]', '\x06')
    string = string.replace('[x07]', '\x07')
    string = string.replace('[x08]', '\x08')
    string = string.replace('[x09]', '\x09')
    string = string.replace('[x10]', '\x10')
    string = string.replace('[x11]', '\x11')
    string = string.replace('[xFF]', '\xFF')
    string = string.replace('[x0E]', '\x0E')
    string = string.replace('[x0F]', '\x0F')
    return string


def process_gsheets_to_binary(url, text_file_path, off_file_path):
    download_gsheets(url, 'temp.tsv')

    with (open('temp.tsv', 'r', newline='', encoding='utf-8') as tsv_file,
          open(text_file_path, 'wb') as txt,
          open(off_file_path, 'wb') as off):
        reader = csv.reader(tsv_file, delimiter='\t')
        next(reader)  # skip the first line
        count = []  # number of rows

        for row in reader:
            text = row[1]  # first column [0] original text, second column [1] translation
            eng_text = row[0]
            if not text.strip():
                text = eng_text
            # encode = text.translate(translation_table)  # use only for Ukrainian and Russian language
            encode1 = encode_text(text)  # for Ukrainian and Russian language change 'text' to 'encode'
            count.append(encode1)  # for the number of rows
            offset = txt.tell()  # offsets
            off.write(struct.pack('H', offset))
            txt.write(encode1.encode('utf-8'))  # final text
            txt.write(bytes(1))  # wrap
        end_offset = txt.tell()
        off.seek(0)
        off.write(struct.pack('H', len(count)))  # number of rows
        off.seek(0, os.SEEK_END)
        off.write(struct.pack('H', end_offset))  # end offset
    os.remove('temp.tsv')
    print("Text successfully packed")


# Example usage:
text_file_path = 'text.dat'
off_file_path = 'text.off'
gsheets_url = 'https://'  # your link to google sheets
process_gsheets_to_binary(gsheets_url, text_file_path, off_file_path)
