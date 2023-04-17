#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy

rospy.init_node('passthrough')

cmd_joy_pub = rospy.Publisher('/cmd_joy', Twist, queue_size=10)

def joy_cb (msg):
   x = msg.axes[0]
   z = msg.axes[1]

   h = Header()
   h.stamp = rospy.Time.now()

   joy = Twist()
   joy.axis = [x,z]
   joy.header = h

   cmd_vel_pub.publish(joy)


rospy.Subscriber('/joy', Joy, joy_cb)

rospy.spin()
