#!/usr/bin/python

import sys
import getopt
import os.path


def read_file(path):
    if os.path.isfile(path):
        with open(path, 'r') as file:
            content = file.read()
            return content
    else:
        raise FileNotFoundError()


def paste(path, content):
    if not os.path.isdir(path):
        with open(path, 'w') as file:
            file.write(content)
    elif os.path.exists(path):
        path = path + "copied_file.txt"
        paste(path, content)
    else:
        raise NotADirectoryError


def main():
    try:
        (opt, arg) = getopt.getopt(sys.argv[1:], 'i:o:', ["input=, output="])

        if len(opt) != 2:
            print("Error: Expected 2 options,", len(opt), "received")
            exit()

        for (option, argument) in opt:
            if option == '-i' or option == '--input':
                source_file_path = argument
            elif option == '-o' or option == '--output':
                destiny_file_path = argument

        content_to_copy = read_file(source_file_path)

        paste(destiny_file_path, content_to_copy)

    except getopt.GetoptError as e:
        print("Error : " + str(e))
    except NameError:
        print("Missing options")
    except IsADirectoryError:
        print("You need to specify the file name")
    except FileNotFoundError:
        print("File doesn't exist")


if __name__ == '__main__':
    main()
