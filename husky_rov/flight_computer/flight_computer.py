from rov_server import ROVServer

if __name__ == '__main__':
    port = int(input('Enter a port for the ROV server: '))
    print('Server running on 192.168.2.99 at port {}'.format(port))
    ROVServer('192.168.2.99', port)
