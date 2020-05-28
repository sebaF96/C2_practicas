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
        clientsocket = server_socket.accept()[0]
        data = clientsocket.recv(2048)

        clientsocket.close()

    elif protocol.upper() == 'UDP':
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind(('', port))
        data = server_socket.recvfrom(2048)[0]

        server_socket.close()

    with open(file_path, 'w') as file:
        file.write(data)


if __name__ == '__main__':
    try:
        main()
    except ValueError:
        print('Port must be an Integer (e.g 8000)')
    except AssertionError:
        print('Error with the arguments. \nExpecting -p (port) -t (udp/tcp) -f (file_path.txt)')
