#include "ros/ros.h"

int main(int argc, char **argv)
{
  ros::Duration(5).sleep();
  ros::NodeHandle nh("/costmap_node");


  ros::spin();

  return 0;
}

