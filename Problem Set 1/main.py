import numpy as np
tmparr = []
generator_matrix = [[1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                    [1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
                    [1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0],
                    [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0],
                    [1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                    [1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                    [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1]]
def codeMessage(m):
    message = np.array(m)
    print("oryginal message:", message)
    finalAdd = []
    for y in range(8):
        tmp = 0;
        for x in range(8):
            if generator_matrix[y][x] == 1 and message[x] == 1:
                tmp += 1
        if tmp%2 != 0:
            finalAdd.append(1)
        else:
            finalAdd.append(0)

    finalAdd = np.array(finalAdd)
    print("finaladd: ", finalAdd)
    codeword = np.concatenate([message, finalAdd])
    return codeword


def decodeMessage(codeword):
    for y in range(8):
        tmp = 0;
        for x in range(8):
            tmp += (codeword[x] * generator_matrix[y][x])
        tmp += codeword[8 + y]
        if tmp%2 != 0:
            tmparr.append(1)
        else:
            tmparr.append(0)

def getColumnFromGeneratorMatrix(columnNumber):
    column = [row[columnNumber] for row in generator_matrix]
    return column

def tryToRepairThat():
    for i in range(16):
        if(tmparr == getColumnFromGeneratorMatrix(i)):
            print("ERROR ON POSITION: ", i)


def bits_to_char(bits):
    bits_str = ''.join([str(bit) for bit in bits])
    char = chr(int(bits_str, 2))
    return char

def char_to_bits(char):
    binary_string = bin(ord(char))[2:].zfill(8)
    bits = [int(bit) for bit in binary_string]
    return bits

codeword = codeMessage(char_to_bits('a'))
print("codeword:", codeword)
codeword = [0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1]
decodeMessage(codeword)
print("column to repair: ", tmparr)
tryToRepairThat()


