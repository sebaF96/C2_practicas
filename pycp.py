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
        raise FileNotFoundError("Source file not found")


def paste(path, content, basename=""):
    if not os.path.isdir(path):
        # If destiny filename is specified
        with open(path, 'w') as file:
            file.write(content)
    elif os.path.exists(path):
        # If destiny exists and is a directory, the file is copied with the original name
        path = path + basename
        paste(path, content)
    else:
        raise NotADirectoryError("Destiny directory not found")


def main():
    try:
        (opt, arg) = getopt.getopt(sys.argv[1:], 'i:o:', ["input=, output="])

        if len(opt) != 2:
            raise AttributeError("Expected 2 options, " + str(len(opt)) + " received")

        for (option, argument) in opt:
            if option == '-i' or option == '--input':
                source_file_path = argument
            elif option == '-o' or option == '--output':
                destiny_file_path = argument

        content_to_copy = read_file(source_file_path)

        paste(destiny_file_path, content_to_copy, os.path.basename(source_file_path))

    except getopt.GetoptError as e:
        print("Error: " + str(e))
    except NameError:
        print("Error: Missing options")
    except AttributeError as e:
        print("AttributeError: " + str(e))
    except NotADirectoryError as e:
        print("Error: " + str(e))
    except FileNotFoundError as e:
        print("FileNotFoundError: " + str(e))


if __name__ == '__main__':
    main()
