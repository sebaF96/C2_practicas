#!/usr/bin/python

import getopt
import sys
import time
import string
import os
from multiprocessing import Lock, Process



def read_options():
    (opt, arg) = getopt.getopt(sys.argv[1:], 'f:r:n:')

    if len(opt) != 3:
        raise getopt.GetoptError('Expected 3 options [-f] [-r] and [-n]. ' + str(len(opt)) + ' received.')

    file_path = iterations = n_processes = None


    for (option, argument) in opt:
        if option == '-f':
            file_path = argument
        if option == '-r':
            iterations = int(argument)
        if option == '-n':
            n_processes = int(argument)

    assert file_path is not None and iterations is not None and n_processes is not None

    return file_path, iterations, n_processes


def write_letters(iterations, letter, filepath, lock):
    lock.acquire()
    with open(filepath, 'a') as file:
        for i in range(iterations):
            file.write(letter)
            time.sleep(1)
    lock.release()


def main():
    file_path, iterations, n_processes = read_options()
    abecedary = string.ascii_uppercase
    lock = Lock()
    processes_list = []

    os.system('rm ' + file_path) if os.path.isfile(file_path) else os.system('touch ' + file_path)

    for i in range(n_processes):
        process = Process(target=write_letters, args=(iterations, abecedary[i], file_path, lock))
        process.start()
        processes_list.append(process)

    for p in processes_list:
        p.join()
    print('Done')


if __name__ == '__main__':
    try:
        main()
    except getopt.GetoptError as ge:
        print(ge)
    except AssertionError:
        print('Missing options. Expected [-f] [-r] and [-n]')
    except ValueError:
        print('[-f] and [-n] arguments must be positive integers.')
