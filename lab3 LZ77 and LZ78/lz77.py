def find_in_dict(buffer, dictionary): 
    shift = len(dictionary)  # длина словаря изначальная
    substring = ""  # подстрока, которая совпала

    for character in buffer: #каждый символ в буфере
        substring_tmp = substring + character #подстрока + символ
        
        shift_tmp = dictionary.rfind(substring_tmp) # возвращает последний индекс, в котором находится подстрока

        if shift_tmp < 0:  # -1, если нет в словаре
            break

        substring = substring_tmp
        shift = shift_tmp

    # возвращает пару (длина совпадающей подстроки, смещение назад от текущей позиции(длина словаря без нового эл-та))
    return len(substring), len(dictionary) - shift

def compress(message, buffer_size, dictionary_size):
    dictionary = ""
    buffer = message[:buffer_size]  # обрезаем сообщение до длины буфера
    output = []  # закодированное сообщение

    while len(buffer) != 0:  # идем по буферу(пока не пуст)
        size, shift = find_in_dict(buffer, dictionary) 

        dictionary += message[:size + 1] #добавляем в словарь префикс(до подстроки + символ)
        #dictionary = dictionary[-dictionary_size:] #длину оставляем, обрезка с конца

        message = message[size:] #сообщение без найденной подстроки
        next_character = message[:1] #следующий символ - первый символ в сообщении
        message = message[1:] #сообщение без первого символа

        buffer = message[:buffer_size] #буфер - следующие 4(n) символа без закодированного
        output.append((shift, size, next_character)) #добавить тройку (смещение  назад от текущей позиции, длина совпадающей подстроки, следующий символ)
    return output

def decompress(compressed_message):
    message = "" #раскодированное сообщение
    for part in compressed_message: #для каждой тройки
        shift, size, character = part
        message = message + message[-shift:][:size] + character #по раскодированной строке идём назад, выводим подстроку и символ
    return message

text = input("Введите шифруемую строку: ")
buffer_size = int(input("Введите размер буфера: "))
dictionary_size = len(text)
#dictionary_size = int(input("Введите размер словаря: "))
encoded = compress(text, buffer_size, dictionary_size)
print(encoded)
decoded = decompress(encoded)
print(decoded)

