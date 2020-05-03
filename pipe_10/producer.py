#!/usr/bin/python

import sys
import os

FIFO_PATH = "/tmp/fifo_10"


def main():
    message = sys.argv[1]

    if not os.path.exists(FIFO_PATH):
        os.mkfifo(FIFO_PATH)

    fifo_w = open(FIFO_PATH, 'w')
    fifo_w.write(message)
    fifo_w.flush()


if __name__ == '__main__':
    try:
        main()
    except IndexError:
        print("Please, enter a command-line message")
