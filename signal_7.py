#!/usr/bin/python

import os
import signal
import time


def parent(child1_pid, child2_pid):
    def handler(signum, frame):
        if signum == signal.SIGUSR1:
            os.kill(child2_pid, signal.SIGUSR1)
        elif signum == signal.SIGINT:
            os.kill(-os.getpid(), signal.SIGTERM)

    signal.signal(signal.SIGUSR1, handler)
    signal.signal(signal.SIGINT, handler)
    os.waitpid(child1_pid, 0)
    os.kill(child2_pid, signal.SIGTERM)


def ping():
    for i in range(10):
        print("Soy el hijo1 con PID = %d: ping" % os.getpid())
        os.kill(os.getppid(), signal.SIGUSR1)
        time.sleep(5) if i < 9 else time.sleep(0.1)


def pong():
    def handler(signum, frame):
        print("Soy el hijo2 con PID = %d: pong\n" % os.getpid())

    signal.signal(signal.SIGUSR1, handler)
    while True:
        signal.pause()


def main():
    parent_pid = os.getpid()
    child_1 = os.fork()

    # If parent, create child 2 and do parent stuff
    if os.getpid() == parent_pid:
        child_2 = os.fork()
        child_2 and parent(child_1, child_2)

    # If child 1, ping!
    if not child_1:
        time.sleep(0.1)
        ping()

    # If child 2, pong!
    if child_1 and not child_2:
        pong()


if __name__ == '__main__':
    main()
