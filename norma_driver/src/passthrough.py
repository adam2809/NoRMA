#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy

def joy_cb (msg):
   x = msg.axes[0]
   y = msg.axes[1]

   twist = Twist()
   twist.linear.x = x
   twist.angular.z = y

   cmd_vel_pub.pub(twist)

rospy.init_node('scan_matching_vel')


rospy.Subscriber('/joy', Joy, self.joy_cb)
self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

rospy.spin()
