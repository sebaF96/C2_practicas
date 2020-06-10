#!/usr/bin/python

import getopt
import socket
import subprocess as sp
import sys
import multiprocessing
import signal


def close_server(s, frame):
    print('\nClosing connections and server...')
    sys.exit(0)


def read_port():
    (opt, arg) = getopt.getopt(sys.argv[1:], 'p:')
    if len(opt) != 1:
        raise getopt.GetoptError("Expected one option [-p] with its argument (port number)")

    port = int(opt[0][1])
    if port < 1:
        raise ValueError
    return port


def attend_client(client_socket, address):
    while True:
        command = client_socket.recv(2048)

        if command.decode('ascii') == 'exit':
            client_socket.send('Bye!'.encode('ascii'))
            break

        with sp.Popen([command], shell=True, universal_newlines=True, stdout=sp.PIPE, stderr=sp.PIPE) as process:
            process_stdout, process_stderr = process.communicate()

            if process.returncode is 0 and process_stdout:
                client_socket.send(process_stdout.encode('ascii'))

            elif process.returncode is 0 and not process_stdout:
                client_socket.send('Ok'.encode('ascii'))

            else:
                client_socket.send(process_stderr.encode('ascii'))

    print('Client', address, 'disconnected')
    client_socket.close()


def main():
    signal.signal(signal.SIGINT, close_server)

    local_address = socket.gethostbyname(socket.getfqdn())
    port = read_port()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    print('Server started at', local_address, 'on port', port)
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