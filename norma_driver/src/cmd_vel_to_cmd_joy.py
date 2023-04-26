#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from nav_msgs.msg import Odometry
from std_msgs.msg import Header

rospy.init_node('passthrough')

cmd_joy_pub = rospy.Publisher('/cmd_joy', Joy, queue_size=10)


class PID():
    def __init__(self,kp,ki,kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd

        self.integral = 0
        self.prev_err = 0


    def control(self,new_input,desired,timestep):
        err = desired - new_input
        self.integral = self.integral + err * timestep
        derivative = (err - self.prev_err) / timestep

        self.prev_err = err

        return self.kp * err + self.ki * self.integral + self.kd * derivative

def trim_deadzone(curr_dz,desi_dz,curr_val):
    if curr_val > desi_dz:
        return curr_dz + curr_val
    elif curr_val < -desi_dz:
        return -(curr_dz + curr_val)
    else:
        return 0


pid_angular = PID(50,5,0)
pid_linear = PID(30,3,0)

odom_linear_vel = 0
odom_angular_vel = 0
def odom_cb (msg):
    global odom_linear_vel,odom_angular_vel
    odom_linear_vel = msg.twist.twist.linear.x
    odom_angular_vel = msg.twist.twist.angular.z


cmd_linear_vel = 0
cmd_angular_vel = 0
prev_cmd_vel_msg = 0
def cmd_vel_cb(msg):
    global prev_cmd_vel_msg, cmd_linear_vel,cmd_angular_vel
    cmd_linear_vel = msg.linear.x
    cmd_angular_vel = msg.angular.z


sub = rospy.Subscriber('/cmd_vel', Twist, cmd_vel_cb)
sub = rospy.Subscriber('/odom', Odometry, odom_cb)

RATE = 10
rate = rospy.Rate(RATE)
timestep = 1.0/RATE

while not rospy.is_shutdown():
    new_linear_vel = pid_linear.control(
      odom_linear_vel,
      cmd_linear_vel,
      timestep
    )

    new_angular_vel = pid_angular.control(
      odom_angular_vel,
      cmd_angular_vel,
      timestep
    )

    x = trim_deadzone(15,5,new_linear_vel)
    z = trim_deadzone(20,5,new_angular_vel)

    h = Header()
    h.stamp = rospy.Time.now()

    joy = Joy()
    joy.axes = [x,z]
    joy.header = h

    print(f"Pubishing linear = {x} and angular = {z}")

    cmd_joy_pub.publish(joy)
    rate.sleep()


