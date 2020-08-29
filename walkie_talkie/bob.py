#!/usr/bin/python

import socket
import sys
import getopt


def stablish_connection():
    try:
        opt, arg = getopt.getopt(sys.argv[1:], 'a:')
        alice_address = opt[0][1] if opt else ''
        bob_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        bob_socket.connect((alice_address, 8080))
        print('Connected with Alice')

        return bob_socket
    except socket.error:
        print('Something went wrong, couldn\'t connect with Alice')
        print('Please specify Alice\'s IP address under the option [-a]')
        sys.exit(1)


def listen(bob_socket):
    while True:
        alice_message = bob_socket.recv(1024).decode()
        if alice_message == 'cambio':
            break
        elif alice_message == 'exit':
            print('\nAlice disconnected')
            sys.exit(0)
        print('Alice:', alice_message)


def talk(bob_socket):
    while True:
        bob_message = input('> ').encode()
        bob_socket.send(bob_message)

        if bob_message.decode() == 'cambio':
            break
        elif bob_message.decode() == 'exit':
            sys.exit(0)


def main():
    bob_socket = stablish_connection()

    while True:
        print("=" * 35)
        talk(bob_socket)
        print("=" * 35)
        listen(bob_socket)


if __name__ == '__main__':
    main()
