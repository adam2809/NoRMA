#!/usr/bin/env python3

import rospy
import math
import numpy as np
from geometry_msgs.msg import Pose2D, Twist

#def get_orthogonal_rotation_matrix():
#    mat = ""
#    mat += f"{math.cos(t)} {math.sin(t)} 0 ;}"
#    mat += f"{-math.cos(t)} {-math.sin(t)} 0 ;}"
#    mat += f"{0 0 1}"
#    return np.matrix(mat)
prev = Pose2D()
prev.x = 0
prev.y = 0
prev.theta = 0
prev_time = 0.0

curr_x = 0
f = open('test.csv','w')
def pose_cb (msg):
    global prev_time
    x_diff = msg.x - prev.x
    y_diff = msg.y - prev.y
    theta_diff = msg.theta - prev.theta
    
    theta_no_zero = 0.001 if msg.theta == 0 else msg.theta
    time_diff = rospy.get_time()-prev_time
    linear_vel = math.sqrt(x_diff**2 + y_diff**2)/time_diff
    angular_vel = theta_diff/time_diff

    prev.x = msg.x
    prev.y = msg.y
    prev.theta = msg.theta
    prev_time = rospy.get_time()
    f.write("{} , {}\n".format(linear_vel,curr_x))


def cmd_vel_cb(msg):
    global curr_x
    curr_x = msg.linear.x

    
def close_file():
    f.close()

rospy.init_node('scan_matching_vel')


sub = rospy.Subscriber('/pose2D', Pose2D, pose_cb)
sub = rospy.Subscriber('/cmd_vel', Twist, cmd_vel_cb)
rospy.on_shutdown(close_file)
rospy.spin()
