#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Imu
from tf.transformations import euler_from_quaternion, quaternion_from_euler

roll = pitch = yaw = 0.0

def get_rotation (msg):
    global roll, pitch, yaw
    orientation_q = msg.orientation
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    (roll,pitch,yaw) =  euler_from_quaternion (orientation_list)

    print('''
---------------
roll  = {0}
pitch = {1}
yaw   = {2}
---------------
    '''.format(roll,pitch,yaw))
     

rospy.init_node('my_quaternion_to_euler')

sub = rospy.Subscriber('/imu/data', Imu, get_rotation)

rospy.spin()
