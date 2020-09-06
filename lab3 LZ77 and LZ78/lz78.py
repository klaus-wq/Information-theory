def compress(charstream):
    dictionary = {} #временной словарь (символ, номер)
    prefix = "" #то, что повторилось(уже было в словаре)
    codestream = [] #закодированная строка - список (номер в словаре самого длинного найденного префикса, следующий за ним символ)
    i = 0 #индекс символа
    while i < len(charstream):
        char = charstream[i] #разбиваем строку на символы, берём один символ
        try:
            dictionary[prefix + char]  #есть ли символ в слоавре? Если нет, то except
            prefix = prefix + char #да, то следующий символ
        except (KeyError): #если такого ключа(символа) нет в словаре
            if prefix == "":
                offset = 0
            else:
                offset = dictionary[prefix]
            codestream.append((offset, char)) #добавление (смещение, символ)
            dictionary[prefix + char] = len(dictionary) + 1 #увеличили для символа его номер
            prefix = ""
        
        i += 1 #следующий символ
    
        if (prefix != "") and (i >= len(charstream)): #для последнего символа, который есть в словаре уже
            codestream.append((dictionary[prefix], ""))
            break
    return codestream

def decompress(codestream):
    dictionary = [] 
    prefix = ""
    charstream = ""
    for (offset, char) in codestream:
        if offset == 0: #не было символа - просто текущий символ в словарь
            prefix = ""
        else:
            prefix = dictionary[offset-1] #символ + предыдущий в словарь
        dictionary.append(prefix + char)
    for s in dictionary: 
        charstream += s #собираем строку
    return charstream

text = input("Введите шифруемую строку: ")
encoded = compress(text)
print(encoded)
decoded = decompress(encoded)
print(decoded)
