import socket
import sys
import getopt


def send_message(connection, message):
    connection.send(message.encode('ascii'))
    response = connection.recv(1024)
    print("Response from server:", response.decode("ascii"))


def main():
    host = None
    port = None

    (opt, arg) = getopt.getopt(sys.argv[1:], 'h:p:', ["host=", "port="])

    for (option, argument) in opt:
        if option == '-h' or option == '--host':
            host = argument
        elif option == '-p' or option == '--port':
            port = int(argument)

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print('Failed to create socket')
        sys.exit()

    assert host is not None
    assert port is not None

    s.connect((host, port))

    name = 'hello|' + input('Enter your name: ')
    send_message(s, name)

    email = 'email|' + input('Enter your email: ')
    send_message(s, email)

    key = 'key|' + input('Enter the key: ')
    send_message(s, key)

    print("Closing connection")
    send_message(s, "exit")


if __name__ == '__main__':
    try:
        main()
    except AssertionError or getopt.GetoptError:
        print("You must enter the port and host value using -h or --host and -p or --port")
