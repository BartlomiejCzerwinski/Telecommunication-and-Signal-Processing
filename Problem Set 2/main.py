import heapq
from collections import defaultdict
import socket
import json

def send_huffman_dict(huffman_dict, host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        json_dict = json.dumps(huffman_dict)
        s.sendall(json_dict.encode())
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
        s.bind(('192.168.77.11', port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Połączenie nawiązane przez', addr)
            data = conn.recv(1024)
            if data:
                encoded_message = json.loads(data.decode())
                decoded_message = huffman_decoding(encoded_message, huffman_dict)
                return decoded_message

def receive_huffman_dict(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('192.168.77.11', port))
        s.listen()
        print("1")
        conn, addr = s.accept()
        with conn:
            print("2")
            print('Connected by', addr)
            data = conn.recv(1024)
            if data:
                print("3")
                json_dict = data.decode()
                huffman_dict = json.loads(json_dict)
                return huffman_dict

print("1.Wyslij")
print("2.Odbieraj")
x = input("Wybor:")
if x == '1':
    text = "Wszystko działa elo beng beng!"
    # kodowanie Huffmana
    huffman_dict = huffman_encoding(text)
    encoded_message = "".join(huffman_dict[char] for char in text)
    # wysłanie zakodowanej wiadomości
    host = "192.168.77.11"
    port = 16500
    send_huffman_encoded_message(json.dumps(encoded_message), host, port)
    send_huffman_dict(huffman_dict, host, port)
    print("wyslano pomyslnie:", encoded_message)
    print("huffman_dict:", huffman_dict)
if x == '2':
    # adres i port do nasłuchiwania
    port = 16500

    huffman_dict = receive_huffman_dict(port)
    print("huffman_dict:", huffman_dict)
    # nasłuchiwanie i odbieranie zakodowanej wiadomości
    decoded_message = receive_huffman_encoded_message(port, huffman_dict)
    print(decoded_message)