#!/usr/bin/python

import socket
import sys


def stablish_connection():
    alice_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    alice_socket.bind(('', 8080))
    local_address = socket.gethostbyname(socket.getfqdn())

    print('Alice listening at', local_address, 'on port 8080')
    print('Waiting for Bob...')

    alice_socket.listen(1)
    bob_socket, bob_address = alice_socket.accept()

    print('Bob connected from', bob_address)
    return alice_socket, bob_socket


def listen(bob_socket):
    while True:
        bob_message = bob_socket.recv(1024).decode()
        if bob_message == 'cambio':
            break
        elif bob_message == 'exit':
            print('\nBob disconnected')
            sys.exit(0)
        print('Bob:', bob_message)


def talk(bob_socket):
    while True:
        alice_message = input('> ').encode()
        bob_socket.send(alice_message)
        if alice_message.decode() == 'cambio':
            break
        elif alice_message.decode() == 'exit':
            sys.exit(0)


def main():
    alice_socket, bob_socket = stablish_connection()

    while True:
        print("~" * 35)
        listen(bob_socket)
        print("~" * 35)
        talk(bob_socket)


if __name__ == '__main__':
    main()
