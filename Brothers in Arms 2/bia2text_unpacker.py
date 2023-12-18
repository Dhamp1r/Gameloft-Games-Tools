import struct

translation_table = str.maketrans(
    'ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ¡¢¹º²³§¨¼½¾¿',
    'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюяЁёЄєІіЇїҐґ–…'
)

def EncodeText(string):
    string = string.replace("\x0A", "\\n")
    string = string.replace("\x00", "[x00]")
    string = string.replace("\x01", "[x01]")
    string = string.replace("\x02", "[x02]")
    string = string.replace("\x03", "[x03]")
    string = string.replace("\x04", "[x04]")
    string = string.replace("\x05", "[x05]")
    string = string.replace("\x06", "[x06]")
    string = string.replace("\x07", "[x07]")
    string = string.replace("\x08", "[x08]")
    string = string.replace("\x09", "[x09]")
    string = string.replace("\x10", "[x10]")
    string = string.replace("\x11", "[x11]")
    string = string.replace("\xFF", "[xFF]")
    string = string.replace("\x0E", "[x0E]")
    string = string.replace("\x0F", "[x0F]")
    string = string.replace("\x2B", "[x2B]")
    return string


def process_data(dat_file_path, output_file_path):
    with (open(dat_file_path, 'rb') as dat_file, open(output_file_path, 'w', encoding='utf-16') as output_file):
        count_str = struct.unpack('I', dat_file.read(4))[0]

        offsets = []

        for i in range(count_str):
            offset = struct.unpack('I', dat_file.read(4))[0]
            offsets.append(offset)

        data = dat_file.read()

        for i in range(count_str):
            start_off = offsets[i]
            end_off = offsets[i+1] - 2 if i < count_str - 1 else len(data) - 2
            text = data[start_off:end_off].decode('utf-16')
            encode = text.translate(translation_table)
            encode2 = EncodeText(encode)
            output_file.write(encode2 + '\n')

    print(f'{dat_file_path} exported to {output_file_path}')


dat_file_path = '1_a.dat'
output_file_path = 'output.txt'
process_data(dat_file_path, output_file_path)
