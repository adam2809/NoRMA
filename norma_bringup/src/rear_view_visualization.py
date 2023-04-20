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

    angle_min = msg.angle_min
    angle_max = msg.angle_max
    angle_increment = msg.angle_increment

    range_min = msg.range_min
    range_max = msg.range_max

rospy.init_node('rear_view_visualization')
rgb_info = rospy.wait_for_message('/camera/color/camera_info', CameraInfo, timeout=10)
range_max
rospy.Subscriber('/camera/color/image_raw', Image, rgb_cb)
rospy.Subscriber('/scan_camera', LaserScan, laser_cb)


while not rospy.is_shutdown():
    angle = range_max
    for r in ranges:
        if r > range_max or r < range_min:
            continue
        
        x = r * cos(angle)
        z = r * sin(angle)
        
        for y in range(-0.1,0.1,0.01)
            pass

        angle += angle_increment


    rospy.spinOnce()
