#!/usr/bin/python

import socket


def main():

    address, port = '127.0.0.1', 8080

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((address, port))
    print('Connected to remote shell on', address, 'on port', port)
    print('Enter command exit to leave the program')
    command = ''

    while command != 'exit':
        command = str(input('> '))
        s.send(command.encode('ascii'))
        answer = s.recv(4096).decode('ascii')
        print(answer)


if __name__ == '__main__':
    main()
