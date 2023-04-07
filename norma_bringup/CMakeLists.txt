cmake_minimum_required(VERSION 3.0.2)
project(norma_bringup)
find_package(catkin REQUIRED laser_geometry)

find_package(catkin_simple REQUIRED)
catkin_simple(ALL_DEPS_REQUIRED)


cs_add_executable(merge_scans src/merge_scans.cpp)

cs_install()
cs_export()
















