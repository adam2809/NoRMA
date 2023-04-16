#!/usr/bin/env python3

import rospy
import math
import numpy as np
from geometry_msgs.msg import Pose2D

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

f = open('test.csv','w')
def pose_cb (msg):
    print('cos')
    x_diff = msg.x - prev.x
    y_diff = msg.y - prev.y
    theta_diff = msg.theta - prev.theta
    
    theta_no_zero = 0.001 if msg.theta == 0 else msg.theta

    linear_vel = x_diff / math.cos(theta_no_zero) + y_diff / math.sin(theta_no_zero)
    angular_vel = theta_diff

    prev.x = msg.x
    prev.y = msg.y
    prev.theta = msg.theta
    f.write("{} , {}\n".format(linear_vel,angular_vel))

    
def close_file():
    f.close()

rospy.init_node('scan_matching_vel')


sub = rospy.Subscriber('/pose2D', Pose2D, pose_cb)
rospy.on_shutdown(close_file)
rospy.spin()
