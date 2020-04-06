# MPSH ROV
---

This control system is meant for use on Husky Explorer Robotics' 2018-2019 underwater remotely operated vehicle, the Husky ROVer. This vehicle was designed and manufactured to compete in the 2019 MATE ROV competition at both a regional and international level. The team placed first in Newfoundland and Labrador and tenth in the world, with a first place prize awarded for the best technical documentation in the world.

![Rov](https://user-images.githubusercontent.com/44215543/78517084-7d58e900-7796-11ea-9da9-61458c8c2575.jpg)
_The Husky Rover_

## Application

The robot is powered electrically with six T-100 thrusters. All onboard electronics reside inside a single watertight enclosure. Sensors include water temperature, pitch, roll, enclosure pressure, temperature and humidity. The ROV connects to the surface through a tether of power cables, analog video cables, pneumatic tubing and a single CAT5e cable for digital communication.

![Main ROV SID 2019_](https://user-images.githubusercontent.com/44215543/78517079-79c56200-7796-11ea-9031-adc7ead3c442.jpg)
_The vehicle's electrical block diagram_

The vehicle's software system includes 4 controllers connected over an IP LAN. The two "surface side" controllers, the pilot and co-pilot terminals, use PyQt GUIs to control and monitor the ROV. These programs include live sensor telemetry, live video feeds, keyboard control for the ROV, and even a computer vision system made using OpenCV, for identifying shapes underwater in real time.

![Screenshot (4)](https://user-images.githubusercontent.com/44215543/78517087-8053d980-7796-11ea-8ba8-865663e4abb0.png)
_The pilot's control terminal_

More information about each of the programs in this repo can be found in the section below.

## Programs

| Program | Hardware Platform | Description |
|:-:|:-:|:-:|
| Pilot Terminal | Windows Laptop | The control point for the ROV's pilot. Allows for full control of the ROV's thrusters and actuators, reading of all sensors, and hosts the computer vision software for recognizing shapes underwater. This all occurs through a GUI made using Qt for Python |
| Co-Pilot Terminal | Windows Laptop | Similar to the Pilot Terminal, but also allows for the use of special calculator dialogs. These are useful during missions for calculating task-specific values. |
| Flight Computer | Raspberry Pi 3 | Parses commands from the terminals and executes them by actuating relays, controlling ESCs with PWM, and controlling servos. Also reads sensor data from onboard the ROV and returns it to the surface. |
| Pneumatics Computer | Raspberry Pi 3 | Recieves commands from the terminals and actuates pneumatic solenoids to control the ROV's pneumatic systems at the surface |
