#Aplikacja klienta
import threading

import socket
import sys
from socket import SHUT_RDWR

import time

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

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
print('Łączenie do {} port {}'.format(*server_address))
sock.connect(server_address)
print('Łączenie zakończone powodzeniem')
print('Aby zakończyć wpisz "exit", aby wysłać wiadomość napisz ją i wciśnij "Enter"')

threads = []

t = threading.Thread(target=nadawanie)
threads.append(t)
t.start()

t = threading.Thread(target=odbieranie)
threads.append(t)
t.start()
