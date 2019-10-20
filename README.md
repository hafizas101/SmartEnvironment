# ROS-based Integration of Smart Space and a Mobile Robot as the Internet of Robotic Things
This repository holds the code and data about my research paper titled "ROS-based Integration of Smart Space and a Mobile Robot as the Internet of Robotic Things" available on [ResearchGate profile](https://www.researchgate.net/publication/336402567_ROS-based_Integration_of_Smart_Space_and_a_Mobile_Robot_as_the_Internet_of_Robotic_Things). This paper attempts to propose how a smart space can be implemented to increase the spatial awareness of a robot by providing more data to make better informed decisions. We focus on using the Robot Operating System (ROS) as a framework to integrate Smart Space and a mobile robot to expand the robots sensory information and make collision avoidance decisions.The key contributions of this research paper are as follows:
- The demonstration of how Smart Space with robust offboard hardware can assist simple robots with no computer vision and image processing capabilities to take complex and computationally expensive decisions.
- The development of the method to replace large number of on-board noisy robot sensors with fewer external sensors.
- The implementation of the ground framework for the field of Internet of Robotic Things (IoRT). 

As shown in the firgure below, the main components of our experimental setup are as follows:
- Mobile Robot’s Node.
- Smart Space’s Node.
<p align="center">
  <img width="600" height="350" src="https://github.com/hafizas101/smart_environment/blob/master/images/topicArchi.png">
</p>


Communication between the robot and the processing node achieved using ROS. One great feature of ROS is that nodes (independent components of the robot) can communicate with each other using messages. We leveraged this framework to send messages from the mobile robot to our smart space processing device.
## Mobile Robot Node
<p align="center">
  <img width="500" height="230" src="https://github.com/hafizas101/smart_environment/blob/master/images/robot_spec.png">
</p>
The hardware and software specifications of our mobile robot have been presented in the Table I.The AprilTag is attached on the robot. The robot is also equipped with an ultrasonic sensor for obstacle detection. On detecting an obstacle, the robot stops and publishes a message to outgoing message topic on which the smart space node is already listening. This message contains identification information. The identification information is the aprilTag data (Tag family and tag ID). AprilTags are divided into different families. Any combination of tag type and tag ID is guaranteed to be unique AprilTag image. Once the identification information has been sent to the smart space node, the robot starts listening for messages from the smart space node on the incoming messages topic. The smart space node locates the robot using the provided information. After doing the necessary processing, the smart space sends back data describing the obstacles in the vicinity of the robot. In our case, the smart space node replies with a list of the names of the detected objects. Based on this information, the robot can decide to continue on the predefined path or change its path. The code for the ROS package running on the Lego EV3 robot is available on [Github Repository](https://github.com/hafizas101/legoNode).

## Smart Space Node
<p align="center">
  <img width="500" height="240" src="https://github.com/hafizas101/smart_environment/blob/master/images/smart_spec.png">
</p>
The smart space node was implemented on a desktop computer whose hardware and software specifications have been presented in the Table II. The IP camera was connected to provide video stream of the environment. The smart space comprises of a ROS master which serves as a central point for all the robots in the smart space environment. The separate ROS node (smart space node) is also implemented to receive and process information from the robots. The smart space node listens on the specified topic for messages published by the robot nodes. This message contains identification information as described above. When a message is received, the smart space node reads the video stream and attempts to detect all AprilTags in the field of view. We compare the tag ID and tag type of the detected AprilTags with the tag information sent by the robot in order to locate the sending robot. Using the AprilTag we can also estimate the pose of the robot which enables us to crop a specific section from the current image frame to include only the robot and the obstacle. This ensures that only the necessary part of the image is processed. The cropped section of the frame is passed to the YOLO object classifier which returns a list of the detected objects.ROS package for Smart Space node can be downloaded from the [Github repository](https://github.com/uched41/smartenv).

## Experiment Results
In our experiment, we are able to detect and classify objects by leveraging the services provided by the smart space infrastructure using a low-end mobile robot with no computer vision abilities. As the mobile robot ROS node is initialized, robot starts moving forward as shown in below figure
<p align="center">
  <img width="500" height="240" src="https://github.com/hafizas101/smart_environment/blob/master/images/design1.jpg">
</p>
As, the Lego ev3 robot detects an obstacle in front of it using ultrasonic sensor, it stops and communicates to the smart space node to request for object detection as shown in below figure.
<p align="center">
  <img width="500" height="240" src="https://github.com/hafizas101/smart_environment/blob/master/images/design2.jpg">
</p>
As soon as the smart space node receives message from robot node, it reads the video stream coming from IP camera. The message published by robot contains AprilTag type and Tag ID which serve as identification information for the smart space node to find robot location. The area around robot is cropped from the current image to ensure YOLO classifier to detect only the obstacles around the robot. Using the supplied AprilTag information, the smart space node is able to locate the robot and classify the obstacle detected by the robot. Information about the obstacles is sent back to the robot node. The robot takes turn after receiving the requested information as shown in below figure
<p align="center">
  <img width="500" height="240" src="https://github.com/hafizas101/smart_environment/blob/master/images/design3.jpg">
</p>
