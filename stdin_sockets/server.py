#!/usr/bin/python

import getopt
import socket
import sys


def read_options():
    port = protocol = file_path = None

    (opt, arg) = getopt.getopt(sys.argv[1:], 'p:t:f:')

    if len(opt) != 3:
        print("Error: Expected 3 options [-p] [-t] [-f],", len(opt), "received")
        sys.exit(0)

    for (option, argument) in opt:
        if option == '-p':
            port = int(argument)
        elif option == '-t':
            protocol = argument
        elif option == '-f':
            file_path = argument

    assert port is not None and file_path is not None
    assert protocol.upper() in ['TCP', 'UDP']

    return port, protocol, file_path


def main():
    port, protocol, file_path = read_options()
    data = ''

    if protocol.upper() == 'TCP':
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('', port))
        server_socket.listen(5)
        client_socket = server_socket.accept()
        data, client_address = client_socket[0].recv(2048), client_socket[1]

        client_socket[0].close()

    elif protocol.upper() == 'UDP':
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind(('', port))
        data, client_address = server_socket.recvfrom(2048)

        server_socket.close()

    with open(file_path, 'w') as file:
        file.write(data.decode())
        print('\nData received from', client_address, 'saved on', file_path)


if __name__ == '__main__':
    try:
        main()
    except ValueError:
        print('Port must be an Integer (e.g 8080)')
    except AssertionError:
        print('Error with the arguments. \nExpecting -p (port) -t (udp/tcp) -f (file_path.txt)')
