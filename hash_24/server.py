#!/usr/bin/python

import socket
import multiprocessing
import threading
import getopt
import sys
import hashlib


HASH_ALGORITHMS = {"sha1sum": hashlib.sha1(), "sha224sum": hashlib.sha224(), "sha256sum": hashlib.sha256(),
                   "sha384sum": hashlib.sha384(), "sha512sum": hashlib.sha512(), "sha3-224sum": hashlib.sha3_224,
                   "sha3-256sum": hashlib.sha3_256, "sha3-384sum": hashlib.sha3_384, "sha3-512sum": hashlib.sha3_512}


def read_port():
    (opt, arg) = getopt.getopt(sys.argv[1:], 'p:')
    if len(opt) != 1:
        raise getopt.GetoptError("Expected one option [-p] with its argument (port number)")

    port = int(opt[0][1])
    if port < 1:
        raise ValueError
    return port


def attend_client(client_socket):
    client_string = client_socket.recv(1024).decode().strip()
    hash_algorithm = client_socket.recv(64).decode().strip()
    if hash_algorithm not in HASH_ALGORITHMS:
        client_socket.send('Hash algorithm not recognized'.encode())
        return

    _hash = HASH_ALGORITHMS[hash_algorithm]
    _hash.update(client_string.encode())
    client_socket.send(_hash.hexdigest().encode())


def main():
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

        new_process = multiprocessing.Process(target=attend_client, args=(client_socket, ))
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
