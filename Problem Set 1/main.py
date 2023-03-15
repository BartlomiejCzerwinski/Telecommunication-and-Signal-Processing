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
        character = char_to_bits(character)
        m = np.array(character)
        finalAdd = []
        for y in range(8):
            tmp = 0;
            for x in range(8):
                if generator_matrix[y][x] == 1 and m[x] == 1:
                    tmp += 1
            if tmp%2 != 0:
                finalAdd.append(1)
            else:
                finalAdd.append(0)

        finalAdd = np.array(finalAdd)
        codeword = codeword + numpyArrayToString(np.concatenate([m, finalAdd]))
    return codeword

def numpyArrayToString(npArray):
    result = ""
    for i in npArray:
        if i == 1:
            result += "1"
        else:
            result +="0"
    return result

def stringToNumpyArray(stringToConvert):
    tmp = []
    for i in stringToConvert:
        if i == "1":
            tmp.append(1)
        else:
            tmp.append(0)
    return np.array(tmp)



def decodeMessage(codeword):
    tmpStr = ""
    res = ""
    for c in codeword:
        tmpStr += c
        if len(tmpStr) == 16:
            tmparr = []
            codewordArray = stringToNumpyArray(tmpStr)
            for y in range(8):
                tmp = 0;
                for x in range(8):
                    tmp += (codewordArray[x] * generator_matrix[y][x])
                tmp += codewordArray[8 + y]
                if tmp%2 != 0:
                    tmparr.append(1)
                else:
                    tmparr.append(0)
            afterErrorsRepair = correctErrors(tmparr, codewordArray)
            afterErrorsRepair = numpyArrayToString(afterErrorsRepair)
            res += bits_to_char(cutOffParityBits(afterErrorsRepair))
            tmpStr = ""
    return res

def getColumnFromGeneratorMatrix(columnNumber):
    column = [row[columnNumber] for row in generator_matrix]
    return column

def correctErrors(errorsArray, codeword):
    if errorsArray == [0, 0, 0, 0, 0, 0, 0, 0]:
        return codeword

    for i in range(16):
        if (errorsArray == getColumnFromGeneratorMatrix(i)):
            codeword[i] = switchBit(codeword[i])
            return codeword
    for i in range(16):
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
    binary_string = bin(ord(char))[2:].zfill(8)
    bits = [int(bit) for bit in binary_string]
    return bits

def cutOffParityBits(bitsToCutOff):
    return bitsToCutOff[:8]

def loadFile(filename):
    file = open(filename, 'r')
    result = file.read()
    file.close()
    return result

def saveFile(filename, data):
    file = open(filename, 'w')
    file.write(data)
    file.close()


codeword = codeMessage('To jest przykladowy tekst')
saveFile("firstSave.txt", codeword)

x = loadFile("firstSave.txt")
print(decodeMessage(x))




