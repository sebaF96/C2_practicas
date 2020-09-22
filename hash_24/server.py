#!/usr/bin/python

import socket
import getopt
import sys
import hashlib

HASH_ALGORITHMS = {"sha1": hashlib.sha1(), "sha224": hashlib.sha224(), "sha256": hashlib.sha256(),
                   "sha384": hashlib.sha384(), "sha512": hashlib.sha512(), "sha3-224": hashlib.sha3_224(),
                   "sha3-256": hashlib.sha3_256(), "sha3-384": hashlib.sha3_384(), "sha3-512": hashlib.sha3_512()}


def read_options():
    port, use_threads = None, None

    (opt, arg) = getopt.getopt(sys.argv[1:], 'mtp:')
    if len(opt) != 2:
        raise getopt.GetoptError("Expected two options: [-p] with its argument (port number) and -m or -t")

    for (option, argument) in opt:
        if option == '-p':
            port = int(argument)
        elif option == '-t':
            use_threads = True
        elif option == '-m':
            use_threads = False

    assert port is not None and use_threads is not None

    if port < 1:
        raise ValueError

    return port, use_threads


def attend_client(client_socket):
    hash_algorithm = client_socket.recv(64).decode()

    if hash_algorithm not in HASH_ALGORITHMS:
        client_socket.send('404'.encode())
        return

    client_socket.send('200'.encode())
    client_string = client_socket.recv(1024).decode()
    _hash = HASH_ALGORITHMS[hash_algorithm]
    _hash.update(client_string.encode())
    client_socket.send(_hash.hexdigest().encode())


def main():
    local_address = socket.gethostbyname(socket.getfqdn())
    port, use_threads = read_options()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    print(f"Server started at {local_address} on port {port}. Working with {'Threads' if use_threads else 'Processes'}")
    print('Waiting for connections...')

    if use_threads:
        from threading import Thread as Worker
    else:
        from multiprocessing import Process as Worker

    while True:
        server_socket.listen(16)
        client_socket, address = server_socket.accept()
        print(f'Got a connection from {address}')

        new_worker = Worker(target=attend_client, args=(client_socket,))
        new_worker.start()


if __name__ == '__main__':
    try:
        main()
    except getopt.GetoptError or AssertionError as e:
        print(e)
    except ValueError:
        print('Port must be a positive Integer')
    except Exception as e:
        print(e)
