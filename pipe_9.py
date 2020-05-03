#!/usr/bin/python

import os
import time
import signal


def handler(s, frame):
    pass


def main():
    process_a = os.getpid()
    r, w = os.pipe()
    signal.signal(signal.SIGUSR1, handler)

    process_b = os.fork()
    if not process_b:
        process_c = os.fork()

    # Process A
    if os.getpid() == process_a:
        time.sleep(0.1)
        os.close(w)
        pipe_r = os.fdopen(r)
        os.kill(process_b, signal.SIGUSR1)
        signal.pause()
        print("A (PID = %d) leyendo:" % os.getpid())
        print(pipe_r.read())

    # Process B
    elif not process_b and process_c:
        signal.pause()
        os.close(r)
        pipe_w = os.fdopen(w, 'w')
        pipe_w.write("Mensaje 1 (PID = %d)\n" % os.getpid())
        os.kill(process_c, signal.SIGUSR1)

    # Process C
    elif not process_c:
        signal.pause()
        os.close(r)
        pipe_w = os.fdopen(w, 'w')
        pipe_w.write("Mensaje 2 (PID = %d)" % os.getpid())
        os.kill(process_a, signal.SIGUSR1)


if __name__ == '__main__':
    main()
