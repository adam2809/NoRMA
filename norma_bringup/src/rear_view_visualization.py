#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Imu,Image
from cv_bridge import CvBridge
import cv2
import numpy
import pyrealsense2
from sensor_msgs.msg import CameraInfo
from geometry_msgs.msg import Point32


roll = pitch = yaw = 0.0

height = 0
width = 0

thresh = 1
def rgb_cb msg):
    global width,height
    width = msg.width 
    height = msg.height 
    
    rgb = bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')


def laser_cb(msg):
    global ranges
    ranges = msg.ranges

rospy.init_node('rear_view_visualization')

rgb_info = rospy.wait_for_message('/camera/color/camera_info', CameraInfo, timeout=10)

rospy.Subscriber('/camera/color/image_raw', Image, rgb_cb)
rospy.Subscriber('/scan_camera', LaserScan, laser_cb)


while not rospy.is_shutdown():
    rospy.spinOnce()
