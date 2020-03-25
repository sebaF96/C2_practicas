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


try:
    (opt, arg) = getopt.getopt(sys.argv[1:], 'n:m:o:', ["number1=", "number2=", "operation="])

    # This prevents the input to have repeated or missing options.
    # If the input has 3 but still incorrect options the except NameError block will catch it.
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
    # If any option is missing arguments, or any other input problem.
    print("Error: " + str(e))

except NameError:
    print("Missing options")

except ValueError:
    # If one or both numbers are not integers.
    print("Your numbers must be integers")

except ZeroDivisionError:
    # If -m or --number2 = 0
    print("You can't divide by zero")
