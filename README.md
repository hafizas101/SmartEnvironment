# ROS-based Integration of Smart Space and a Mobile Robot as the Internet of Robotic Things
This repository holds the code and data about my research paper titled "ROS-based Integration of Smart Space and a Mobile Robot as the Internet of Robotic Things" available on [ResearchGate profile](https://www.researchgate.net/publication/336402567_ROS-based_Integration_of_Smart_Space_and_a_Mobile_Robot_as_the_Internet_of_Robotic_Things). The video demo of our project is available on [YouTube](https://www.youtube.com/watch?v=zKeig5aofyg) This paper attempts to propose how a smart space can be implemented to increase the spatial awareness of a robot by providing more data to make better informed decisions. We focus on using the Robot Operating System (ROS) as a framework to integrate Smart Space and a mobile robot to expand the robots sensory information and make collision avoidance decisions.The key contributions of this research paper are as follows:
- The demonstration of how Smart Space with robust offboard hardware can assist simple robots with no computer vision and image processing capabilities to take complex and computationally expensive decisions.
- The development of the method to replace large number of on-board noisy robot sensors with fewer external sensors.
- The implementation of the ground framework for the field of Internet of Robotic Things (IoRT). 

As shown in the firgure below, the main components of our experimental setup are as follows:
- Mobile Robot’s Node.
- Smart Space’s Node.
<p align="center">
  <img width="600" height="300" src="https://github.com/hafizas101/smart_environment/blob/master/images/topicArchi.png">
</p>


Communication between the robot and the processing node achieved using ROS. One great feature of ROS is that nodes (independent components of the robot) can communicate with each other using messages. We leveraged this framework to send messages from the mobile robot to our smart space processing device.

## Installation Instructions
1. Boot lego mindstorm ev3 robot using micro SD card running ev3 image using the instructions at https://www.ev3dev.org/
2. Install ROS melodic and create a catkin workspace on ev3 image robot as well as desktop PC using the instructions available on ROS Wiki http://wiki.ros.org/ROS/Tutorials/InstallingandConfiguringROSEnvironment
3. Place the folder named "lego_smart_env" in the src folder of catkin workspace running on lego robot. Do Catkin_make and source devel.
4. Place the folder named "smartenv" in the src folder of catkin workspace running on desktop PC. Do Catkin_make and source devel.
5. Download wights file from and place in directory /smartenv/scripts/yolo_files/
5. First run the smart environment node at desktop PC using the command:
~~~
rosrun smartenv smartenv
~~~
7. Then run the robot node using the command:
~~~
rosrun lego_smart_env lego_node.py
~~~
Robot should start moving forward.

## Experiment Results
In our experiment, we are able to detect and classify objects by leveraging the services provided by the smart space infrastructure using a low-end mobile robot with no computer vision abilities. As the mobile robot ROS node is initialized, robot starts moving forward as shown in below figure
<p align="center">
  <img width="800" height="370" src="https://github.com/hafizas101/smart_environment/blob/master/images/design1.jpg">
</p>
As, the Lego ev3 robot detects an obstacle in front of it using ultrasonic sensor, it stops and communicates to the smart space node to request for object detection as shown in below figure.
<p align="center">
  <img width="800" height="370" src="https://github.com/hafizas101/smart_environment/blob/master/images/design2.jpg">
</p>
As soon as the smart space node receives message from robot node, it reads the video stream coming from IP camera. The message published by robot contains AprilTag type and Tag ID which serve as identification information for the smart space node to find robot location. The area around robot is cropped from the current image to ensure YOLO classifier to detect only the obstacles around the robot. Using the supplied AprilTag information, the smart space node is able to locate the robot and classify the obstacle detected by the robot. Information about the obstacles is sent back to the robot node. The robot takes turn after receiving the requested information as shown in below figure
<p align="center">
  <img width="800" height="370" src="https://github.com/hafizas101/smart_environment/blob/master/images/design3.jpg">
</p>
