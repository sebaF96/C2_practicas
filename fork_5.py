#!/usr/bin/python

import os
import getopt
import sys


def main():
    (opt, arg) = getopt.getopt(sys.argv[1:], 'n:')
    if len(opt) != 1:
        raise getopt.GetoptError("Expected one option with its argument")

    number_of_children = int(opt[0][1])
    father_id = os.getpid()

    for i in range(number_of_children):
        if os.fork() == 0:
            print("Soy el proceso", os.getpid(), ", mi padre es", os.getppid())
            break

    # If the father doesn't wait, some children will be inherited by
    # process init, showing an incorrect message (mi padre es 1), so...
    if os.getpid() == father_id:
        os.wait()


if __name__ == '__main__':
    try:
        main()
    except getopt.GetoptError as e:
        print(e)
    except ValueError:
        print("Argument must be an integer")
