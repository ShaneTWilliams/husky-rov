import pigpio

rpi = pigpio.pi()
pin = input("Enter a pin: ")

while True:
    speed = input("Enter a speed: ")
    rpi.set_servo_pulsewidth(pin, speed)
    input("Press any key to stop")
