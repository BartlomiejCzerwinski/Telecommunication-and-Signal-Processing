import heapq
from collections import defaultdict
import socket
import json
import tkinter as tk
from tkinter import messagebox


def send_huffman_dict(huffman_dict, host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        json_dict = json.dumps(huffman_dict)
        s.sendall(json_dict.encode())
def huffman_encoding(data):
    # zliczanie występowania każdego znaku w wiadomośći
    freq = defaultdict(int)
    for char in data:
        freq[char] += 1

    # tworzenie zbioru z każdym znakiem i jego częstością występowania
    heap = [[weight, [symbol, ""]] for symbol, weight in freq.items()]
    heapq.heapify(heap)

    # łączenie węzłów drzewa huffmana i tworzenie kodów dla znaków
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


def receive_huffman_encoded_message(address, port, huffman_dict):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((address, port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            data = conn.recv(1024)
            if data:
                encoded_message = json.loads(data.decode())
                decoded_message = huffman_decoding(encoded_message, huffman_dict)
                return decoded_message

def receive_huffman_dict(address, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((address, port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            data = conn.recv(1024)
            if data:
                json_dict = data.decode()
                huffman_dict = json.loads(json_dict)
                return huffman_dict

decoded_message = ''
def receiveMessageWindow():
    global decoded_message
    # adres i port do nasłuchiwania
    address = '10.77.14.30'
    port = 16500

    # odbieranie słownika huffmana
    huffman_dict = receive_huffman_dict(address, port)
    print("Odebrany słownik: ", huffman_dict)

    # odbieranie zakodowanej wiadomości
    decoded_message = receive_huffman_encoded_message(address, port, huffman_dict)
    print("Odebrana wiadomość: ", decoded_message)
    # utworzenie nowego okna
    new_window = tk.Toplevel(root)
    new_window.geometry("300x100")

    # naglowek tekstu
    text_box_label = tk.Label(new_window, text="Podaj nazwe pliku:", font=("Aerial", 8))
    text_box_label.pack(pady=5)

    #pole tekstowe
    text_box = tk.Entry(new_window, textvariable=text_var1, font=("Arial", 8))
    text_box.pack(pady=5)

    # przycisk w nowym oknie
    new_button = tk.Button(new_window, text="Zapisz odebrany plik", font=("Arial", 8) ,command=receiveMessage)
    new_button.pack(pady=5)


def sendMessageWindow():

    new_window = tk.Toplevel(root)
    new_window.geometry("300x100")

    text_box_label = tk.Label(new_window, text="Podaj nazwe pliku:", font=("Aerial", 8))
    text_box_label.pack(pady=5)

    text_box = tk.Entry(new_window, textvariable=text_var2, font=("Arial", 8))
    text_box.pack(pady=5)

    new_button = tk.Button(new_window, text="Wyślij plik", font=("Arial", 8), command=sendMessage)
    new_button.pack(pady=5)

root = tk.Tk()
root.configure(background='lightblue')
root.geometry("600x200")

text_var1 = tk.StringVar()
text_var2 = tk.StringVar()

send_button = tk.Button(root, text="Wysyłaj",font=("Arial", 8), command=sendMessageWindow, height=5, width=100)
send_button.pack(pady=10,padx=30)

receive_button = tk.Button(root, text="Odbieraj",font=("Arial", 8), command=receiveMessageWindow, height=5, width=100)
receive_button.pack(pady=10, padx=30)

def sendMessage():

    # odczytanie wiadomości z pliku
    filename = text_var2.get()
    try:
        with open(filename, "r") as file:
            text = file.read()
            file.close()
    except FileNotFoundError:
        messagebox.showinfo("Error", "Plik nie istnieje")

    # tworzenie słownika i kodowanie wiadomości
    huffman_dict = huffman_encoding(text)
    encoded_message = "".join(huffman_dict[char] for char in text)

    # wysłanie zakodowanej wiadomości
    host = "10.77.14.30"
    port = 16500
    send_huffman_dict(huffman_dict, host, port)
    send_huffman_encoded_message(json.dumps(encoded_message), host, port)
    messagebox.showinfo("Wysłano wiadomość", "Pomyślnie wysłano wiadomość.")


def receiveMessage():
    global decoded_message

    # zapisanie wiadomości na dysku
    filename = text_var1.get()
    try:
        with open(filename, "w") as file:
            file.write(decoded_message)
            file.close()
            print("Zapisano plik pod nazwą: ", filename)
    except FileNotFoundError:
        messagebox.showinfo("Error", "Nie podano nazwy")
    messagebox.showinfo("Odebrano wiadomość", "Pomyślnie odebrano wiadomość.")

root.mainloop()