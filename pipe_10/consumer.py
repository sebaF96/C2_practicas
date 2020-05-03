#!/usr/bin/python

import os
import signal


def handler(s, f):
    pass


def main():
    signal.signal(signal.SIGUSR1, handler)
    r, w = os.pipe()
    child_pid = os.fork()

    # Parent
    if child_pid != 0:
        fifo_r = open("/tmp/fifo_10")
        message = fifo_r.readline()

        pipe_w = os.fdopen(w, 'w')
        pipe_w.write(message)
        pipe_w.close()

        os.kill(child_pid, signal.SIGUSR1)
        os.wait()

    # Child
    else:
        signal.pause()
        os.close(w)
        pipe_r = os.fdopen(r)
        print(pipe_r.read())


if __name__ == '__main__':
    try:
        main()
    except FileNotFoundError:
        print("FIFO not found, you should talk with the producer first")
