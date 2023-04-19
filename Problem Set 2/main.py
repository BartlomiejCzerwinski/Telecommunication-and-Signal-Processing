import heapq
from collections import defaultdict
import socket
import json


def huffman_encoding(data):
    freq = defaultdict(int)
    for char in data:
        freq[char] += 1

    heap = [[weight, [symbol, ""]] for symbol, weight in freq.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        for pair in left[1:]:
            pair[1] = '0' + pair[1]
        for pair in right[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [left[0] + right[0]] + left[1:] + right[1:])

    huffman_dict = dict(sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p)))
    return huffman_dict

def send_huffman_encoded_message(encoded_message, host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(json.dumps(encoded_message).encode())


def huffman_decoding(encoded_message, huffman_dict):
    decoded_message = ""
    code = ""
    print(code)
    for bit in encoded_message[1:]:
        code += bit
        for char, value in huffman_dict.items():
            if value == code:
                decoded_message += char
                code = ""
                break
    return decoded_message


def receive_huffman_encoded_message(port, huffman_dict):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Połączenie nawiązane przez', addr)
            data = conn.recv(1024)
            if data:
                encoded_message = json.loads(data.decode())
                decoded_message = huffman_decoding(encoded_message, huffman_dict)
                print("Odebrana wiadomość:", decoded_message)

print("1.Wyslij")
print("2.Odbieraj")
x = input("Wybor:")
if x == '1':
    text = "Wszystko działa elo beng beng!"
    # kodowanie Huffmana
    huffman_dict = huffman_encoding(text)
    print(huffman_dict)
    encoded_message = "".join(huffman_dict[char] for char in text)
    # wysłanie zakodowanej wiadomości
    host = "127.0.0.1"
    port = 4000
    send_huffman_encoded_message(json.dumps(encoded_message), host, port)
    print("wyslano pomyslnie:", encoded_message)
if x == '2':
    # adres i port do nasłuchiwania
    port = 4000

    huffman_dict = {' ': '010', 'e': '000', 'a': '0110', 'b': '0111', 'g': '1001', 'n': '1011', 'o': '1100', 's': '1101', 'z': '1111', 'ł': '0010', '!': '00110', 'W': '00111', 'd': '10000', 'i': '10001', 'k': '10100', 'l': '10101', 't': '11100', 'y': '11101'}

    # nasłuchiwanie i odbieranie zakodowanej wiadomości
    receive_huffman_encoded_message(port, huffman_dict)