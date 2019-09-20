# MPSH ROV
###### ROV control software for Mount Pearl Senior High's underwater robotics team
---
### Application
This control system is meant for use on Husky Explorer Robotics' 2018-2019 underwater remotely operated vehicle, the Husky ROVer. This vehicle was designed and manufactured to compete in the 2019 MATE ROV competition at both a regional and international level. The team placed first in Newfoundland and Labrador and tenth in the world, with a first place prize awarded for the best technical documentation in the world.

The robot is powered electrically with six T-100 thrusters. All electronics reside inside a single watertight enclosure. Sensors include water temperature, pitch, roll and enclosure pressure, temperature and humidity. The ROV connects to the surface through a tether of power cables, analog video cables, pneumatic tubing and a single CAT5e cable for digital communication.

### Overview
The system consists of four controllers connected over an IP LAN. On boot, the flight computer creates a TCP server and all other devices connect.

| Program | Hardware Platform | Purpose
|:-:|:-:|:-:|
| Pilot Terminal | Windows Laptop | The control point for the ROV's pilot. Allows for full control of the ROV's thrusters and actuators, reading of all sensors, and hosts the computer vision software for recognizing shapes underwater. This all occurs through a GUI made using Qt for Python |
| Co-Pilot Terminal | Windows Laptop | Similar to the Pilot Terminal, but also allows for the use of special calculator dialogs. These are useful during mission for calculating task-specific values. |
| Flight Computer | Raspberry Pi 3 | Parses commands from the terminals and executes them by actuating relays, controll ESCs with PWM, and controlling servos. Also reads sensor data from onboard the ROV and returns it to the surface. |
| Pneumatics Computer | Raspberry Pi 3 | Recieves commands from the terminals and actuates pneumatic solenoids to control the ROV's pneumatic systems |
