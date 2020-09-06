import fractions as fr

text = input("Введите шифруемую строку: ")

#Кодирование
freq = {}
text1 = ""
for i in range(len(text)):
    if text[i] in freq:
        freq[text[i]] += 1
    else:
        text1 += text[i]
        freq[text[i]] = 1 
#freq = [text.count(i) for i in (set(list(text)))]
#prob = [text.count(i) / len(text) for i in (set(list(text)))]
prob = {}
for i in range(len(text1)):
    prob[text1[i]] = freq[text1[i]]/len(text)

intervals = {}
low = fr.Fraction(0, 1)
for item in freq:
    high = fr.Fraction(freq[item], len(text))
    intervals[item] = [low, low+high]
    low = low+high

print("Символ | Частота | Относительная частота |       Интервал")
for i in range(len(text1)):
    print("%4c%8d%15f%25f%10f" %(text1[i], freq[text1[i]], prob[text1[i]], intervals[text1[i]][0], intervals[text1[i]][1]))
print("----------------------------------------------------------------------------------------")

for item in intervals:
    print(item, end=" ")
    print(intervals[item][0], end=" ")
    print(intervals[item][1])

oldLow = fr.Fraction(0, 1)
oldHigh = fr.Fraction(1, 1)
newLow = fr.Fraction(0, 1)
newHigh = fr.Fraction(1, 1)

print("Символ | Нижняя граница | Верхняя граница")
for ch in text:
    newLow = oldLow + (oldHigh - oldLow) * intervals[ch][0]
    newHigh = oldLow + (oldHigh - oldLow) * intervals[ch][1]
    oldLow = newLow
    oldHigh = newHigh
    print("%5c%15f%20f" %(ch, newLow, newHigh))
    #print(ch, newLow, newHigh)
print("------------------------------------------------------------")
print(oldLow, oldHigh)
print(float(oldLow))

#Декодирование
decoded = oldLow
for i in range(len(text)):
    for item in intervals:
        if decoded >= intervals[item][0] and decoded < intervals[item][1]:
            print(item, end="")
            decoded = (decoded-intervals[item][0])/(intervals[item][1]-intervals[item][0]) #удаление влияния символа item текста
            #print(item, decoded)
            break







