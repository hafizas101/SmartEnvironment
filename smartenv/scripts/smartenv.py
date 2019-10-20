#!/usr/bin/env python3
import rospy
import queue
import time
#from smartenv.srv import *
import threading
from std_msgs.msg import String
from tracker import RobotTracker
from utils.logger import Logger
from object_detector import Object_Detector

class SmartEnv(threading.Thread, Logger):
    def __init__(self, obj_q, trig_q, img_q):
        threading.Thread.__init__(self)
        Logger.__init__(self, "SMART_ENV")
        self.response_queue = obj_q
        self.trigger_queue  = trig_q
        self.image_queue    = img_q
        rospy.init_node('smart_environment', anonymous=True)
        #self.rate = rospy.Rate(10)  # 10hz

        self.ros_listener = rospy.Subscriber("/smart_environment/request",
                String, self.listen_callback)
        self.ros_sender   = rospy.Publisher("/smart_environment/response",
                String, queue_size=10)
        #self.engine = RobotDetector("rtsp://10.90.130.124:554/ch0_0.h264")

    def listen_callback(self, msg):
        data = msg.data
        print(data)
        if data == "start":
            ans = self.run_once()
            newmsg = String()
            newmsg.data = str(ans)
            self.ros_sender.publish(newmsg)

    def run_once(self):
        s1 = {"locate":True, "tag_id":0}
        s2 = {"locate":False}
        self.image_queue.queue.clear()
        self.trigger_queue.put(s1)
        return self.response_queue.get(block=True)

    def run(self):
        rospy.spin()


if __name__ == '__main__':
    try:
        img_queue     = queue.Queue()
        objects_queue = queue.Queue()
        trigger_queue = queue.Queue()

        stream_address = "rtsp://10.90.131.71:554/ch0_1.h264"
        obj_detector = Object_Detector(img_queue, objects_queue)
        tracker      = RobotTracker(img_queue, trigger_queue, stream_address)
        env          = SmartEnv(objects_queue, trigger_queue, img_queue)

        tracker.start()
        obj_detector.start()
        env.start()

    except rospy.ROSInterruptException:
        print("Error occured exiting")
        pass
