#!/usr/bin/python

import socket
import getopt
import sys
import time


def read_options():
    address = port = string = hash_algorithm = None

    (opt, arg) = getopt.getopt(sys.argv[1:], 'a:c:h:p:')

    if len(opt) != 4:
        print("Error: Expected 4 options [-a] [-p] [-c] and [-h]", len(opt), "received")
        sys.exit(0)

    for (option, argument) in opt:
        if option == '-p':
            port = int(argument)
        elif option == '-a':
            address = argument
        elif option == '-c':
            string = argument
        elif option == '-h':
            hash_algorithm = argument

    assert port is not None and address is not None and hash_algorithm is not None and string is not None

    return address, port, string, hash_algorithm


def main():
    address, port, _string, hash_algorithm = read_options()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((address, port))
    print('Connected to hash server', address, 'on port', port, "\n")

    s.send(hash_algorithm.encode())
    response_code = s.recv(1024)
    if int(response_code.decode()) == 404:
        print('Hash algorithm not recognized')
        sys.exit(0)

    s.send(_string.encode())
    hashed_digest = s.recv(1024).decode()
    print(f'Your string: {_string}\n')
    print(f'{hash_algorithm} value: {hashed_digest}')


if __name__ == '__main__':
    try:
        main()
    except getopt.GetoptError as e:
        print(e)
    except AssertionError:
        print('Expected options [-a] (address), [-p] (port), [-h] (hash algorithm) and [-c] (string)')
    except ConnectionRefusedError:
        print('Error: Connection refused')
    except socket.error:
        print('Failed to create a socket')
    except Exception as e:
        print(e)
