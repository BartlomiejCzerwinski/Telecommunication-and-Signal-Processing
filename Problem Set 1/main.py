import numpy as np

generator_matrix = [[1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                    [1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
                    [1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0],
                    [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0],
                    [1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                    [1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                    [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1]]
def codeMessage(message):
    codeword = ""
    for character in message:
        characterAsBits = char_to_bits(character)
        characterAsBits = np.array(characterAsBits)
        bitsToAdd = []
        for y in range(8):
            tmp = 0
            for x in range(8):
                if generator_matrix[y][x] == 1 and characterAsBits[x] == 1:
                    tmp += 1
            if tmp%2 != 0:
                bitsToAdd.append(1)
            else:
                bitsToAdd.append(0)

        bitsToAdd = np.array(bitsToAdd)
        codeword = codeword + numpyArrayToString(np.concatenate([characterAsBits, bitsToAdd]))
    return codeword

def decodeMessage(codeword):
    tmpStr = ""
    result = ""
    for c in codeword:
        tmpStr += c
        if len(tmpStr) == 16:
            tmparr = []
            codewordArray = stringToNumpyArray(tmpStr)
            for y in range(8):
                tmp = 0
                for x in range(8):
                    tmp += (codewordArray[x] * generator_matrix[y][x])
                tmp += codewordArray[8 + y]
                if tmp%2 != 0:
                    tmparr.append(1)
                else:
                    tmparr.append(0)
            afterErrorsRepair = correctErrors(tmparr, codewordArray)
            afterErrorsRepair = numpyArrayToString(afterErrorsRepair)
            result += bits_to_char(cutOffParityBits(afterErrorsRepair))
            tmpStr = ""
    return result

def correctErrors(errorsArray, codeword):
    if errorsArray == [0, 0, 0, 0, 0, 0, 0, 0]:
        return codeword

    for i in range(16):                                         #try to correct one bit error
        if (errorsArray == getColumnFromGeneratorMatrix(i)):
            codeword[i] = switchBit(codeword[i])
            return codeword

    for i in range(16):                                         #try to correct two bits error
        for j in range(15):
            tmp = []
            columnA = getColumnFromGeneratorMatrix(i)
            columnB = getColumnFromGeneratorMatrix(j)
            for k in range(8):
                tmp.append((columnA[k] + columnB[k]) % 2)
            if tmp == errorsArray:
                codeword[i] = switchBit(codeword[i])
                codeword[j] = switchBit(codeword[j])
                return codeword

def stringToNumpyArray(stringToConvert):
    tmp = []
    for i in stringToConvert:
        if i == "1":
            tmp.append(1)
        else:
            tmp.append(0)
    return np.array(tmp)

def codewordToAsciiChars(codeword):
    arr = stringToNumpyArray(codeword)
    i = 0
    result = ""
    tmp = []
    for a in arr:
        tmp.append(a)
        i += 1
        if i == 8:
            result += bits_to_char2(tmp)
            tmp = []
            i = 0
    return result

def asciiCharsToCodeword(asciiChars):
    result = ""
    for c in asciiChars:
        result += numpyArrayToString(np.array(char_to_bits(c)))
    return result

def bits_to_char2(bits):
    bits_str = ''.join([str(bit) for bit in bits])
    char = chr(int(bits_str, 2))
    return char

def numpyArrayToString(npArray):
    result = ""
    for i in npArray:
        if i == 1:
            result += "1"
        else:
            result +="0"
    return result

def getColumnFromGeneratorMatrix(columnNumber):
    column = [row[columnNumber] for row in generator_matrix]
    return column

def switchBit(bitToSwitch):
    if bitToSwitch == 1:
        bitToSwitch = 0;
    else:
        bitToSwitch = 1;
    return bitToSwitch
def bits_to_char(bits):
    bits = cutOffParityBits(bits)
    bits_str = ''.join([str(bit) for bit in bits])
    char = chr(int(bits_str, 2))
    return char

def char_to_bits(char):
    char = chr(char)
    binary_string = bin(ord(char))[2:].zfill(8)
    bits = [int(bit) for bit in binary_string]
    return bits

def cutOffParityBits(bitsToCutOff):
    return bitsToCutOff[:8]

def loadFile(filename):
    file = open(filename, 'rb')
    result = file.read()
    file.close()
    return result

def saveFile(filename, data):
    file = open(filename, 'wb')
    file.write(data)
    file.close()

while(1):
    print("Co chcesz zrobic?")
    print("1. Zakodowac wiadomosc")
    print("2. Odkodowac wiadomosc")
    print("3. Wyjscie z programu")
    choice = input("Wybor: ")
    if choice == "1":
        fileWithMessageToCode = input("Podaj nazwe pliku z wiadomoscia do zakodowania: ")
        fileToSaveCodeword = input("Podaj nazwe pliku do zapisania zakodowanej wiadomosci: ")
        codeword = codeMessage(loadFile(fileWithMessageToCode))
        codeword = codewordToAsciiChars(codeword)
        saveFile(fileToSaveCodeword, codeword)
        print("Zakodowano wiadomosc")
    elif choice == "2":
        fileWithCodedMessage = input("Podaj nazwe pliku z wiadomoscia do odkodowania: ")
        print("Odkodowana wiadomosc:")
        codedMessage = loadFile(fileWithCodedMessage)
        print(decodeMessage(asciiCharsToCodeword(codedMessage)))
    elif choice == "3":
        exit()
    else:
        print("Nie ma takiej opcji!")