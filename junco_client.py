#!/usr/bin/python

import socket
import sys
import getopt


def communicate(connection, message):
    connection.send(message.encode('ascii'))
    response = connection.recv(1024).decode("ascii")
    print("Response from server:", response)


def main():
    host = None
    port = None

    (opt, arg) = getopt.getopt(sys.argv[1:], 'h:p:', ["host=", "port="])

    for (option, argument) in opt:
        if option == '-h' or option == '--host':
            host = argument
        elif option == '-p' or option == '--port':
            port = int(argument)

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print('Failed to create socket')
        sys.exit()

    assert host is not None
    assert port is not None

    s.connect((host, port))

    name = 'hello|' + input('Enter your name: ').replace(' ', '_')
    communicate(s, name)

    email = 'email|' + input('Enter your email: ')
    communicate(s, email)

    key = 'key|' + input('Enter the key: ')
    communicate(s, key)

    print("Closing connection")
    communicate(s, "exit")


if __name__ == '__main__':
    try:
        main()
    except AssertionError or getopt.GetoptError:
        print("You must enter the port and host value using [-h] or [--host] and [-p] or [--port]")
