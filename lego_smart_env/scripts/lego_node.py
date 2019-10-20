#!/usr/bin/env python3
import os
import rospy
from std_msgs.msg import String
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.motor import LargeMotor,OUTPUT_A,OUTPUT_B,SpeedPercent,MoveTank, MoveDifferential, SpeedRPM
from ev3dev2.sensor import INPUT_4
from ev3dev2.wheel import EV3Tire
from time import sleep
import threading

waiting_s = False
STUD_MM = 8
received = False
turning = False

def send_request():
	global pub
	#print("here")
	global waiting_s
	if not waiting_s:
		waiting_s = True
		print("Obstacle detected, requesting identification")
		req="start"
		newmsg = String()
		newmsg.data = req
		pub.publish(req)
		rate.sleep()

def rcallback(data):
	global obstacles
	global waiting_s
	global received
	global turning
	print(data.data)
	rospy.loginfo(rospy.get_caller_id()+" Detected:  %s", data.data)
	if data.data in obstacle_list:
		try:
			turning = True
			#tank_drive.turn_right(SpeedRPM(60), 90)
		except rospy.ROSInterruptException:
			pass
	else:
		try:
			turning = True
			#tank_drive.turn_left(SpeedRPM(40), 90)
		except rospy.ROSInterrupException:
			pass
	received = True
	waiting_s = False
	#turning = False


if __name__ == '__main__':
	obstacle_list=[]

	print("Startimg ...")
	file_location = os.path.join( "/home/robot/catkin_ws/src/lego_smart_env/scripts", "obstacles.txt" )
	fp=open(file_location, "r")
	obstacle_name=fp.readline()
	while obstacle_name:
		obstacle_list.append(obstacle_name[:-1])
		obstacle_name=fp.readline()

	print("initializing ros node")	
	rospy.init_node('lego_node',anonymous=True)
	print("ros node initialized")
	us=UltrasonicSensor()
	tank_drive=MoveDifferential(OUTPUT_A,OUTPUT_B, EV3Tire, 16*STUD_MM)
	tank_drive.odometry_start()
	rate = rospy.Rate(10)
	pub=rospy.Publisher('/smart_environment/request',String,queue_size=10)
	rospy.Subscriber('/smart_environment/response',String, rcallback, queue_size=5)
	print("starting loop")

	#while not rospy.is_shutdown():
	#	rate.sleep()
	#	pass

	while not rospy.is_shutdown():	
		try:
			if us.distance_centimeters>10 and not turning:
				tank_drive.on_for_distance(SpeedRPM(40), -20)

			else:	
				send_request()
				#print("Obstacle detected, requesting identification")
				#while not received:
				#	pass
				#received = False

			if turning:
				tank_drive.turn_right(SpeedRPM(60), 90)
				turning = False

		except rospy.ROSInterruptException:
			pass

		rate.sleep()
		pass




























