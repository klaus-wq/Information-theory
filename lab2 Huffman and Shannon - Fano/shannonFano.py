#делим на две группы
def split(items):
    summ = sum(item[1] for item in items) #сумма всех частот
    index = 0
    summ_freq = 0 
    min_difference = summ

    for item in items:
        summ_freq += item[1] #частота первого эл-та +=
        difference = abs(summ - 2 * summ_freq) 
        if min_difference > difference:
            min_difference = difference
        else:
            break

        index += 1
    return items[:index], items[index:] #возвращаем две группы

#собственно, кодируем
def shannon_fano(items):
    if len(items) == 1:
        return

    first, second = split(items)

    for item in first:
        item[2] += '0'

    for item in second:
        item[2] += '1'

#рекурсия
    shannon_fano(first)
    shannon_fano(second)

def main():

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

    #формируем список частот
    freq = []
    for i in range(len(symb)):
        freq.append(symb[i][1])

    #формируем список символов
    char = []
    for i in range(len(symb)):
        char.append(symb[i][0])

    #формируем список items, состоящий из символа, частота, код
    items = []
    for i in range(len(symb)):
        items.append(([char[i], freq[i], '']))

    #сортируем по убыванию частот
    items = sorted(items, key=lambda x: x[1], reverse=True)
    shannon_fano(items)

    for item in items:
        print(item[0], "-", item[2])

    result = []
    for item in items:
        result.append([item[2]])

    encoded = ""
    for i in range(len(text)):
        for item in items:
            if text[i] == item[0]:
                encoded += item[2]
                encoded += ' '
    print(encoded)

    split_encoded = []
    split_encoded = encoded.split()

    decoded = ""
    for i in range(len(split_encoded)):
        for item in items:
            if split_encoded[i] == item[2]:
                decoded += item[0]
    print(decoded)

if __name__ == '__main__':
    main()

