#!/usr/bin/python

import getopt
import sys
import time
import string
import os
import threading
import subprocess as sp
from datetime import datetime


def log_activity(threads_number):
    date_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open('etc_23/lock_19_log.txt', 'w') as logfile:
        logfile.write(f'File lock_19.py ran at {date_time} and generated {threads_number} threads including main\n')
        logfile.write('ps -eLf output shown below:\n\n')

        with sp.Popen(['ps -eLf | grep lock_19 | grep -v grep'], shell=True, universal_newlines=True, stdout=sp.PIPE) as proccess:
            proccess_stdout = proccess.communicate()[0]
            logfile.write(proccess_stdout)


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
            file.flush()
            time.sleep(1)
    lock.release()


def main():
    file_path, iterations, n_processes = read_options()
    abecedary = string.ascii_uppercase
    lock = threading.Lock()

    os.system('rm ' + file_path) if os.path.isfile(file_path) else os.system('touch ' + file_path)

    for i in range(n_processes):
        th = threading.Thread(target=write_letters, args=(iterations, abecedary[i], file_path, lock))
        th.start()

    log_activity(len(threading.enumerate()))

    for th in threading.enumerate():
        # An exception will raise if we try to join the main thread, so we exclude it.
        if th == threading.main_thread():
            continue
        th.join()
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
