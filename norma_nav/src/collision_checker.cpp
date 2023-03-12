#include <ros/ros.h>

#include "nav_msgs/Odometry.h"

#include <costmap_2d/costmap_2d_ros.h>

#include <tf2_ros/transform_listener.h>

#include <base_local_planner/trajectory.h>
#include <base_local_planner/local_planner_limits.h>
#include <base_local_planner/simple_trajectory_generator.h>
#include <base_local_planner/simple_scored_sampling_planner.h>
#include <base_local_planner/obstacle_cost_function.h>

#include <vector>
#include <Eigen/Core>

Eigen::Vector3d vel(0, 0, 0);

void odom_cb(const nav_msgs::Odometry::ConstPtr& msg)
{
  ROS_INFO("Vel-> Linear: [%f], Angular: [%f]", msg->twist.twist.linear.x,msg->twist.twist.angular.z);
  vel(0) = msg->twist.twist.linear.x;
  vel(2) = msg->twist.twist.angular.z;
}
int main(int argc, char** argv)
{
  ros::init(argc, argv, "costmap_node");
  ros::NodeHandle nh;
  tf2_ros::Buffer buffer(ros::Duration(10));
  tf2_ros::TransformListener tf(buffer);
  costmap_2d::Costmap2DROS costmap("costmap", buffer);

  ros::Subscriber sub = nh.subscribe("odom", 1000, odom_cb);

  base_local_planner::SimpleTrajectoryGenerator traj_generator;

  std::vector<base_local_planner::TrajectorySampleGenerator*> generator_list;
  generator_list.push_back(&traj_generator);

  std::vector<base_local_planner::TrajectoryCostFunction*> critics;
  base_local_planner::ObstacleCostFunction obstacle_costs(costmap.getCostmap());
  obstacle_costs.setSumScores(false);
  obstacle_costs.setParams(0.26, 0.2, 0.3);
  obstacle_costs.setScale(0.02);
  obstacle_costs.setFootprint(costmap.getRobotFootprint());
  critics.push_back(&obstacle_costs);

  base_local_planner::SimpleScoredSamplingPlanner collision_checking_planner = base_local_planner::SimpleScoredSamplingPlanner(generator_list, critics);
  Eigen::Vector3d pos(0, 0, 0);
  Eigen::Vector3d goal(0, 0, 0);

  ros::Rate loop_rate(10);
  while (ros::ok()){
    base_local_planner::Trajectory traj;
    traj_generator.initialise(pos, vel, goal, &limits, 20);
    traj_generator.generateTrajectory(pos, vel, 20, traj);

//  double cost = collision_checking_planner.scoreTrajectory(traj, -1);

//  if(cost >= 0) {
//    ROS_INFO("GOOD trajectory");
//  }else{
//    ROS_INFO("BAD trajectory");
//  }


    ros::spinOnce();

    loop_rate.sleep();
  }


  return (0);
}
