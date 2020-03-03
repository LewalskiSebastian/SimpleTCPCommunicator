#Aplikacja klienta
import threading

import socket
import sys
from socket import SHUT_RDWR
import os

import time


def nadawanie_pliku():
    CHUNKSIZE = 1_000_000

    filename = input('Nazwa pliku do wysłania: ')

    sock2 = socket.socket()
    sock2.connect(('localhost', 5000))
    with sock2, open(filename, 'rb') as f:
        sock2.sendall(filename.encode() + b'\n')
        sock2.sendall(f'{os.path.getsize(filename)}'.encode() + b'\n')

        # Send the file in chunks so large files can be handled.
        while True:
            data = f.read(CHUNKSIZE)
            if not data: break
            sock2.sendall(data)


def nadawanie():
    wejscie = 'nic'
    while wejscie != '\q':
        wejscie = input()
        if wejscie == '\q':
            sock.sendall('quit'.encode(encoding='U16'))
            try:
                sock.shutdown(SHUT_RDWR)
                sock.close()
                time.sleep(1)
                sys.exit()
                print('Zamykanie połączenia')
            except Exception:
                pass
            break
        elif wejscie == 'plik':
            message = wejscie.encode(encoding='U16')
            sock.sendall(message)
            nadawanie_pliku()
        else:
            message = wejscie.encode(encoding='U16')
            try:
                print('Wysyłanie {!r}'.format(message.decode(encoding='U16')))
                sock.sendall(message)
            finally:
                print('Wysłano')


def odbieranie():
    amount_received = 0
    amount_expected = 1024
    while amount_received < amount_expected:
        data = sock.recv(1024)
        amount_received += len(data)
        print('Otrzymano {!r}: '.format(data.decode(encoding='U16')))
        if data.decode(encoding='U16') == 'quit':
            try:
                sock.shutdown(SHUT_RDWR)
                sock.close()
                time.sleep(1)
                sys.exit()
                print("Zatrzymywanie odbierania")
            except Exception:
                pass
            break
        elif data.decode(encoding='U16') == 'plik':
            server()


def server():
    CHUNKSIZE = 1_000_000

    os.makedirs('Pobrane', exist_ok=True)

    sock2 = socket.socket()
    sock2.bind(('', 5000))
    sock2.listen(1)

    with sock2:
        while True:
            client, addr = sock2.accept()

            with client, client.makefile('rb') as clientfile:
                filename = clientfile.readline().strip().decode()
                length = int(clientfile.readline())
                print(f'Pobieranie {filename}, rozmiar:{length}...')
                path = os.path.join('Pobrane', filename)

                with open(path, 'wb') as f:
                    while length:
                        chunk = min(length, CHUNKSIZE)
                        data = clientfile.read(chunk)
                        if not data: break
                        f.write(data)
                        length -= len(data)
                if length != 0:
                    print('Błąd przy pobieraniu.')
                else:
                    print('Ukończono pobieranie.')
                    #startfile(path)
                    break


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
print('Łączenie do {} port {}'.format(*server_address))
sock.connect(server_address)
print('Łączenie zakończone powodzeniem')
print('Aby zakończyć wpisz "\q", aby wysłać plik napisz "plik", aby wysłać wiadomość napisz ją i wciśnij "Enter".')

threads = []

t = threading.Thread(target=nadawanie)
threads.append(t)
t.start()

t = threading.Thread(target=odbieranie)
threads.append(t)
t.start()
