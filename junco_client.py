import socket
import sys  # for exit
import getopt


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
    s.send(name.encode('ascii'))
    response = s.recv(1024)
    print(response.decode("ascii"))

    email = 'email|' + input('Enter your email: ')
    s.send(email.encode('ascii'))
    response = s.recv(1024)
    print(response.decode("ascii"))

    key = 'key|' + input('Enter the key: ')
    s.send(key.encode('ascii'))
    response = s.recv(1024)
    print(response.decode("ascii"))

    s.send("exit".encode('ascii'))
    response = s.recv(1024)
    print(response.decode("ascii"))


if __name__ == '__main__':
    try:
        main()
    except AssertionError:
        print("You must enter the port and host value using -h or --host and -p or --port")
