#!/usr/bin/python

import os
import signal
import time


def handler(s, frame):
    if s == signal.SIGUSR1:
        print("Child proccess here, signal", s, "received")
    if s == 2:
        print("Parent received SIGINT, finishing now...")
        os.kill(-os.getpid(), signal.SIGTERM)


def parent(child_pid):
    for i in range(10):
        os.kill(child_pid, signal.SIGUSR1)
        time.sleep(5)
    os.kill(child_pid, signal.SIGTERM)


def main():
    child_pid = os.fork()

    signal.signal(signal.SIGUSR1, handler) if child_pid == 0 else signal.signal(signal.SIGINT, handler)

    if child_pid == 0:
        while True:
            signal.pause()
    else:
        parent(child_pid)


if __name__ == '__main__':
    main()
