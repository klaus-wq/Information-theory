import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
import copy

#индексы для буквенно-цифрового кодирвоания
indexes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
           'T', 'U', 'V', 'W', 'X', 'Y', 'Z', ' ', '$', '%', '*', '+', '-', '.', '/', ':']

#максимальное количество полезной информации вместе со служебной (в битах) для M(15%), версия 1
MAX_LEN = 128
#количество блоков
AMOUNT_OF_BLOCKS = 1
#номер версии
V = 1
#количество байтов коррекции для версии
AMOUNT_OF_CORRECTION_BYTES = 10
# Генерирующий многочлен
GENERATING_POLYNOMS = [251, 67, 46, 61, 118, 70, 64, 94, 32, 45]                   

#Поле Галуа
GALOIS_FIELD = [ 1, 2, 4, 8, 16, 32, 64, 128, 29, 58, 116, 232, 205, 135, 19, 38,
                            76, 152, 45, 90, 180, 117, 234, 201, 143, 3, 6, 12, 24, 48, 96, 192,
                            157, 39, 78, 156, 37, 74, 148, 53, 106, 212, 181, 119, 238, 193, 159, 35,
                            70, 140, 5, 10, 20, 40, 80, 160, 93, 186, 105, 210, 185, 111, 222, 161,
                            95, 190, 97, 194, 153, 47, 94, 188, 101, 202, 137, 15, 30, 60, 120, 240,
                            253, 231, 211, 187, 107, 214, 177, 127, 254, 225, 223, 163, 91, 182, 113, 226,
                            217, 175, 67, 134, 17, 34, 68, 136, 13, 26, 52, 104, 208, 189, 103, 206,
                            129, 31, 62, 124, 248, 237, 199, 147, 59, 118, 236, 197, 151, 51, 102, 204,
                            133, 23, 46, 92, 184, 109, 218, 169, 79, 158, 33, 66, 132, 21, 42, 84,
                            168, 77, 154, 41, 82, 164, 85, 170, 73, 146, 57, 114, 228, 213, 183, 115,
                            230, 209, 191, 99, 198, 145, 63, 126, 252, 229, 215, 179, 123, 246, 241, 255,
                            227, 219, 171, 75, 150, 49, 98, 196, 149, 55, 110, 220, 165, 87, 174, 65,
                            130, 25, 50, 100, 200, 141, 7, 14, 28, 56, 112, 224, 221, 167, 83, 166,
                            81, 162, 89, 178, 121, 242, 249, 239, 195, 155, 43, 86, 172, 69, 138, 9,
                            18, 36, 72, 144, 61, 122, 244, 245, 247, 243, 251, 235, 203, 139, 11, 22,
                            44, 88, 176, 125, 250, 233, 207, 131, 27, 54, 108, 216, 173, 71, 142, 1]

# Обратное поле Галуа
REV_GALOIS_FIELD = [ -1, 0, 1, 25, 2, 50, 26, 198, 3, 223, 51, 238, 27, 104, 199, 75,
                     4, 100, 224, 14, 52, 141, 239, 129, 28, 193, 105, 248, 200, 8, 76, 113,
                     5, 138, 101, 47, 225, 36, 15, 33, 53, 147, 142, 218, 240, 18, 130, 69,
                     29, 181, 194, 125, 106, 39, 249, 185, 201, 154, 9, 120, 77, 228, 114, 166,
                     6, 191, 139, 98, 102, 221, 48, 253, 226, 152, 37, 179, 16, 145, 34, 136,
                     54, 208, 148, 206, 143, 150, 219, 189, 241, 210, 19, 92, 131, 56, 70, 64,
                     30, 66, 182, 163, 195, 72, 126, 110, 107, 58, 40, 84, 250, 133, 186, 61,
                     202, 94, 155, 159, 10, 21, 121, 43, 78, 212, 229, 172, 115, 243, 167, 87,
                     7, 112, 192, 247, 140, 128, 99, 13, 103, 74, 222, 237, 49, 197, 254, 24,
                     227, 165, 153, 119, 38, 184, 180, 124, 17, 68, 146, 217, 35, 32, 137, 46,
                     55, 63, 209, 91, 149, 188, 207, 205, 144, 135, 151, 178, 220, 252, 190, 97,
                     242, 86, 211, 171, 20, 42, 93, 158, 132, 60, 57, 83, 71, 109, 65, 162,
                     31, 45, 67, 216, 183, 123, 164, 118, 196, 23, 73, 236, 127, 12, 111, 246,
                     108, 161, 59, 82, 41, 157, 85, 170, 251, 96, 134, 177, 187, 204, 62, 90,
                     203, 89, 95, 176, 156, 169, 160, 81, 11, 245, 22, 235, 122, 117, 44, 215,
                     79, 174, 213, 233, 230, 231, 173, 232, 116, 214, 244, 234, 168, 80, 88, 175 ]

