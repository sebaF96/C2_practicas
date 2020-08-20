#!/usr/bin/python

import getopt
import socket
import sys


def read_options():
    address = port = logfile_path = None

    (opt, arg) = getopt.getopt(sys.argv[1:], 'a:p:l:')

    if len(opt) < 2:
        print("Error: Expected at least 2 options [-a] [-p]", len(opt), "received")
        sys.exit(0)

    for (option, argument) in opt:
        if option == '-p':
            port = int(argument)
        elif option == '-a':
            address = argument
        elif option == '-l':
            logfile_path = argument

    assert port is not None and address is not None

    return address, port, logfile_path


def write_log(command, logfile_path):
    from datetime import datetime
    datetime = datetime.now().strftime("%d/%m/%Y %H:%M")
    with open(logfile_path, 'a') as file:
        file.write('[' + datetime + '] - ' + command + '\n')


def main():

    address, port, logfile_path = read_options()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((address, port))
    print('Connected to remote shell at', address, 'on port', port)
    print("Enter command 'exit' to leave the program")
    command = ''

    while command != 'exit':
        command = str(input('> '))
        s.send(command.encode())
        answer = s.recv(4096).decode()
        print(answer)
        write_log(command, logfile_path) if logfile_path else None


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
