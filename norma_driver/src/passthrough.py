#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy

rospy.init_node('passthrough')

cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

def joy_cb (msg):
   x = msg.axes[0]
   y = msg.axes[1]

   twist = Twist()
   twist.linear.x = x
   twist.angular.z = 0

   cmd_vel_pub.publish(twist)


rospy.Subscriber('/joy', Joy, joy_cb)

rospy.spin()
