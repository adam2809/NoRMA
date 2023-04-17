#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from std_msgs.msg import Header

rospy.init_node('passthrough')

cmd_joy_pub = rospy.Publisher('/cmd_joy', Joy, queue_size=10)


class PID():
    def __init__(self,kp,ki,kd,desired,timestep,err_fun):
        self.kp = kp
        self.ki = ki
        self.kd = kd

        self.integral = 0
        self.prev_err = 0

        self.err_fun = err_fun


    def control(self,new_input,desired,timestep):
        err = desired - new_input
        p = self.kp * err
        self.integral = (self.integral + err * timestep) * self.kp
        d = self.kd * (err - self.prev_err) * timestep

        self.prev_err = err

        return p + self.integral + d



pid_angular = PID(0.2,0,0)
pid_linear = PID(10,0,0)

odom_linear_vel = 0
odom_angular_vel = 0
def odom_cb (msg):
    global odom_linear_vel,odom_angular_vel
    odom_linear_vel = msg.twist.twist.linear.x
    odom_angular_vel = msg.twist.twist.angular.z


prev_cmd_vel_msg = 0
def cmd_vel_cb(msg):
    global last_msg
    cmd_linear_vel = msg.linear.x
    cmd_angular_vel = msg.angular.z

    new_linear_vel = pid_linear.control(
      odom_linear_vel,
      cmd_linear_vel,
      rospy.get_rostime().secs - prev_cmd_vel_msg
    )

    prev_cmd_vel_msg = rospy.get_rostime().secs

    x = new_linear_vel
    z = msg.axes[1]

    h = Header()
    h.stamp = rospy.Time.now()

    joy = Joy()
    joy.axes = [x,z]
    joy.header = h

    cmd_joy_pub.publish(joy)


sub = rospy.Subscriber('/cmd_vel', Twist, cmd_vel_cb)
sub = rospy.Subscriber('/odometry/filtered_map', Odometry, odom_cb)

rospy.spin()
