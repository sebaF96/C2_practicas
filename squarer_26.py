#!/usr/bin/python

import getopt
import multiprocessing
from squarer_25 import read_options


def square(number):
    print(f'{multiprocessing.current_process().name}: {number}^2 = {number ** 2}')


def main():
    n_processes, min_num, max_num = read_options()
    with multiprocessing.Pool(n_processes) as pool:
        input('press intro to see the map result ')
        pool.map(square, range(min_num, max_num))

        input('\npress intro to see the apply result ')
        [pool.apply(square, (n,)) for n in range(min_num, max_num)]


if __name__ == '__main__':
    try:
        main()
    except getopt.GetoptError as e:
        print(e)
    except AssertionError:
        print('Expected options [-p], [-m] and [-n]')
    except ValueError:
        print('All 3 options must be positive integers')
    except Exception as e:
        print(e)
