from tcp_server import TCPServer
import sys


if __name__ == '__main__':
    TCPServer('192.168.2.100', int(sys.argv[1]))
