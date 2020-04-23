#!/usr/bin/python

import os
import signal
import time

children = []


def main():
    parent_pid = os.getpid()
    child_1 = os.fork()

    if os.getpid() == parent_pid:
        child_2 = os.fork()

    if os.getpid() == parent_pid:
        def handler_parent(signum, frame):
            if signum == signal.SIGINT:
                os.kill(-os.getpid(), signal.SIGTERM)
            if signum == signal.SIGUSR1:
                os.kill(child_2, signal.SIGUSR1)

        signal.signal(signal.SIGINT, handler_parent)
        signal.signal(signal.SIGUSR1, handler_parent)
        while True:
            os.waitpid(child_1, 0)
            os.kill(-os.getpid(), signal.SIGTERM)

    if child_1 != 0 and child_2 == 0:
        def handler_son2(signum, frame):
            print("Soy el hijo2 con PID = %d: pong" % os.getpid())
        signal.signal(signal.SIGUSR1, handler_son2)
        while True:
            signal.pause()

    if child_1 == 0:
        time.sleep(1)
        for i in range(10):
            os.kill(os.getppid(), signal.SIGUSR1)
            print("Soy el hijo1 con PID = %d: ping" % os.getpid())
            time.sleep(5) if i < 9 else time.sleep(1)


if __name__ == '__main__':
    main()
