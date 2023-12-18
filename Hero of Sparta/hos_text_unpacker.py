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


def process_data(off_file_path, dat_file_path, output_file_path):
    with open(off_file_path, 'rb') as off_file, open(dat_file_path, 'rb') as dat_file:
        count_str = struct.unpack('H', off_file.read(2))[0]
        block_off = count_str * 2

        offsets = [0]

        for i in range(count_str):
            offset = struct.unpack('H', off_file.read(2))[0]
            offsets.append(offset)

        data = dat_file.read()

        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for i in range(count_str):
                start_off = offsets[i]
                end_off = offsets[i + 1] - 1 if i < count_str - 1 else block_off
                text = data[start_off:end_off].decode('utf-8')
                encode = text.translate(translation_table)
                encode2 = EncodeText(encode)
                output_file.write(encode2 + '\n')
                print(encode2)


off_file_path = '2_5411.dat'
dat_file_path = '1_3e.dat'
output_file_path = 'output.txt'
process_data(off_file_path, dat_file_path, output_file_path)
