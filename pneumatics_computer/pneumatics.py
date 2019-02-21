from app.pneumatics_computer import PneumaticsComputer


def main():
    port = input('Enter a port to connect to: ')
    PneumaticsComputer(port)


if __name__ == '__main__':
    main()