#для отрисовки
SEARCH_ELEMENT = [
    [1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,1,0,1],
    [1,0,1,0,0,0,1,0,1],
    [1,0,1,0,0,0,1,0,1],
    [1,0,1,0,0,0,1,0,1],
    [1,0,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1]]

def coding(text):
    i = 0
    split_by_two_to_bin = ""
    for i in range(i, len(text), 2):
        split_by_two = text[i:i+2]
        print(split_by_two)
        if len(split_by_two) == 2:
            temp1 = 45*indexes.index(split_by_two[0]) + indexes.index(split_by_two[1])
            temp = bin(temp1)[2:]
            split_by_two_to_bin += temp.rjust(11, '0') 
        if len(split_by_two) == 1:
            temp = bin(indexes.index(split_by_two))[2:] 
            split_by_two_to_bin += temp.rjust(6, '0')  
    add_inf = "0010" + (bin(int(len(text)))[2:]).rjust(9, '0') + split_by_two_to_bin
    return add_inf

def fill_to_certain_length(for_fill):
    #заполнение до MAX_LEN
    addit_byte1 = "11101100"
    addit_byte2 = "00010001"

    for i in range(0,4):
        if len(for_fill) != MAX_LEN:
            for_fill += '0'

    #последовательность кратна 8
    while len(for_fill) % 8 != 0:
        for_fill += '0'

    i = 0
    while len(for_fill) != MAX_LEN:
        if i % 2 == 0:
            for_fill += addit_byte1
            i +=1
        else:
            for_fill += addit_byte2
            i += 1
    return for_fill

def forming_blocks(whole_data):
    bytes1 = []
    for k in range(0, len(whole_data), 8):
        bytes1.append(int(whole_data[k:k+8], 2))
    return bytes1

def create_correcting_bytes(blocks_):
    len_blocks = len(blocks_)
    while len(blocks_) < AMOUNT_OF_CORRECTION_BYTES: 
        blocks_.append(0)
    for j in range(0, len_blocks): 
        temp_A = blocks_[0]
        blocks_.pop(0)
        blocks_.append(0)
        if temp_A == 0:
            continue
        temp_B = REV_GALOIS_FIELD[temp_A]
        place = 0
        for k in GENERATING_POLYNOMS:
            temp_D = (temp_B + k) % 255
            temp_D = GALOIS_FIELD[temp_D]
            blocks_[place] ^= temp_D 
            place += 1
    #обрезаем нули с конца в коррект блоке
    while len(blocks_) > AMOUNT_OF_CORRECTION_BYTES:
        blocks_.pop()
    return blocks_

def draw_search_pattern(pixels):
    #3 поисковых узора
    for i in range(len(SEARCH_ELEMENT)-1):
        for j in range(len(SEARCH_ELEMENT)-1):
            pixels[i][j] = SEARCH_ELEMENT[i+1][j+1]  # левый верхний 
            pixels[i][len(pixels) - 8 + j] = SEARCH_ELEMENT[i+1][j]  # левый нижний
            pixels[len(pixels) - 8 + i][j] = SEARCH_ELEMENT[i][j+1]  # правый верхний
    return pixels

