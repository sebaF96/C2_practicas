#!/usr/bin/python

import multiprocessing
import sys
import os
import signal


def read_stdin(pipe_extreme, fd):
    sys.stdin = os.fdopen(fd)    # We open the original stdin in this process
    print("Reading from stdin, press CTRL-D when you're done")
    for line in sys.stdin:
        pipe_extreme.send(line)


def read_pipe(pipe_extreme):
    while True:
        msg = pipe_extreme.recv()
        print('Leyendo (pid: %d): %s' % (os.getpid(), msg))


def main():
    x, y = multiprocessing.Pipe()

    stdin_fd = sys.stdin.fileno()    # Get the father stdin's file descriptor.

    p1 = multiprocessing.Process(target=read_stdin, args=(x, stdin_fd))
    p2 = multiprocessing.Process(target=read_pipe, args=(y, ))
    p1.start()
    p2.start()

    p1.join()
    os.kill(p2.pid, signal.SIGTERM)    # When process 1 is done, father kills process 2.


if __name__ == '__main__':
    main()
