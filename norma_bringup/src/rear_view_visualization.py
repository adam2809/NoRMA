#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Imu,Image
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from cv_bridge import CvBridge

roll = pitch = yaw = 0.0

height = 0
width = 0

thresh = 1
def rgb_cb msg):
    global width,height
    width = msg.width 
    height = msg.height 
    
    rgb = bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')




def depth_cb(msg):
    global width,height
    if msg.width != width or msg.height != height:
        rospy.logerr('Unequal width or hight values between depth and rgb images')

    depth = msg.data[:]


rospy.init_node('rear_view_visualization')

rospy.Subscriber('/camera/color/image_raw', Image, rgb_cb)
rospy.Subscriber('/camera/depth/image_rect_raw', Image, depth_cb)
rospy.Publisher('/scan_camera', LaserScan, laser_cb)
while not rospy.is_shutdown():
    for i in height*width:

        x = i % width
        y = i // width
    rospy.spinOnce()
