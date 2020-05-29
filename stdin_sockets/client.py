#!/usr/bin/python

import getopt
import socket
import sys



def read_options():
    address = port = protocol = None

    (opt, arg) = getopt.getopt(sys.argv[1:], 'a:p:t:')

    if len(opt) != 3:
        print("Error: Expected 3 options [-a] [-p] [-t],", len(opt), "received")
        sys.exit(0)

    for (option, argument) in opt:
        if option == '-p':
            port = int(argument)
        elif option == '-t':
            protocol = argument
        elif option == '-a':
            address = argument

    assert port is not None and address is not None
    assert protocol.upper() in ['TCP', 'UDP']

    return address, port, protocol


def read_stdin():
    data = ''
    for line in sys.stdin:
        data += line

    return data


def main():
    address, port, protocol = read_options()

    if protocol.upper() == 'TCP':
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((address, port))
        print('Connected to', address, 'on port', port)
        print("Start typing and press CTRL-D when you're done")
        data = read_stdin()

        s.send(data.encode('ascii'))


    elif protocol.upper() == 'UDP':
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("Start typing and press CTRL-D when you're done")
        data = read_stdin()

        s.sendto(data.encode('ascii'), (address, port))

    print('\nData sent to', address)


if __name__ == '__main__':
    try:
        main()
    except ValueError:
        print('Port must be an Integer (e.g 8000)')
    except AssertionError:
        print('Error with the arguments. \nExpecting -a (address) -t (udp/tcp) -p (port)')
    except socket.error:
        print('Failed to create a socket')
