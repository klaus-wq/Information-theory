import math

text = input("\nШифруемая строка: ")

flag = 0 
symb = [] #список из пары(символ:частота)

#ищем частоты каждого символа и записываем в список
for i in range(len(text)):
    for j in range(len(symb)):
        if text[i] == symb[j][0]:
            symb[j][1] += 1
            flag = 1
    if flag == 0:
        symb.append([text[i], 1]) #добавляем элемент [символ:частота] в конец списка
    flag = 0

symb.sort(key = lambda i: i[1]) #сортируем список на основе функции key, по возрастанию частот

codes = [] #список кодов символов

#добавляем в список. Нулевой столбец списка codes = символу из symb, а первый - его код 
for i in range(len(symb)):
    codes.append([symb[i][0], ""])

while len(symb) > 1: 
    tmp1 = symb.pop(0) #удалил нулевой из symb и записали нулевой в tmp1
    tmp2 = symb.pop(0) #удалил первый и записали его
    #пробегаем всю таблицу кодов и находим в ней символы tmp0, tmp1
    for i in range(len(codes)):
        if codes[i][0] in tmp1[0]: #символ в кодах = символу в tmp?
            codes[i][1] = '0' + codes[i][1]
        if codes[i][0] in tmp2[0]:
            codes[i][1] = '1' + codes[i][1]
    symb.append([tmp1[0] + tmp2[0], tmp1[1] + tmp2[1]]) #добавляем в symb суммарный символ. Два символа в один = tmp1+tmp2 (удалённые)
    symb.sort(key = lambda i: i[1]) #сортировка по возрастанию частот
 
print("\nХаффман:\n")
for i in range(len(codes)):
    print("%s - %s"%(codes[i][0], codes[i][1]))

result = []
for i in range(len(codes)):
    result.append(codes[i][1])

encoded = ""
for i in range(len(text)):
    for j in range(len(codes)):
         if text[i] == codes[j][0]:
            encoded += codes[j][1]
            encoded += ' '
print(encoded)

split_encoded = []
split_encoded = encoded.split()

decoded = ""
for i in range(len(split_encoded)):
    for j in range(len(codes)):
         if split_encoded[i] == codes[j][1]:
            decoded += codes[j][0]
print(decoded)
