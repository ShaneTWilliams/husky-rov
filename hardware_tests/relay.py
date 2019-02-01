import pigpio

rpi = pigpio.pi()
pin = input("Enter a pin: ")

while True:
    speed = input("Press enter to write HIGH")
    rpi.write(pin, 1)
    input("Press enter to write pull LOW")
    rpi.write(pin, 0)
