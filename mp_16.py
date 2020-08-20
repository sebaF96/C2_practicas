#!/usr/bin/python

import multiprocessing
import time
import os


def action(n, queue):
    print('Proceso %d, PID: %d' % (n, os.getpid()))
    time.sleep(n)
    queue.put(str(os.getpid()) + "\t")


def main():
    queue = multiprocessing.Queue()
    processes_list = []

    for i in range(1, 11, 1):   # [1, 10]
        process = multiprocessing.Process(target=action, args=(i, queue))
        process.start()
        processes_list.append(process)

    for process in processes_list:
        process.join()

    print()
    while not queue.empty():
        print(queue.get(), end='')

    print('\n')


if __name__ == '__main__':
    main()
