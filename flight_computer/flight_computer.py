from app.rov import ROV

if __name__ == '__main__':
    port = int(input('Enter a port for the ROV server: '))
    # ip = input('Enter an IP address for the ROV server: ')
    ROV('192.168.2.99', port)
