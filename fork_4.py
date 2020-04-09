#!/usr/bin/python

import os


def main():
    pid = os.fork()
    if pid == 0:
        for i in range(5):
            print("Soy el hijo, PID", os.getpid())
        print("PID", os.getpid(), "terminado")
    else:
        for i in range(2):
            print("Soy el padre, PID", os.getpid(), ", mi hijo es", pid)
        os.wait()
        print("Mi proceso hijo", pid, "terminó")


if __name__ == '__main__':
    main()
