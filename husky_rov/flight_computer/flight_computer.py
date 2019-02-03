from tcp_server import TCPServer

if __name__ == '__main__':
    port = int(input('Enter a port for the ROV server: '))
    ip = input('Enter an IP address for the ROV server: ')
    TCPServer(ip, port)
