cmake_minimum_required(VERSION 2.8.3)
project(norma_nav)

## Find catkin and any catkin packages
find_package(catkin REQUIRED COMPONENTS roscpp rospy std_msgs genmsg costmap_2d tf2 base_local_planner)

## Declare a catkin package
catkin_package()
