#!/usr/bin/python

import getopt
import sys
import subprocess as sp


def get_datetime():
    from datetime import datetime
    return datetime.now().strftime("%d/%m/%Y %H:%M")


def write_log(log_file, command, error_message, correctly_executed=False):
    with open(log_file, "a") as file:
        if correctly_executed:
            file.write(get_datetime() + " - command '" + command + "' successfully executed.\n")
        else:
            file.write(get_datetime() + " - " + error_message)


def write_stdout(output_file, output):
    with open(output_file, "a") as file:
        file.write(output + "\n")


def main():
    try:
        (opt, arg) = getopt.getopt(sys.argv[1:], 'c:f:l:')

        if len(opt) != 3:
            raise AttributeError("Expected 3 options, " + str(len(opt)) + " received")

        for (option, argument) in opt:
            if option == '-c':
                command = argument
            elif option == '-f':
                output_file = argument
            elif option == '-l':
                log_file = argument

        with sp.Popen([command], shell=True, universal_newlines=True, stdout=sp.PIPE, stderr=sp.PIPE) as proccess:

            proccess_stdout, proccess_stderr = proccess.communicate()

            if proccess.returncode is 0:
                write_stdout(output_file, proccess_stdout)
                write_log(log_file, command, proccess_stderr, correctly_executed=True)
            else:
                write_log(log_file, command, proccess_stderr)

    except getopt.GetoptError as e:
        print("Error: " + str(e))
    except NameError:
        print("Error: Missing options")
    except AttributeError as e:
        print("Error: " + str(e))
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
