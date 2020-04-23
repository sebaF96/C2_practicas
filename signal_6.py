#!/usr/bin/python

import os
import signal
import time


def handler(signum, frame):
    if signum == signal.SIGUSR1:
        print("Child process here, signal", signum, "received")
    if signum == signal.SIGINT:
        print("Parent received SIGINT, killing child and finishing now...")
        os.kill(-os.getpid(), signal.SIGTERM)
        # I'm using the NEGATIVE father's pid to send the same signal to the children process.
        # This way, the parent will "kill -TERM" his child and himself.


def parent(child_pid):
    for i in range(10):
        os.kill(child_pid, signal.SIGUSR1)
        time.sleep(5) if i < 9 else time.sleep(1)
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
