#!/usr/bin/python

import getopt
import sys
import multiprocessing


def read_options():
    processes = bottom = top = None

    (opt, arg) = getopt.getopt(sys.argv[1:], 'p:m:n:')

    if len(opt) != 3:
        print(f"Error: Expected 3 options [-p] [-m] and [-n], {len(opt)} received")
        sys.exit(0)

    for (option, argument) in opt:
        if int(argument) < 0:
            raise ValueError
        if option == '-p':
            processes = int(argument)
        elif option == '-m':
            bottom = int(argument)
        elif option == '-n':
            top = int(argument)

    assert processes is not None and bottom is not None and top
    if bottom > top:
        raise getopt.GetoptError('Bottom number [-m] can not be higher than Top number [-n]')
    if processes > top - bottom:
        raise getopt.GetoptError("Can't have more processes than numbers to process")

    return processes, bottom, top


def square_sublist(sublist):
    for num in sublist:
        print(f'{multiprocessing.current_process().name}: {num}^2 = {num ** 2}')


def split_list(target_list, slices):
    size = len(target_list)
    return [target_list[i * size // slices:(i + 1) * size // slices] for i in range(slices)]


def main():
    n_processes, min_num, max_num = read_options()
    target_list = list(range(min_num, max_num))
    processes = []

    for sublist in split_list(target_list, n_processes):
        process = multiprocessing.Process(target=square_sublist, args=(sublist,))
        process.start()
        processes.append(process)

    for p in processes:
        p.join()


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
