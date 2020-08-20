#!/usr/bin/python

import getopt
import socket
import sys


def read_options():
    host = port = None
    (opt, arg) = getopt.getopt(sys.argv[1:], 'h:p:')

    if len(opt) < 2:
        print("Error: Expected at least 2 options [-h] [-p]", len(opt), "received")
        sys.exit(0)

    for (option, argument) in opt:
        if option == '-p':
            port = int(argument)
        elif option == '-h':
            host = argument

    assert host is not None and port is not None
    return host, port


def main():
    address, port = read_options()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((address, port))
    print('Connected')
    print("Enter command 'exit' to leave the program")
    message = ''

    while message != 'exit':
        message = str(input('>>> '))
        s.send(message.encode())
        answer = s.recv(4096).decode()
        print(answer)


if __name__ == '__main__':
    try:
        main()
    except getopt.GetoptError as e:
        print(e)
    except AssertionError:
        print('Expected options [-a] and [-p] specifying address and port respectively')
    except ConnectionRefusedError:
        print('Error: Connection refused')
    except socket.error:
        print('Failed to create a socket')
    except Exception as e:
        print(e)
