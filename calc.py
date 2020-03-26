#!/usr/bin/python

import sys
import getopt


# This function is called in case that both, numbers and the operator, are correct.
def calculate_result(num1, op, num2):
    if op == '+':
        result = num1 + num2
    elif op == '-':
        result = num1 - num2
    elif op == 'x':
        result = num1 * num2
    else:
        result = num1 / num2
    return result


def main():
    try:
        (opt, arg) = getopt.getopt(sys.argv[1:], 'n:m:o:', ["number1=", "number2=", "operation="])

        if len(opt) != 3:
            print("Error: Expected 3 options,", len(opt), "received")
            exit()

        for (option, argument) in opt:
            if option == '-n' or option == '--number1':
                number1 = int(argument)
            elif option == '-m' or option == '--number2':
                number2 = int(argument)
            elif option == '-o' or option == '--operation':
                operation = argument

        if operation not in ['+', '-', 'x', '/']:
            print("Invalid operation")
        else:
            print(number1, operation, number2, "=", calculate_result(number1, operation, number2))

    except getopt.GetoptError as e:
        print("Error: " + str(e))

    except NameError:
        print("Missing options")

    except ValueError:
        print("Your numbers must be integers")

    except ZeroDivisionError:
        print("You can't divide by zero")


if __name__ == '__main__':
    main()