def draw_timing_strip(pixels):
    #полосы синхронизации
    i = 8
    for i in range(i, len(pixels)-8):
        if i % 2 != 0:
            pixels[6][i] = 1
            pixels[i][6] = 1
            continue
        pixels[6][i] = 0
        pixels[i][6] = 0
    return pixels

def draw_code_mask_and_correct_level(pixels):
    code = "101010000010010" # нулевая маска и уровень корекции М 15%
    # заполняем вокруг левого верхнего
    # 0-7 биты
    place = 0
    for j in range(0,8):
        if pixels[8][j] ==-1:
            pixels[8][j] = int(code[place]) ^ 1
            place +=1

    i = 8
    while i >=0:
        if pixels[i][8] ==-1:
            pixels[i][8] = int(code[place])^1
            place +=1
        i -=1
    place = 0
    j = len(pixels)-1
    while j > len(pixels)-8:
        if pixels[j][8] ==-1:
            pixels[j][8] = int(code[place])^1
            place +=1
        j -=1
    pixels[len(pixels)-8][8] = 0 # ставим черный статичный модуль
    j = len(pixels)-8
    while j < len(pixels):
        if pixels[8][j] ==-1:
            pixels[8][j] = int(code[place])^1
            place +=1
        j +=1

    return pixels

def is_mask_true(row,col):
    return (row+col)%2 == 1 #если маска равна единице не инвертируем бит

def draw_data(pixels, data):
    size = len(pixels)
    str_bits = ""
    for k in data:
        str_bits += (bin(k)[2:]).rjust(8, '0')

    i = size - 1
    j = size - 1
    place = 0
    up_forw_module = True
    while j > 0: # идём по столбцам справа налево и отнимаем 2
        if up_forw_module:
            for i in range(size-1,-1,-1):
                if pixels[i][j]==-1: #правый
                    pixels[i][j] = (int(str_bits[place]) ^ 1) if is_mask_true(i,j) else int(str_bits[place])
                    place +=1
                if pixels[i][j-1] == -1: #левый
                    pixels[i][j-1] = (int(str_bits[place]) ^ 1) if is_mask_true(i,j-1) else int(str_bits[place])
                    place += 1
            up_forw_module = False #следующий модуль вниз идёт
        else:
            for i in range(0,size,1):
                if pixels[i][j]==-1: #правый
                    pixels[i][j] = (int(str_bits[place])^1) if is_mask_true(i,j) else int(str_bits[place])
                    place +=1
                if pixels[i][j-1] == -1: #левый
                    pixels[i][j-1] = (int(str_bits[place])^1) if is_mask_true(i,j-1) else int(str_bits[place])
                    place += 1
            up_forw_module = True #следующий модуль вверх идёт
        j -=2
        if j == 6: #левая полоса синхронизации
            j -= 1
    return pixels

text = input("Введите данные: ")
text1 = coding(text)
print('Буквенно-цифровое кодрование: ', text1)
ready_to_form_blocks: str = fill_to_certain_length(text1)
print('Заполненная: ', ready_to_form_blocks)
blocks = forming_blocks(ready_to_form_blocks)
print('Блоки: ', blocks)
blocks_of_correct = copy.deepcopy(blocks)
create_correcting_bytes(blocks_of_correct)
print('Корректирующие блоки: ', blocks_of_correct)
data = blocks + blocks_of_correct
print('Объединённые блоки: ', data)

img = Image.new('1', (21+8, 21+8), color='white')
pixels = np.full((21,21),-1)
img_pixels = img.load()

draw_search_pattern(pixels)
print('pix1', pixels)
draw_timing_strip(pixels)
print('pix2', pixels)
draw_code_mask_and_correct_level(pixels)
print('pix3', pixels)
draw_data(pixels,data)
print('pix4', pixels)

#переводим nd.array  в пиксели
for i in range(img.size[0]-8):
    for j in range(img.size[0]-8):
        if(pixels[i][j] != -1):
            img_pixels[j+4, i+4] = int(pixels[i][j])

plt.imshow(np.asarray(img), cmap='gray') 
plt.show()




