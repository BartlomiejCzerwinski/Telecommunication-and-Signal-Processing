import numpy as np

def codeMessage(m):
    message = np.array(m)
    print("oryginal message:", message)
    generator_matrix = [[1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                        [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                        [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
                        [1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
                        [1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
                        [0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0],
                        [1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1]]
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
    generator_matrix = [[1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                        [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                        [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
                        [1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
                        [1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
                        [0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0],
                        [1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1]]

    for y in range(8):
        tmp = 0;
        for x in range(8):
            tmp += (codeword[x] * generator_matrix[y][x])
        tmp += codeword[8 + y]
        print(tmp%2)


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
decodeMessage(codeword)


