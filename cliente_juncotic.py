#!/usr/bin/python

import socket
import sys
import getopt

RESPONSE_CODES = {200: 'OK', 400: 'The command seems valid but out of place', 404: 'Wrong Key', 405: 'Null String',
                  500: 'Invalid command'}


def communicate(connection, message):
    connection.send(message.encode())
    response_code = int(connection.recv(1024).decode())
    print("Response from server:", response_code, '-', RESPONSE_CODES.get(response_code), '\n')

    return int(response_code)


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

    assert host is not None and port is not None

    s.connect((host, port))

    name_check = email_check = key_check = False

    while not name_check:
        name = 'hello|' + input('Enter your name: ').replace(' ', '_')
        name_check = int(communicate(s, name)) == 200

    while not email_check:
        email = 'email|' + input('Enter your email: ')
        email_check = int(communicate(s, email)) == 200

    while not key_check:
        key = 'key|' + input('Enter the key: ')
        key_check = int(communicate(s, key)) == 200

    print("Closing connection")
    communicate(s, "exit")


if __name__ == '__main__':
    try:
        main()
    except AssertionError or getopt.GetoptError:
        print("You must enter the port and host value using [-h] or [--host] and [-p] or [--port]")
