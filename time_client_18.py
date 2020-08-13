#!/usr/bin/python

import socket
import getopt
import sys


def read_options():
    (opt, arg) = getopt.getopt(sys.argv[1:], 'p:h:t:')
    # Default values for port and protocol
    port = 37
    protocol = 'TCP'
    host = None

    for (option, argument) in opt:
        if option == '-p':
            port = int(argument)
        elif option == '-h':
            host = argument
        elif option == '-t':
            protocol = argument.upper() if argument.upper() in ['TCP', 'UDP'] else 'TCP'

    assert host is not None
    return port, host, protocol


def format_output(datetime: str) -> str:
    stdout = 'Fecha y hora actual (UTC): '
    date, time = datetime.split(' ')[1], datetime.split(' ')[2]
    stdout += date + ' ' + time

    return stdout



def main():
    port, host, protocol = read_options()

    if protocol == 'TCP':
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((host, port))
            print('Connection stablished')
            datetime = s.recv(1024).decode()
            print(format_output(datetime))
        except socket.error as se:
            print(se)

    elif protocol == 'UDP':
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(''.encode(), (host, port))
            datetime = s.recvfrom(1024)[0].decode()
            print(format_output(datetime))
        except socket.error as se:
            print(se)


if __name__ == '__main__':
    try:
        main()
    except getopt.GetoptError as e:
        print("GetoptError:", e)
    except AssertionError:
        print("You must specify a valid host using the [-h] option")
