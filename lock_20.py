#!/usr/bin/python

import socket
import multiprocessing
import getopt
import sys
import signal

SERVER_COMMANDS = ["ABRIR", "CERRAR", "AGREGAR", "LEER"]


def read_port():
    try:
        opt, arg = getopt.getopt(sys.argv[1:], 'p:')
        return int(opt[0][1])

    except getopt.GetoptError as ge:
        print("Error: ", ge)
    except IndexError:
        print("You must specify port number with option [-p]")
    except ValueError:
        print("Port -[p] must be a possitive integer")

    sys.exit(0)


def handler(s, f):
    print("Cosing server")
    sys.exit(0)


def attend_client(client_socket, lock, client_address):
    filename = None
    opened_file = None
    client_socket.send(('> Welcome, server commands are ' + str(SERVER_COMMANDS) + '\n').encode())

    while True:
        command = client_socket.recv(256).decode()
        command = command.upper().strip()

        if command == 'ABRIR':
            if opened_file is not None:
                client_socket.send('> File already open\n'.encode())
                continue

            client_socket.send('> Specify filename: '.encode())
            try:
                filename = client_socket.recv(256).decode()
                opened_file = open(filename, 'a')
                client_socket.send('> OK\n'.encode())
            except FileNotFoundError:
                client_socket.send('> Error: File not found\n'.encode())

        elif command == 'AGREGAR':
            if opened_file is None:
                client_socket.send('> You must open a file first\n'.encode())
                continue

            client_socket.send('> Send a string to append at the end of your file:\n'.encode())
            user_string = client_socket.recv(256).decode()

            lock.acquire()
            opened_file.writelines(user_string)
            opened_file.flush()
            lock.release()

            client_socket.send('> OK\n'.encode())

        elif command == 'LEER':
            if opened_file is None:
                client_socket.send('> You must open a file first\n'.encode())
                continue

            with open(filename, 'r') as read_fd:
                content = str(read_fd.read()) + '\n'
                client_socket.send(content.encode())

        elif command == 'CERRAR' or command == 'EXIT':
            client_socket.send('> Bye. Closing connection\n'.encode())
            if opened_file is not None:
                opened_file.close()
            break
        else:
            client_socket.send(('> Invalid command. Try with ' + str(SERVER_COMMANDS) + '\n').encode())

    print('Client', client_address, 'disconnected')
    client_socket.close()


def main():
    signal.signal(signal.SIGINT, handler)

    port = read_port()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    server_address = socket.gethostbyname(socket.getfqdn())
    print('Server started at', server_address, 'on port', port)

    lock = multiprocessing.Lock()
    while True:
        server_socket.listen(32)
        client_socket, connection = server_socket.accept()
        print("Client", connection[0], "connected")
        new_process = multiprocessing.Process(target=attend_client, args=(client_socket, lock, connection[0]))
        new_process.start()




if __name__ == '__main__':
    main()
