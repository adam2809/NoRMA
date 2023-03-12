cmake_minimum_required(VERSION 2.8.3)
project(norma_nav)

## Find catkin and any catkin packages
find_package(catkin REQUIRED COMPONENTS roscpp rospy std_msgs genmsg costmap_2d tf2 base_local_planner)

## Declare a catkin package
catkin_package()

## Build talker and listener
include_directories(include ${catkin_INCLUDE_DIRS})

add_executable(collision_checker src/collision_checker.cpp)
target_link_libraries(collision_checker ${catkin_LIBRARIES})
