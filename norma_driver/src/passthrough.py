#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from std_msgs.msg import Header

rospy.init_node('passthrough')

cmd_joy_pub = rospy.Publisher('/cmd_joy', Joy, queue_size=10)

def joy_cb (msg):
   x = msg.axes[0]
   z = msg.axes[1]

   h = Header()
   h.stamp = rospy.Time.now()

   joy = Joy()
   joy.axes = [x,z]
   joy.header = h

   cmd_joy_pub.publish(joy)


rospy.Subscriber('/joy', Joy, joy_cb)

rospy.spin()
