#!/usr/bin/python

import os
import signal
import sys
import getopt
import time


def read_option():
    (opt, arg) = getopt.getopt(sys.argv[1:], 'p:', ['process='])
    if len(opt) != 1:
        raise getopt.GetoptError("Expected one option with its argument")
    number_of_children = int(opt[0][1])
    if number_of_children < 1:
        raise ValueError

    return number_of_children


def send_signals(children):
    for pid in children:
        os.kill(pid, signal.SIGUSR2)
    os.wait()


def handler(signum, frame):
    print("Soy el PID", os.getpid(), "recibí la señal", signum, "de mi padre PID", os.getppid())


def main():
    number_of_children = read_option()
    father_id = os.getpid()
    children_pids = []

    for i in range(number_of_children):
        child = os.fork()
        if child == 0:
            signal.signal(signal.SIGUSR2, handler)
            signal.pause()
            break

        print("Creando proceso:", child)
        children_pids.append(child)

    if os.getpid() == father_id:
        time.sleep(0.1)
        send_signals(children_pids)


if __name__ == '__main__':
    try:
        main()
    except getopt.GetoptError as e:
        print("Error:", e)
    except ValueError:
        print("Argument must be a positive integer")
