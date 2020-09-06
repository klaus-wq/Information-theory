text = input("Введите шифруемую строку: ")

stroka = list(text.encode('ascii'))
print(stroka)

for i in range (len(stroka)):
    stroka[i] = bin(stroka[i])
    stroka[i] = stroka[i][2:]
print(stroka)

for i in range(len(stroka)):
    for j in range(len(stroka[i])):
        if len(stroka[i]) < 7:
            stroka[i] = '0' + stroka[i]

print(stroka)

for i in range(len(stroka)):
    stroka[i] = '00' + stroka[i]
    stroka[i] = stroka[i][:3] + '0' + stroka[i][3:]
    stroka[i] = stroka[i][:7] + '0' + stroka[i][7:]
#print(stroka)

def coding(stroka1):
    for i in range(len(stroka1)):
        if (int(stroka1[i][0])+int(stroka1[i][2])+int(stroka1[i][4])+int(stroka1[i][6])+int(stroka1[i][8])+int(stroka1[i][10])) % 2 == 1:
            stroka1[i] = '0' + stroka1[i][1:]
        else:
            stroka1[i] = '1' + stroka1[i][1:]
            
        if (int(stroka1[i][1])+int(stroka1[i][2])+int(stroka1[i][5])+int(stroka1[i][6])+int(stroka1[i][9])+int(stroka1[i][10])) % 2 == 1:
            stroka1[i] = stroka1[i][:1] + '0' + stroka1[i][2:]
        else:
            stroka1[i] = stroka1[i][:1] + '1' + stroka1[i][2:]

        if (int(stroka1[i][3])+int(stroka1[i][4])+int(stroka1[i][5])+int(stroka1[i][6])) % 2 == 1:
            stroka1[i] = stroka1[i][:3] + '0' + stroka1[i][4:]
        else:
            stroka1[i] = stroka1[i][:3] + '1' + stroka1[i][4:]

        if (int(stroka1[i][7])+int(stroka1[i][8])+int(stroka1[i][9])+int(stroka1[i][10])) % 2 == 1:
            stroka1[i] = stroka1[i][:7] + '0' + stroka1[i][8:]
        else:
            stroka1[i] = stroka1[i][:7] + '1' + stroka1[i][8:]  
    return stroka1                                              

stroka = coding(stroka)

for i in range(len(text)):
    print(text[i], stroka[i])

encoded = ""
for i in range(len(stroka)):
    encoded += str(stroka[i])
print(encoded)

str_decode = input("Введите искажённую строку: ")
#print(str_decode)

for i in range(len(str_decode)):
    if (str_decode[i] != '0') and (str_decode[i] != '1'):
        print("Неверные данные!")
        quit()
if len(str_decode) != len(stroka)*11:
    print("Неверная длина сообщения!")
    quit()

msg_str_decode = []
while str_decode != '':
    msg_str_decode.append(str_decode[:11])
    str_decode = str_decode[11:]
print(msg_str_decode)

for i in range(len(msg_str_decode)):
    msg_str_decode[i] = '00' + msg_str_decode[i][2:]
    msg_str_decode[i] = msg_str_decode[i][:3] + '0' + msg_str_decode[i][4:]
    msg_str_decode[i] = msg_str_decode[i][:7] + '0' + msg_str_decode[i][8:]
print(msg_str_decode)
msg_str_decode = coding(msg_str_decode)
print(msg_str_decode)

error = []                             
for i in range(len(stroka)):
    error_count = 0
    if (stroka[i] != msg_str_decode[i]):
        for j in range(len(stroka[i])):
            if (stroka[i][j] != msg_str_decode[i][j]) and ((j==0) or (j==1) or (j==3) or (j==7)):
                    error_count = error_count + j + 1
    error.append(error_count)
print(error)

for i in range(len(msg_str_decode)):               
    if error[i] == 0:
        i = i + 1
    else:
        if int(msg_str_decode[i][(error[i]) - 1]) == 0:
            msg_str_decode[i] = msg_str_decode[i][:(error[i] - 1)] + '1' + msg_str_decode[i][(error[i]):]
        else:
            msg_str_decode[i] = msg_str_decode[i][:(error[i] - 1)] + '0' + msg_str_decode[i][(error[i]):]
print(msg_str_decode)

decoded = ""
for i in range(len(msg_str_decode)):
    decoded += str(msg_str_decode[i])
print(decoded)

msg = ''
for i in range(len(msg_str_decode)):
    msg_str_decode[i] = msg_str_decode[i][2] + msg_str_decode[i][4:7] + msg_str_decode[i][8:]
    #print(msg_str_decode[i])
    print(chr(int(msg_str_decode[i], base = 2)), msg_str_decode[i])
    msg_str_decode[i] = chr(int(msg_str_decode[i], base = 2))
    msg = msg + msg_str_decode[i]
print("Исходное сообщение: ", msg)








