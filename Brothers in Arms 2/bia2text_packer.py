import csv
import struct
import os
from gsheets_downloader import download_gsheets

translation_table = str.maketrans(
    'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюяЁёЄєІіЇїҐґ–…',
    'ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ¡¢¹º²³§¨¼½¾¿'
)

def EncodeText(string):
    string = string.replace("\\n", "\n")
    string = string.replace("[x00]", "\x00")
    string = string.replace("[x01]", "\x01")
    string = string.replace("[x02]", "\x02")
    string = string.replace("[x03]", "\x03")
    string = string.replace("[x04]", "\x04")
    string = string.replace("[x05]", "\x05")
    string = string.replace("[x06]", "\x06")
    string = string.replace("[x07]", "\x07")
    string = string.replace("[x08]", "\x08")
    string = string.replace("[x09]", "\x09")
    string = string.replace("[x10]", "\x10")
    string = string.replace("[x11]", "\x11")
    string = string.replace("[xFF]", "\xFF")
    string = string.replace("[x0E]", "\x0E")
    string = string.replace("[x0F]", "\x0F")
    string = string.replace("[x2B]", "\x2B")
    return string


def process_data(tsv_file_path, temp_text, temp_off, dat_file_path):
    with (open(tsv_file_path, 'r', newline='', encoding='utf-8') as tsv_file,
          open(temp_text, 'wb') as txt, open(temp_off, 'wb') as off,
          open(dat_file_path, 'wb') as dat_file):

        reader = csv.reader(tsv_file, delimiter='\t')
        next(reader)

        temp = []

        off.write(bytes(4))

        for row in reader:
            text = row[1]
            eng_text = row[0]
            if not text.strip():
                text = eng_text
            encode = EncodeText(text)
            transl = encode.translate(translation_table)
            offset = txt.tell()
            temp.append(offset)
            off.write(struct.pack('I', offset))
            txt.write(transl.encode('utf-16-le'))
            txt.write(bytes(2))
        off.seek(0)
        off.write(struct.pack('I', len(temp)))

    with open(temp_text, 'rb') as file1, open(temp_off, 'rb') as file2, open(dat_file_path, 'wb') as target_file:
        target_file.write(file2.read())
        target_file.write(file1.read())

    os.remove(temp_text)
    os.remove(temp_off)
    os.remove(tsv_file_path)


url = 'https://docs.google.com/spreadsheets/'
tsv_file_path = 'TEXT.tsv'
download_gsheets(url, tsv_file_path)
temp_text = '1.text'
temp_off = '1.off'
dat_file_path = '1_a.dat'
process_data(tsv_file_path, temp_text, temp_off, dat_file_path)
