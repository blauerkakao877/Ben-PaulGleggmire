Roadrunners - Future engineers 2024 
====

<img src="https://github.com/blauerkakao877/Roadrunners-FE24/assets/131390374/50f191a3-0340-4c7b-ba7b-8b8aab709dd7" width="400" height="400">

## Table of Contents 📚👇

1. [Overview](#overview) 🌟
2. [Design Process](#Design-Process)🔧
3. [Car Photos](#carphoto)
4. [Mobility Management](#Mobility-Management)
    - [Chassis](#Chassis)
    - [Assembly Instructions](#assembly-instructions) 🛠
    - [Driving Motor and Gearing](#Driving-Motor-and-Gearing)
    - [Steering Mechanism](#Steering-Mechanism)
    - [Power and Sense Management](#Power-and-Sense-Management)  
    - [Power supply](#Power-supply)
    - [Controllers](#Controllers)
    - [Sensors](#Sensors)
    - [Camera](#camera)
    - [Schematics](#schematics) 📐👀
    - [Components List](#components-list) 🔍
5. [Software Design](#software) 💻👨‍💻
    - [Software Development](#software-development)
    - [Opening Race](#opening-race)
    - [Obstacle Race](#obstacle-race)
    - [Programming Languages](#programming-languages) 👩‍💻
    - [Dependencies](#dependencies) 
6. [Utilities](#utilities) 🛠
    - [Failsafe Mechanisms](#failsafe)
    - [Debugging Tools](#debugging-tools) 🐞🔍
7. [Team Photos](#team-photos) 📸
8. [Demonstration Videos](#demonstration-videos) 🎥
9. [Contributors](#contributors) 👥
10. [Resources](#sources) ℹ

   
<a name="overview"></a>


## Overview 🌟

<img src="./v-photos/Beauty01.jpeg" width="50%">


Welcome to the official GitHub repository for Team Smart Riders from Germany, participating in the WRO World Finals 2023. This repository contains all the code, documentation, and resources for our project, SmartiecarV2. We have used scoring criteria from the ruleblock as headings in our documentation to make it easy to navigate our repository.

<img src="https://github.com/Nezar187/GSG_SmartiecarV2/assets/131591590/7b0c5513-870f-475c-9993-cfca6aa5659f" width="75%">




We built our car from Lego parts and plastic plates.
The chassis consists of Lego Technic parts. 
We looked in the book ‘The Unofficial LEGO Technic Builder's Guide 2nd Edition’ to find out how to build a car from LEGO, especially how to build a steering system.
Then we developed our own chassis. 
Our first car last year had a plastic base plate, LEGO parts on it and then another plastic top plate and was quite big.
This year we wanted to try and build a smaller car so that it would be easier to get past the obstacles. 
To do this, we first focussed on building the smallest possible chassis with the smallest possible motors. We only used Lego this year and managed to create a much smaller chassis.
However, there is another plastic plate on the chassis for the sensors and the control electronics.

Last year, we used an Arduino for control and a Pixy2 Smartcam as a camera. The Arduino often reacted slowly and the camera image could not be optimally adjusted.
This year we are using a Raspberry Pi with a Pi wide-angle camera. 
There are many electronic components available as HATs for the Raspberry Pi that you can simply plug onto the Pi. We have also taken advantage of this to save space so that our car can remain smaller.

We also thought that it would be good to be able to see what the car is currently seeing or analysing while driving. This helps to find reasons for errors.
We didn't want to build a display on our car. For one thing, they are rather large and heavy and it's not easy to read what's on them when you're standing next to the pitch. Our idea is to use LEDs in different colours. We built our own LED strip with red and green for the obstacles, blue and orange for the lines and yellow and white to indicate that the car is ready to start.

When testing the obstacle race, we had problems with our car getting stuck on the inside wall in very tight bends. For example: driving in the right-hand direction, a red obstacle on the inside at the very end and another red obstacle immediately after the bend.
When we realised that you are allowed to touch the walls this year, we installed wall rollers at the very end at the front and on the side, which ensure that the car can still squeeze around the corner in most cases if it touches the wall when turning in.

Motorisation and power supply
We use Lego Powerfunctions motors as a drive because they are very easy to install in a Lego chassis.
In the beginning we tried to drive with a longitudinally installed Lego XL motor, but it had too little speed and was much too slow. We then used an L-motor. It worked quite well with that when you were going fast. 
Then we used 2 Powerfunctions L Lego motors because 1 motor alone didn't have enough power when driving slowly and our car got stuck on bumps. 

We connected the two engines to each other via a gearbox because the rules state that you can only have two engines if you couple them mechanically. At first we thought that it was good to make the car as fast as possible. But then we realised that you can drive much more accurately if you drive more slowly. 

You need a motor driver so that the Raspberry Pi can control the motors. We used a motor HAT from Adafruit, which can be plugged into the Raspberry Pi. 
We then had to connect the motors to the motor driver for the power supply. To do this, we cut off the normal Lego connections and soldered on JST connectors. 
We didn't screw the cut cables directly to the HAT because the power function cable cores are quite thin and don't hold well in the screw terminals.
For steering we use a Geekservo Lego-compatible servo, which has a housing like a Lego brick. The Raspberry Pi controls the steering servo via a 16-channel servo HAT from Waveshare. This can be plugged onto the motor HAT so that it doesn't take up any extra space.
You only need one channel of the HAT servo for the servo. 
It can also control LEDs. We use 6 of the other slots to control our LED strip.
We use a 7.4V lithium-polymer battery (Lipo) for the overall power supply. On our car we need 9V for the Lego traction motors and 5V for the servo, the LEDs and the Raspberry Pi. The voltage of the battery is not always the same, it drops from 8.4V when fully charged to 6.0 when the battery is empty.
We have installed a step-up converter (XL6109) for the motors, which increases the voltage from the battery to a constant 9V. 

For everything that needs 5V, we have a step-down converter that has a USB connection for the Raspberry Pi and screw terminals for the servo HAT.
The step-down converter needs at least 7.5V at the input, so it switches off our car even when the battery is only half empty. On the other hand, this is a good fuse to prevent the battery from running out and being damaged.
In our circuit diagram you can see how the components are wired together and supplied with power from the Lipo battery.

Sensors
For the sensors, we first considered which ones we could use for which race mode. Last year we already had experience with ultrasonic distance sensors and wanted to use them again.
We decided in favour of the URM09 digital sensors from DFRobot because they can work with 3.3V and because their mounting holes fit Lego. 
The Raspberry Pi only has 3.3V logic voltage and most ultrasonic sensors need 5V.
We mounted an ultrasonic sensor at the front of each side to measure the distances to the side walls and one to the front to measure the distance to a wall opposite.
We then considered that we would have to recognise the lines in the obstacle race in order to find the bends. Only with the distances to the side could you measure an obstacle that is directly behind the bend and then miss the bend. 

We have installed an Adafruit AS7262 6-channel colour sensor for line detection. The sensor has its own LED to illuminate the floor.
We also wanted to be able to recognise in which direction the car has just turned and how far it has already turned overall. For this we need a gyro sensor or an IMU sensor.
One problem with gyro sensors is drift. The gyro does not return to 0 when turning and turning back and the error increases over time. We have tested various sensors. The Bosch BNO085 worked best. 
To recognise the obstacles, you also need a camera. We chose a wide-angle camera, the Raspberry Pi V3 Wide Camera, so that the Raspberry Pi can see as much of the playing field as possible.

Our first version from the opening race only used the two side ultrasonic sensors to find the first corner and then drive along the inside wall at a fixed distance. We then used the gyro to measure when the car had turned 360 degrees 3 times. Then we stopped.
When we started the obstacle race, we realised that the colour sensor only sees a line if you query it at the exact moment the car crosses the line. If the control programme is not running fast enough, you can easily miss a line. That was a problem. 
We then tried to recognise the lines with the camera. Once we had managed to set the camera so that orange and red were clearly different, it worked (see chapter on obstacles). 
The LEDs show what the car is currently seeing: blue/orange for lines, red/green for obstacles. This is very useful for testing.

n our obstacle programme, we also recognise the walls with the camera and steer straight ahead using the gyro. For fun, we tested how the programme behaves in the opening race. We were surprised to find that it also works and that you can even drive much faster because the Raspberry Pi processes the camera images much faster than the ultrasonic sensors can measure. 
We then decided to make another opening version of our obstacle race, in which we removed the obstacle detection and increased the speed.

 Programming obstacles
We use Python3 as the programming language and the listing on the right shows the sequence of the main loop.

Main loop
In the obstacle race, we use the camera to analyse the playing field and the gyro sensor to determine the orientation of the car.
We use the OpenCV and Numpy libraries for image processing. To read the gyro and drive and control the car, we used libraries from Adafruit Circuitpython.
We read the next camera image and cut off the top edge in order to minimise the amount of the image that does not belong to the playing field. 
The camera delivers the image in BGR (blue-green-red) format. In order to be able to filter out colours better, the image is also converted into an HSV (Hue Saturation Value) format.
We filter the black walls from the BGR image and calculate whether there is a risk of collision on the right or left.
We filter the lines and obstacles from the HSV image.
We use the lines to calculate the current straight ahead gyro course.
We use this information to determine the next control movement.

Determining the next control movement
Avoid the wall first: 
If the collision alarm is set on one side, we steer hard away from the wall.
 
Then avoid an obstacle: 
If there is an obstacle in the image and there is no line at the bottom of the image, steer so that the obstacle in the image moves all the way to the left (red) or all the way to the right (green).
The camera will lose the obstacle from the picture before we are completely past it. We therefore remember that we are steering by obstacle and the time.

If the obstacle is no longer visible, we continue for a timeout in the last direction past the obstacle.
Then we reset the ‘Obstacle’ flag.

If there is no wall and no obstacle control:
Steer by gyro to the straight ahead direction in degrees

If an obstacle is visible and at the same time there is a line at the bottom of the screen (in the colour of the direction of travel), the obstacle is directly behind the curve. We then drive up to the line before we swerve out of the way. Otherwise, the car may no longer see the wall and swerve inwards to avoid the obstacle before it has passed the inside corner. 

Processing the walls
We filter out the parts of the BGR image that appear very dark in all 3 colour channels at the same time. This results in a black and white mask in which the walls are white and everything else is black.
As a measure of how close we are to a wall, we take the height of the wall in the image. Due to the perspective, nearer parts of the wall appear higher in the picture than those further away.
We now split the wall mask in the centre into a wall image on the left and a wall image on the right. To determine the height, we use numpy to count the sum of all pixels in each image column. 
Since black = 0, only the white pixels are counted. We then determine the maximum value for each page.
If the maximum value for one side is too high, we set a flag to True for collision alarm for that side. If there is a collision alarm on both sides at the same time, the car drives directly towards a wall. 

In addition, we return the height for each side as control information.
We first tried to filter the walls using the HSV image. However, this did not work so well as black is not a colour in the Hue range.
Then we tried to use a greyscale image that only shows the brightness. 
This doesn't work so well either, because the blue lines and green obstacles often appear very dark in the greyscale image and would then be mistaken for walls.
This effect can be avoided with the BGR image because the blue lines in the blue channel and the green obstacles in the green channel appear lighter and can therefore be filtered out.  

Processing the obstacles
To recognise the obstacles, we first filter red areas and green areas from the HSV image, resulting in a black and white mask for red and one for green.
The obstacles appear white on a black background. We apply a blur effect so that there is no noise in the masks.
Then, as with the lines, we invert the masks so that the obstacles appear black on white. Then we use the Simple Blob Detector again to find black ‘blobs’ on the masks. 
For each colour, we then go through the list of blobs found and note the largest blob. Then we compare the largest red blob with the largest green blob.
The largest of the two is the next obstacle.
We use slightly different parameters for the blob detector for the obstacles than for the lines. 
For the control, we then supply the x and y position of the blob centre point and the size of the blob in pixels.

Processing the lines
The lines are used to determine the direction of travel, how many corners have already been travelled and the current straight-ahead course according to Gyro.
During the race, we cut out a small area at the bottom centre of the HSV image. We only look for the lines in this area. 
If a line appears in this area, the car is almost on the line. To find a line, we filter out the colour of the line in the HSV image. 
The result is a black and white mask in which the line appears white. Then we convert the mask with Opencv so that it becomes a sharp line on white.
Then we apply the OpenCV function Simple Blob Detector, which can find black areas on a white background. 
We set a minimum size of pixels from which the Simple Blob Detector should recognise the line. The line is then fully in the image.
As the camera cannot look right in front of the wheels, we find the line just before the car drives over it.

We start by looking for orange and blue. As soon as the first line has been found, we remember the direction of travel and only search for this colour.
We then set a short timeout before evaluating the line found. This means that the line is only analysed when the car actually drives over it.
When evaluating the line, we count the number of lines already found.
We then calculate the straight-ahead direction in degrees as number_lines*90 for the direction of travel to the right or number_lines* (-90) for the left.
This means that our car automatically drives round the bend when it steers back to the gyro after the line.





Sources and Resources:
The Unofficial LEGO Technic Builder's Guide 2nd Edition
Ingmar Stapel: Robot cars with the Raspberry Pi
Learn.adafruit.com
Dfrobot.com
Opencv.org/get-started
Docs.Opencv.org












