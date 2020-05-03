import os
import time
import signal


def handler(s, frame):
    pass


def main():
    parent_pid = os.getpid()
    r, w = os.pipe()
    signal.signal(signal.SIGUSR1, handler)

    process_b = os.fork()
    if not process_b:
        process_c = os.fork()

    # Process A
    if os.getpid() == parent_pid:
        time.sleep(0.2)
        os.close(w)
        r = os.fdopen(r)
        os.kill(process_b, signal.SIGUSR1)
        signal.pause()
        print("A (PID = %d) leyendo:" % os.getpid())
        print(r.read())

    # Process B
    elif not process_b and process_c:
        os.close(r)
        w = os.fdopen(w, 'w')
        signal.pause()
        w.write("Mensaje 1 (PID = %d)\n" % os.getpid())
        os.kill(process_c, signal.SIGUSR1)

    # Process C
    elif not process_c:
        os.close(r)
        w = os.fdopen(w, 'w')
        signal.pause()
        w.write("Mensaje 2 (PID = %d)\n" % os.getpid())
        os.kill(parent_pid, signal.SIGUSR1)


if __name__ == '__main__':
    main()
