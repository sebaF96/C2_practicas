#!/usr/bin/python

import multiprocessing
import sys
import getopt
import socket
import signal


def read_port():
    (opt, arg) = getopt.getopt(sys.argv[1:], 'p:')
    if len(opt) != 1:
        raise getopt.GetoptError("Expected one option [-p] with its argument (port number)")

    port = int(opt[0][1])
    if port < 1:
        raise ValueError
    return port


def reverse_string(string: str) -> str:
    return string[::-1]


def attend_client(client_socket, address):
    while True:
        message = client_socket.recv(2048).decode()

        if message == 'exit':
            client_socket.send('--> Bye!'.encode())
            break

        client_socket.send(('--> ' + reverse_string(message)).encode())

    print('Client', address, 'disconnected')
    client_socket.close()


def close_server(s, frame):
    print('\nClosing connections and server...')
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, close_server)
    port = read_port()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    print('Server started at', socket.gethostbyname(socket.getfqdn()), 'on port', port)
    print('Waiting for connections...')

    while True:
        server_socket.listen(16)
        client_socket, address = server_socket.accept()
        print('\nGot a connection from', address)

        new_process = multiprocessing.Process(target=attend_client, args=(client_socket, address))
        new_process.start()


if __name__ == '__main__':
    try:
        main()
    except getopt.GetoptError as e:
        print(e)
    except ValueError:
        print('Port must be a positive Integer')
    except Exception as e:
        print(e)
