from tcp_server import TCPServer

if __name__ == '__main__':
    port = int(input('Enter a port for the ROV server: '))
    TCPServer('192.168.0.98', port)
