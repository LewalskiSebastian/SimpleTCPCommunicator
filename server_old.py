#Aplikacja serwera + klient
import threading

import socket
import sys
def serwerowanie():
    is_open = True
    while is_open:
        connection, client_address = sock.accept()
        try:
            print('Polaczenie od', client_address)
        finally:
            is_open = False
            connection.close()

def nadawanie():
    wejscie = 'nic'
    while wejscie != '\q':
        wejscie = input()
        if wejscie == '\q':
            sock.sendall('quit'.encode(encoding='U16'))
            print('Zamykanie połączenia')
            connection.close()
            sys.exit()
        message = wejscie.encode(encoding='U16')
        try:
            print('Wysyłanie {!r}'.format(message.decode(encoding='U16')))
            connection.sendall(message)
        finally:
            print('Wysłano')

def odbieranie():
    amount_received = 0
    amount_expected = 1024
    while amount_received < amount_expected:
        data = connection.recv(1024)
        data.decode(encoding='U16')
        amount_received += len(data)
        print('Otrzymano {!r}: '.format(data.decode(encoding='U16')))
        if data.decode(encoding='U16') == 'quit':
            print('witam')
            connection.close()
            sock.close()
            sys.exit()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
print('Łączenie do {} port {}'.format(*server_address))
sock.bind(server_address)
sock.listen(2)
print('Czekanie na połączenie')
connection, client_address = sock.accept()
print('Aby zakończyć wpisz "\q", aby wysłać wiadomość napisz ją i wciśnij "Enter"')

threads = []

t = threading.Thread(target=serwerowanie)
threads.append(t)
t.start()

t = threading.Thread(target=nadawanie)
threads.append(t)
t.start()

t = threading.Thread(target=odbieranie)
threads.append(t)
t.start()
