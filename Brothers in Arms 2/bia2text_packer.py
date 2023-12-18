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
    string = string.replace('[x2B]', '\x2B')
    return string


def process_gsheets_to_binary(url, dat_file_path):
    tsv_file_path = 'temp.tsv'
    temp_text = 'temp.text'
    temp_off = 'temp.off'

    download_gsheets(url, tsv_file_path)

    with (open(tsv_file_path, 'r', newline='', encoding='utf-8') as tsv_file,
          open(temp_text, 'wb') as txt, open(temp_off, 'wb') as off):

        reader = csv.reader(tsv_file, delimiter='\t')
        next(reader)

        temp = []

        off.write(bytes(4))

        for row in reader:
            text = row[1]  # first column [0] original text, second column [1] translation
            eng_text = row[0]
            if not text.strip():
                text = eng_text
            # transl = text.translate(translation_table)  # use only for Ukrainian and Russian language
            encode = encode_text(text)  # for Ukrainian and Russian language change 'text' to 'transl'
            offset = txt.tell()
            temp.append(offset)
            off.write(struct.pack('I', offset))
            txt.write(encode.encode('utf-16-le'))
            txt.write(bytes(2))
        off.seek(0)
        off.write(struct.pack('I', len(temp)))

    with open(temp_text, 'rb') as file1, open(temp_off, 'rb') as file2, open(dat_file_path, 'wb') as target_file:
        target_file.write(file2.read())
        target_file.write(file1.read())

    os.remove(temp_text)
    os.remove(temp_off)
    os.remove(tsv_file_path)
    print(f'Data from {url} processed and saved to {dat_file_path}')


# Example usage:
dat_file_path = 'new.text'
gsheets_url = 'https://'  # your link to google sheets
process_gsheets_to_binary(gsheets_url, dat_file_path)
