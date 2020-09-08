#!/usr/bin/python

import socket
import sys
import threading
import subprocess as sp
from datetime import datetime


def listen(bob_socket, bob_n):
    while True:
        bob_message = bob_socket.recv(1024).decode()
        if bob_message == 'cambio':
            break
        elif bob_message == 'exit':
            print('\nBob disconnected')
            sys.exit(0)
        print(f'Bob {bob_n}:', bob_message)


def talk(bob_socket, bob_n):
    while True:
        alice_message = input(f'to Bob {bob_n} > ').encode()
        bob_socket.send(alice_message)
        if alice_message.decode() == 'cambio':
            break
        elif alice_message.decode() == 'exit':
            sys.exit(0)


def attend_bob(bob_socket, bob_n, lock):
    with open('../etc_23/alice_log.txt', 'a') as logfile:
        with sp.Popen(['ps -eLf | grep alice.py | grep -v grep'], shell=True, universal_newlines=True, stdout=sp.PIPE) as p:
            proccess_stdout = p.communicate()[0]
            date_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            lock.acquire()
            logfile.write(f'[{date_time}] Attending one Bob with thread {threading.current_thread().name}\n')
            logfile.write('ps -eLf output shown below:\n')
            logfile.write(proccess_stdout + '\n\n')
            lock.release()

    while True:
        print("~" * 35)
        listen(bob_socket, bob_n)
        print("~" * 35)
        talk(bob_socket, bob_n)


def main():

    alice_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    alice_socket.bind(('', 8080))
    local_address = socket.gethostbyname(socket.getfqdn())
    lock = threading.Lock()

    print('Alice listening at', local_address, 'on port 8080')
    print('Waiting for Bobs...')
    alice_socket.listen(16)

    bob_n = 1
    while True:
        bob_socket, bob_address = alice_socket.accept()
        print('A Bob connected from', bob_address)
        th = threading.Thread(target=attend_bob, args=(bob_socket, bob_n, lock))
        th.start()
        print(f'Launched thread with name {th.name} to attend Bob {bob_n}')
        bob_n += 1


if __name__ == '__main__':
    main()
