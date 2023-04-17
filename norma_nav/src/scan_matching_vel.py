#!/usr/bin/env python3

import rospy
import math
import numpy as np
from geometry_msgs.msg import TwistWithCovariance,Twist
from nav_msgs.msg import Odometry

curr_x = 0
f = open('test.csv','w')
def odom_cb (msg):
    linear_vel = msg.twist.twist.linear.x
    f.write("{} ,{} , {}\n".format(msg.header.stamp,linear_vel,curr_x))


def cmd_vel_cb(msg):
    global curr_x
    curr_x = msg.linear.x

    
def close_file():
    f.close()

rospy.init_node('scan_matching_vel')


sub = rospy.Subscriber('/odom', Odometry, odom_cb)
sub = rospy.Subscriber('/cmd_vel', Twist, cmd_vel_cb)
rospy.on_shutdown(close_file)
rospy.spin()
