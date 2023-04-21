#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Imu,Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import cv_bridge
import numpy
from math import cos,sin
import pyrealsense2
from sensor_msgs.msg import CameraInfo,LaserScan
from geometry_msgs.msg import Point32


roll = pitch = yaw = 0.0

height = 0
width = 0

thresh = 1
bridge = cv_bridge.CvBridge()
rgb = []
vis_pub = rospy.Publisher('/camera/vis', Image,queue_size=10)
def rgb_cb (msg):
    global width,height,rgb
    width = msg.width 
    height = msg.height 
    
    rgb = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')


angle_min = 0
angle_max = 0
angle_increment = 0

ranges = []
range_min = 0
range_max = 0
def laser_cb(msg):
    global ranges,angle_min,angle_max,angle_increment,range_min,range_max
    ranges = msg.ranges

    angle_min = msg.angle_min
    angle_max = msg.angle_max
    angle_increment = msg.angle_increment

    range_min = msg.range_min
    range_max = msg.range_max

def get_pixel_from_point(cam_info,point):
    _intrinsics = pyrealsense2.intrinsics()
    _intrinsics.width = cam_info.width
    _intrinsics.height = cam_info.height
    _intrinsics.ppx = cam_info.K[2]
    _intrinsics.ppy = cam_info.K[5]
    _intrinsics.fx = cam_info.K[0]
    _intrinsics.fy = cam_info.K[4]
    _intrinsics.model  = pyrealsense2.distortion.none
    _intrinsics.coeffs = [i for i in cam_info.D]
    res = pyrealsense2.rs2_project_point_to_pixel(_intrinsics, point)
    return res

rospy.init_node('rear_view_visualization')
rgb_info = rospy.wait_for_message('/camera/color/camera_info', CameraInfo, timeout=10)

cv2.namedWindow( "costam", cv2.WINDOW_AUTOSIZE );
rospy.Subscriber('/camera/color/image_raw', Image, rgb_cb)

msg = rospy.wait_for_message('/camera/color/image_raw', Image, timeout=10)
rgb = numpy.copy(bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8'))

rospy.Subscriber('/scan_camera', LaserScan, laser_cb)

rate = rospy.Rate(30)

while not rospy.is_shutdown():

    angle = angle_max

    vis = rgb
    for r in ranges:
        if r > range_max or r < range_min:
            continue
        
        print(angle)
        x = r * cos(angle)
        z = r * sin(angle)
        
        (x_img,y_img) = get_pixel_from_point(rgb_info,[x,0,z]) 
        x_img = int(x_img)
        y_img = int(y_img)
        print(x_img)
        print(y_img)
        print('-------------------')
        vis = cv2.circle(vis, (x_img,y_img), radius=5, color=(0, 0, 255), thickness=-1)

        angle += angle_increment
    
    try:
        vis_msg = bridge.cv2_to_imgmsg(vis, "bgr8")
        vis_msg.header.frame_id = "camera_link"
        vis_pub.publish(vis_msg)
    except CvBridgeError as e:
        print(e)

    rate.sleep()

