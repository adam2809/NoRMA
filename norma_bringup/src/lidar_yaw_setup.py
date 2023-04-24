#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan


left_center_range = 0 
right_center_range = 0
def get_lidar(msg):
    global left_center_range,right_center_range
    center_range = msg.ranges[len(msg.ranges)//2]
    if msg.header.frame_id == 'laser_left':
        left_center_range = center_range
        print("""
left = {}
right = {}
--------------------
        """.format(left_center_range,right_center_range))
    else:
        right_center_range = center_range


     

rospy.init_node('lidars_yaw_setup')

rospy.Subscriber('/scan_laser_left', LaserScan, get_lidar)
rospy.Subscriber('/scan_laser_right', LaserScan, get_lidar)

rospy.spin()
