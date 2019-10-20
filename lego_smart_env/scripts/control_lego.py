#!/usr/bin/env python3
import os
file_location = os.path.join( "/home/robot/catkin_ws/src/lego_smart_env/scripts", "obstacles.txt" )
fp=open(file_location, "r")
item_name=fp.readline()
obstacle_list=[]

while item_name:
	obstacle_list.append(item_name[:-1])
	item_name=fp.readline()

print(obstacle_list)

fp.close()
